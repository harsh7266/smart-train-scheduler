# Smart Train Scheduling Simulator

A lightweight, Python-based simulator that **optimizes train timetables** across multiple stations using a **graph model** and **conflict-aware scheduling**. It produces a clean **timetable** and a **Gantt chart** visualization to showcase real-time decision support aligned with **smart signalling** concepts.

## ✨ Features
- Stations as **graph nodes**, tracks as **edges** (with travel times).
- **Conflict-free** scheduling on single-track segments with **headway** constraints.
- **Dwell time** at stations.
- Generates an **optimized timetable** (CSV) and a **Gantt chart** (PNG).
- Clean, readable code — perfect for a resume/portfolio.

## 🗂 Project Structure
```
smart-train-scheduler/
├─ data/
│  ├─ stations.csv       # Stations
│  ├─ edges.csv          # Track segments with travel minutes
│  └─ trains.csv         # Train routes + desired starts
├─ outputs/
│  ├─ schedule.csv       # Generated optimized timetable
│  └─ gantt.png          # Gantt chart visualization
├─ src/
│  ├─ scheduler.py       # Core scheduling logic
│  ├─ visualize.py       # Gantt plotting
│  └─ demo.py            # Entry point to run everything
├─ requirements.txt
└─ README.md
```

## 🚀 Quickstart

```bash
# 1) Create & activate a virtual env (optional but recommended)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the demo
python src/demo.py

# 4) Inspect outputs
# - outputs/schedule.csv
# - outputs/gantt.png
```

## 🧩 Data Format

### `data/stations.csv`
| station_id | name       |
|------------|------------|
| S1         | Station A  |
| S2         | Station B  |
| S3         | Station C  |
| S4         | Station D  |

### `data/edges.csv`
Undirected, single-track segments with travel time in minutes.
| source | target | travel_min |
|--------|--------|------------|
| S1     | S2     | 10         |
| S2     | S3     | 12         |
| S3     | S4     | 9          |
| S1     | S3     | 18         |
| S2     | S4     | 15         |
| S1     | S4     | 20         |

### `data/trains.csv`
| train_id | route            | start_time |
|----------|------------------|------------|
| T1       | S1,S2,S3,S4      | 08:00      |
| T2       | S1,S3,S4         | 08:05      |
| T3       | S2,S3            | 08:02      |

- **`route`** is a comma-separated list of station IDs.
- **`start_time`** is in 24h `HH:MM`.

## ⚙️ Scheduling Assumptions (Simple & Clear)
- Tracks are **single-track**: only one train can occupy a segment at a time.
- **Headway** (default 2 minutes) ensures safe separation between back-to-back uses of the same segment.
- **Dwell time** (default 2 minutes) at each intermediate station.
- Stations have ample platform capacity (simplified); focus is on track conflicts.
- If a conflict is detected on a segment, the affected train is **delayed to the earliest safe slot**.

## 🖼 Visualization
- A single **Gantt chart** (PNG) shows each train with horizontal bars for its **movement segments**.
- Generated at `outputs/gantt.png` after running `src/demo.py`.

## 🧪 Extend Ideas (if you want to impress further)
- Different dwell times per station.
- Per-direction travel times or explicit double-track segments.
- Station/platform capacity constraints.
- Route computation via shortest path when only origin-destination is given.
- Add a small Streamlit UI.

## 📜 License
MIT — free to use and modify.
