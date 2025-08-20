from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict
import pandas as pd
import networkx as nx

# ---------------------------
# Utility time helpers
# ---------------------------
def hhmm_to_min(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)

def min_to_hhmm(x: int) -> str:
    x = int(round(x))
    h = (x // 60) % 24
    m = x % 60
    return f"{h:02d}:{m:02d}"

def overlaps(a: Tuple[int,int], b: Tuple[int,int]) -> bool:
    # [a0, a1) overlaps [b0, b1) ?
    a0,a1 = a
    b0,b1 = b
    return a0 < b1 and b0 < a1

@dataclass
class Config:
    dwell_min: int = 2
    headway_min: int = 2

class TrainScheduler:
    def __init__(self, graph: nx.Graph, config: Config | None = None):
        self.G = graph
        self.config = config or Config()
        # occupancy per undirected edge (single track), store as sorted list of (start, end)
        self.edge_occupancy: Dict[Tuple[str,str], List[Tuple[int,int]]] = {}

    def _edge_key(self, u: str, v: str) -> Tuple[str,str]:
        return tuple(sorted((u,v)))

    def _find_slot_and_block(self, edge: Tuple[str,str], start: int, travel: int) -> Tuple[int,int]:
        """
        Find earliest available [s, e) on edge given desired start and travel time,
        respecting headway. Block it by inserting into occupancy.
        Returns (s, e).
        """
        key = self._edge_key(*edge)
        occ = self.edge_occupancy.setdefault(key, [])
        s = start
        e = s + travel

        # Scan/shift until no conflict with any existing occupancy expanded by headway
        changed = True
        while changed:
            changed = False
            for (o_s, o_e) in occ:
                # expand by headway both sides
                pad_s = o_s - self.config.headway_min
                pad_e = o_e + self.config.headway_min
                if overlaps((s, e), (pad_s, pad_e)):
                    s = o_e + self.config.headway_min
                    e = s + travel
                    changed = True
                    break

        # Insert and keep sorted
        occ.append((s,e))
        occ.sort(key=lambda x: x[0])
        self.edge_occupancy[key] = occ
        return s, e

    def schedule_trains(self, trains_df: pd.DataFrame) -> pd.DataFrame:
        """Return schedule rows: train_id, station, arrival, departure (HH:MM strings)"""
        rows = []
        for _, tr in trains_df.iterrows():
            train_id = tr["train_id"]
            route = [s.strip() for s in tr["route"].split(",") if s.strip()]
            desired_start = hhmm_to_min(tr["start_time"])

            # Track times as minutes from 00:00
            current_time = desired_start
            arrival_times = {}
            departure_times = {}

            # First station: we will set departure after we find slot on first edge
            first_station = route[0]
            # We'll fill arrival at first as same as departure for clarity later

            for i in range(len(route)-1):
                u, v = route[i], route[i+1]
                if not self.G.has_edge(u, v):
                    raise ValueError(f"No edge between {u} and {v} in graph.")
                travel = int(self.G[u][v]["travel_min"])

                # Earliest we can depart this segment is after dwell at u
                if i == 0:
                    earliest_depart = current_time
                else:
                    earliest_depart = current_time + self.config.dwell_min

                # Find a conflict-free slot on edge (u,v)
                s, e = self._find_slot_and_block((u,v), earliest_depart, travel)

                # Update departure at u and arrival at v
                departure_times[u] = s
                arrival_times[v] = e

                # Advance current time to arrival at v
                current_time = e

            # For stations with no explicit arrival/departure, fill logically
            # First station arrival = departure
            if first_station in departure_times:
                arrival_times[first_station] = departure_times[first_station]

            # Last station has arrival but no departure
            last_station = route[-1]

            # For intermediate stations, departure is when the next segment starts (which we set above)
            # arrival for intermediate stations already set when coming into them

            # Emit rows in route order
            for i, st in enumerate(route):
                arr = arrival_times.get(st, None)
                dep = departure_times.get(st, None)
                rows.append({
                    "train_id": train_id,
                    "station": st,
                    "arrival": min_to_hhmm(arr) if arr is not None else "",
                    "departure": min_to_hhmm(dep) if dep is not None else ""
                })

        schedule_df = pd.DataFrame(rows, columns=["train_id","station","arrival","departure"])                         .sort_values(["train_id"]).reset_index(drop=True)
        return schedule_df

def build_graph(edges_df: pd.DataFrame) -> nx.Graph:
    G = nx.Graph()
    for _, r in edges_df.iterrows():
        u = str(r["source"]).strip()
        v = str(r["target"]).strip()
        t = int(r["travel_min"])
        G.add_edge(u, v, travel_min=t)
    return G
