# Project Resource Planner

A Streamlit-based web application for calculating and visualizing project resource allocation across weekly timelines.

## Features

- **Flexible Resource Allocation**: Split hours between General and Specialist resources
- **Dual Allocation Modes**: Choose between percentage-based or fixed hours allocation
- **Visual Planning**: Interactive bar charts showing weekly burn rates
- **Export Capability**: Download plans as CSV files
- **Linear Burn Model**: Automatically distributes hours evenly across project timeline

## Quick Start

### Prerequisites

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

```bash
# Install dependencies
uv sync
```

### Running the App

```bash
# Start the Streamlit app
uv run streamlit run planner.py

# Run with auto-reload (for development)
uv run streamlit run planner.py --server.runOnSave true
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Set Project Parameters** (in sidebar):
   - Enter total sold hours
   - Choose start and end dates
   - Select allocation mode (Percentage or Flat Hours)
   - Configure Specialist resource allocation

2. **View Results**:
   - See project metrics (duration, hours, burn rate)
   - Review weekly burn schedule chart
   - Expand data table for detailed breakdown
   - Download as CSV for external use

## How It Works

- **Week-based Planning**: Weeks start on Monday and hours are distributed evenly
- **Remainder Distribution**: Any remaining hours are allocated to the first weeks
- **Specialist Hours**: Tracked for allocation but not displayed in the weekly schedule (only General hours shown)

## Development

```bash
# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

## License

MIT