import os
import pandas as pd
from scheduler import TrainScheduler, build_graph, Config
from visualize import plot_gantt

BASE = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(BASE, 'data')
OUT = os.path.join(BASE, 'outputs')

def main():
    edges_df = pd.read_csv(os.path.join(DATA, 'edges.csv'))
    trains_df = pd.read_csv(os.path.join(DATA, 'trains.csv'))

    # Build graph
    G = build_graph(edges_df)

    # Configure scheduler
    config = Config(dwell_min=2, headway_min=2)
    scheduler = TrainScheduler(G, config)

    # Compute schedule
    schedule_df = scheduler.schedule_trains(trains_df)

    # Save
    out_csv = os.path.join(OUT, 'schedule.csv')
    os.makedirs(OUT, exist_ok=True)
    schedule_df.to_csv(out_csv, index=False)

    # Plot Gantt
    out_png = os.path.join(OUT, 'gantt.png')
    plot_gantt(out_csv, out_png)

    print(f"Saved schedule -> {out_csv}")
    print(f"Saved Gantt -> {out_png}")

if __name__ == '__main__':
    main()
