import math
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- App Configuration ---
st.set_page_config(page_title="Project Resource Planner", layout="wide")

st.title("📊 Project Resource Plan Builder")
st.markdown(
    "Define your hours, timeline, and resource split to generate a weekly burn plan."
)

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Project Inputs")

    # Input: Total Hours
    total_hours = st.number_input(
        "Total Sold Hours",
        min_value=1,
        value=1000,
        step=10,
        help="The total bucket of hours sold for this project.",
    )

    # Input: Timeline
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date", value=pd.to_datetime("today"))
    end_date = col2.date_input(
        "End Date", value=pd.to_datetime("today") + timedelta(weeks=12)
    )

    # Input: Resource Split
    st.subheader("Resource Split")
    
    # Toggle between percentage and flat hours
    allocation_mode = st.radio(
        "Allocation Mode",
        options=["Percentage", "Flat Hours"],
        horizontal=True,
        help="Choose how to allocate specialist resources.",
    )
    
    if allocation_mode == "Percentage":
        specialist_pct = st.slider(
            "Specialist Allocation (%)",
            min_value=0,
            max_value=100,
            value=20,
            help="Percentage of hours allocated to Specialist resources.",
        )
        specialist_hours_allocated = total_hours * (specialist_pct / 100.0)
    else:
        specialist_hours_allocated = st.number_input(
            "Specialist Hours",
            min_value=0,
            max_value=total_hours,
            value=int(total_hours * 0.2),
            step=10,
            help="Fixed number of hours allocated to Specialist resources.",
        )
        specialist_pct = (specialist_hours_allocated / total_hours * 100) if total_hours > 0 else 0

    # Calculated values for display
    general_hours_allocated = total_hours - specialist_hours_allocated
    general_pct = (general_hours_allocated / total_hours * 100) if total_hours > 0 else 0
    
    st.caption(
        f"**Split:** {round(general_hours_allocated, 1)} hrs General ({round(general_pct, 1)}%) / "
        f"{round(specialist_hours_allocated, 1)} hrs Specialist ({round(specialist_pct, 1)}%) - Specialist not shown in schedule"
    )

# --- Logic Engine ---

if start_date >= end_date:
    st.error("Error: End Date must be after Start Date.")
else:
    # 1. Generate the Weekly Timeline
    # We create a range of dates starting from the start_date, stepping by 7 days
    dates = pd.date_range(start=start_date, end=end_date, freq="W-MON")

    # If the start date isn't exactly a Monday, pandas might skip the first partial week.
    # Let's ensure we capture the start by using a manual weekly range if pandas returns empty or offsets it.
    if len(dates) == 0:
        dates = pd.date_range(
            start=start_date, periods=1
        )  # Fallback for <1 week projects

    num_weeks = len(dates)

    # 2. Calculate The Split
    # Specialist hours are allocated but not shown in the burn schedule
    total_specialist_hours = specialist_hours_allocated
    total_general_hours = general_hours_allocated

    # 3. Apply Linear Burn (Even Spread)
    # Only general hours are shown in the weekly schedule
    # Use integer division and distribute remainder across first weeks
    base_general_weekly = int(total_general_hours // num_weeks)
    general_remainder = int(total_general_hours % num_weeks)
    
    base_specialist_weekly = int(total_specialist_hours // num_weeks)
    specialist_remainder = int(total_specialist_hours % num_weeks)

    # 4. Build the DataFrame
    # Specialist hours are tracked for allocation but not displayed in schedule
    data = []
    for i, date in enumerate(dates):
        # Distribute remainder hours to first N weeks
        general_hours = base_general_weekly + (1 if i < general_remainder else 0)
        
        data.append(
            {
                "Week Starting": date.strftime("%Y-%m-%d"),
                "General Hours": general_hours,
            }
        )

    df = pd.DataFrame(data)

    # --- Dashboard Output ---

    # Top Level Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Project Duration", f"{num_weeks} Weeks")
    m2.metric("Total Sold Hours", f"{int(total_hours)} hrs")
    m3.metric("Specialist Hours (Allocated)", f"{int(total_specialist_hours)} hrs")
    if general_remainder > 0:
        m4.metric("General Hours/Week", f"{base_general_weekly}-{base_general_weekly + 1} hrs")
    else:
        m4.metric("General Hours/Week", f"{base_general_weekly} hrs")

    st.divider()

    # Resource Split Visualization
    st.subheader("Resource Allocation")
    
    col_metrics, col_chart = st.columns([2, 1])
    
    with col_metrics:
        # Create visual split representation using progress-like display
        st.write(f"**Total: {int(total_hours)} hours**")
        
        # Display as stacked metrics
        st.metric(
            "General Hours", 
            f"{int(total_general_hours)} hrs", 
            delta=f"{round(general_pct, 1)}%",
            delta_color="off"
        )
        st.metric(
            "Specialist Hours", 
            f"{int(total_specialist_hours)} hrs", 
            delta=f"{round(specialist_pct, 1)}%",
            delta_color="off"
        )
    
    with col_chart:
        # Create pie chart
        fig, ax = plt.subplots(figsize=(1.5, 1.5))
        
        sizes = [total_general_hours, total_specialist_hours]
        labels = ['General', 'Specialist']
        colors = ['#1f77b4', '#ff7f0e']  # Blue and orange
        explode = (0.05, 0)  # Slightly separate the General slice
        
        ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            textprops={'fontsize': 8}
        )
        ax.axis('equal')  # Equal aspect ratio ensures pie is circular
        
        st.pyplot(fig, use_container_width=False)
    
    st.divider()

    # Visuals
    st.subheader("Weekly Burn Schedule (General Resources Only)")

    # Show only general hours in the chart
    chart_data = df.set_index("Week Starting")[["General Hours"]]
    st.bar_chart(chart_data)

    # Data Table
    with st.expander("View Detailed Data Table", expanded=True):
        st.dataframe(df, use_container_width=True)

    # Download Button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Plan as CSV",
        data=csv,
        file_name="project_resource_plan.csv",
        mime="text/csv",
    )
