# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

A Streamlit-based Project Resource Planner application that helps calculate and visualize project resource allocation across weekly timelines. The app supports splitting hours between General and Specialist resources with flexible allocation modes (percentage or flat hours).

## Development Environment

- **Python Version**: 3.9 (specified in `.python-version`)
- **Package Manager**: `uv` (with `uv.lock` for dependency locking)
- **Framework**: Streamlit 1.50.0+
- **Virtual Environment**: `.venv/` (managed by uv)

## Key Commands

### Environment Setup
```bash
# Install dependencies (uv will automatically create/use .venv)
uv sync

# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>
```

### Running the Application
```bash
# Run the Streamlit app
uv run streamlit run planner.py

# Run with auto-reload on file changes (development)
uv run streamlit run planner.py --server.runOnSave true
```

### Python Environment
```bash
# Activate virtual environment manually (if needed)
source .venv/bin/activate

# Run Python with project dependencies
uv run python <script.py>
```

## Architecture

### Application Structure

The application is a single-file Streamlit app (`planner.py`) organized into three main sections:

1. **Configuration & Inputs** (Sidebar)
   - Total hours input
   - Date range selection (start/end dates)
   - Resource split controls with dual allocation modes:
     - **Percentage mode**: Allocate Specialist hours as a percentage of total
     - **Flat hours mode**: Allocate a fixed number of Specialist hours

2. **Logic Engine** (Core processing)
   - Weekly timeline generation using pandas date ranges (W-MON frequency)
   - Resource split calculation (General vs Specialist hours)
   - Linear burn distribution with integer division and remainder handling
   - Remainder hours are distributed to first N weeks to ensure accurate totals

3. **Dashboard Output** (Main area)
   - Top-level metrics display (duration, hours, weekly burn rate)
   - Bar chart visualization (General hours only)
   - Expandable data table
   - CSV download functionality

### Key Design Decisions

- **Specialist hours are allocated but not displayed in the schedule** - only General hours appear in the weekly burn chart
- **Linear burn model** - hours are distributed evenly across weeks with any remainder hours allocated to the first weeks
- **Week-based planning** - weeks start on Monday (W-MON frequency)
- **Wide layout** - uses Streamlit's wide page config for better dashboard viewing

## Dependencies

- `streamlit>=1.50.0` - Web app framework
- `pandas` - Date range generation and data handling (transitive dependency)
- Standard library: `math`, `datetime`
