import os
import pandas as pd
import streamlit as st
from scheduler import TrainScheduler, build_graph, Config
from visualize import plot_gantt

BASE = os.path.dirname(os.path.dirname(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "outputs")

st.set_page_config(page_title="Smart Train Scheduling Simulator", layout="wide")
st.title("🚆 Smart Train Scheduling Simulator")

# Sidebar config
st.sidebar.header("⚙️ Scheduler Settings")
dwell_min = st.sidebar.number_input("Dwell Time (minutes)", 1, 10, 2)
headway_min = st.sidebar.number_input("Headway (minutes)", 1, 10, 2)

# File inputs
st.sidebar.header("📂 Data Files")
stations_file = st.sidebar.file_uploader("Stations CSV", type="csv")
edges_file = st.sidebar.file_uploader("Edges CSV", type="csv")
trains_file = st.sidebar.file_uploader("Trains CSV", type="csv")

run_btn = st.sidebar.button("Run Scheduler")

if run_btn:
    try:
        # Load datasets
        if stations_file: stations_df = pd.read_csv(stations_file)
        else: stations_df = pd.read_csv(os.path.join(DATA, "stations.csv"))

        if edges_file: edges_df = pd.read_csv(edges_file)
        else: edges_df = pd.read_csv(os.path.join(DATA, "edges.csv"))

        if trains_file: trains_df = pd.read_csv(trains_file)
        else: trains_df = pd.read_csv(os.path.join(DATA, "trains.csv"))

        # Build graph and run scheduler
        G = build_graph(edges_df)
        config = Config(dwell_min=dwell_min, headway_min=headway_min)
        scheduler = TrainScheduler(G, config)
        schedule_df = scheduler.schedule_trains(trains_df)

        # Save and visualize
        os.makedirs(OUT, exist_ok=True)
        out_csv = os.path.join(OUT, "schedule.csv")
        schedule_df.to_csv(out_csv, index=False)

        out_png = os.path.join(OUT, "gantt.png")
        plot_gantt(out_csv, out_png)

        # Show results
        st.subheader("📋 Optimized Timetable")
        st.dataframe(schedule_df)

        st.subheader("📊 Gantt Chart")
        st.image(out_png, caption="Train Schedule Gantt Chart", use_container_width=True)

        # Download button
        with open(out_csv, "rb") as f:
            st.download_button("⬇️ Download Timetable CSV", f, file_name="schedule.csv")

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("Upload CSVs or use defaults, then click **Run Scheduler**.")
