import pandas as pd
import matplotlib.pyplot as plt

def hhmm_to_min(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)

def plot_gantt(schedule_csv: str, output_png: str) -> None:
    # Load schedule
    df = pd.read_csv(schedule_csv)
    # For each train, create intervals for movement segments between stations
    trains = sorted(df["train_id"].unique())
    fig, ax = plt.subplots(figsize=(10, 5))

    yticks = []
    yticklabels = []

    y = 10  # start y position
    height = 8

    for train in trains:
        tdf = df[df["train_id"] == train].reset_index(drop=True)

        # Build (start, duration) tuples for each travel segment
        segments = []
        for i in range(len(tdf)-1):
            dep = tdf.loc[i, "departure"]
            arr = tdf.loc[i+1, "arrival"]
            if isinstance(dep, str) and dep and isinstance(arr, str) and arr:
                start = hhmm_to_min(dep)
                end = hhmm_to_min(arr)
                if end > start:
                    segments.append((start, end - start))

        if segments:
            # Use broken_barh to draw multiple segments on one row
            ax.broken_barh(segments, (y, height))

        yticks.append(y + height/2)
        yticklabels.append(train)
        y += height + 6  # spacing between rows

    ax.set_yticks(yticks)
    ax.set_yticklabels(yticklabels)
    ax.set_xlabel("Time (minutes from 00:00)")
    ax.set_title("Train Schedule Gantt Chart")
    ax.grid(True)

    fig.tight_layout()
    fig.savefig(output_png, dpi=150)
    plt.close(fig)
