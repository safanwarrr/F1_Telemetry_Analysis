# F1 Telemetry Analysis Tool

This tool fetches Formula 1 telemetry data using FastF1 and allows you to compare multiple drivers' telemetry data lap by lap and side by side.

## Quick Start

1. **Configure your analysis** by editing `f1_config.py`:
   ```python
   YEAR = 2024
   RACE = "Monaco"
   SESSION = "Q"  # Q for Qualifying, R for Race
   DRIVER1 = "VER"  # Max Verstappen
   DRIVER2 = "LEC"  # Charles Leclerc
   ```

2. **Run the analysis**:
   ```bash
   python3 run_f1_analysis.py
   ```

3. **View interactive visualizations**:
   ```bash
   python3 view_f1_visuals.py
   ```

4. **Launch interactive dashboard**:
   ```bash
   python3 launch_dashboard.py
   ```


## Files

### Core Analysis
- `f1_config.py` - Configuration file (modify this to change what you analyze)
- `run_f1_analysis.py` - Main runner script
- `f1_telemetry_analysis.py` - Core analysis functionality
- `f1_advanced_visuals.py` - Advanced static visualizations

### Interactive Dashboard
- `f1_dashboard.py` - Interactive web dashboard with Dash/Plotly
- `f1_dashboard_config.py` - Dashboard configuration settings
- `launch_dashboard.py` - Dashboard launcher with setup checks

### Utilities
- `view_f1_visuals.py` - Browser for static visualizations
- `quick_examples.py` - Pre-configured analysis examples
- `f1_summary.py` - System overview and status
- `README.md` - This documentation

## What You Get

- **Comparison Summary**: Lap times, speeds, and performance metrics
- **CSV Data**: Complete telemetry data for both drivers
- **Static Plots**: Matplotlib speed and throttle comparison plots (PNG)
- **Static Interactive Visualizations**: Advanced Plotly visualizations (HTML)
  - Speed vs Distance comparison
  - Track position with speed heatmap
  - Gear usage heatmap over track
  - Throttle and brake analysis
  - Speed delta plot (showing where each driver is faster)
  - Comprehensive dashboard with all metrics
- **Live Interactive Dashboard**: Web-based dashboard (Dash/Plotly)
  - Real-time filtering by drivers, laps, sessions
  - Dynamic chart updates
  - Multiple visualization modes
  - Professional web interface
  - Session loading and management
- **Cache**: FastF1 automatically caches data for faster subsequent runs

## Configuration Options

### Sessions
- `"Q"` - Qualifying
- `"R"` - Race
- `"FP1"`, `"FP2"`, `"FP3"` - Practice sessions
- `"S"` - Sprint (if available)

### Popular Races
- `"Monaco"` - Street circuit precision
- `"Silverstone"` - High-speed British GP
- `"Spa"` - Challenging with elevation
- `"Monza"` - Temple of speed
- `"Singapore"` - Night street race

### Driver Codes (2024)
- **Red Bull**: VER (Verstappen), PER (Perez)
- **Ferrari**: LEC (Leclerc), SAI (Sainz)
- **Mercedes**: HAM (Hamilton), RUS (Russell)
- **McLaren**: NOR (Norris), PIA (Piastri)
- **And more...** (see f1_config.py for complete list)

## Example Output

```
Fastest Lap Comparison Summary
==============================

🏎️  VER (Red Bull Racing)
     Lap Time: 0:01:10.270
     Max Speed: 318.2 km/h
     Avg Speed: 156.3 km/h

🏎️  LEC (Ferrari)
     Lap Time: 0:01:10.486
     Max Speed: 315.8 km/h
     Avg Speed: 154.9 km/h

🏆 Faster Driver: VER
⏱️  Time Difference: 0.216 seconds
```

## Tips

- **First run takes longer** as data is downloaded and cached
- **Subsequent runs are much faster** thanks to caching
- **Try different comparisons**: teammates, championship rivals, etc.
- **Analyze different sessions** to see how performance varies
- **Check the CSV data** for detailed analysis opportunities
- **Open interactive HTML files** in your browser for dynamic exploration
- **Use the visualization viewer** (`python3 view_f1_visuals.py`) for easy access

## Troubleshooting

- Make sure race names match exactly (e.g., "Monaco", not "Monaco GP")
- Driver codes must be 3-letter codes (e.g., "VER", not "Verstappen")
- Some older races may not have all session types
- Internet connection required for first-time data download

