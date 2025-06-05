#!/usr/bin/env python3
"""
F1 Telemetry Analysis Runner

This script runs the F1 telemetry analysis using the configuration
specified in f1_config.py
"""

from f1_config import *
from f1_telemetry_analysis import F1TelemetryAnalyzer

def run_analysis():
    """
    Run the F1 telemetry analysis with the specified configuration.
    """
    analyzer = F1TelemetryAnalyzer()
    
    print("F1 Telemetry Analysis Tool")
    print("=" * 50)
    print(f"Configuration:")
    print(f"  Year: {YEAR}")
    print(f"  Race: {RACE}")
    print(f"  Session: {SESSION}")
    print(f"  Drivers: {DRIVER1} vs {DRIVER2}")
    print("=" * 50)
    
    # Load session
    if not analyzer.load_session(YEAR, RACE, SESSION):
        print("\n❌ Failed to load session. Please check your configuration.")
        print("\nTips:")
        print("- Make sure the race name is correct (e.g., 'Monaco', 'Silverstone')")
        print("- Check that the year and session type are valid")
        print("- Some older races might not have all session types available")
        return False
    
    # Compare drivers
    if analyzer.compare_drivers(DRIVER1, DRIVER2):
        # Get and display summary
        summary = analyzer.get_comparison_summary()
        
        print("\n" + "=" * 60)
        print("FASTEST LAP COMPARISON SUMMARY")
        print("=" * 60)
        
        print(f"\n🏎️  {summary['driver1']['name']} ({summary['driver1']['team']})")
        print(f"     Lap Time: {summary['driver1']['lap_time']}")
        print(f"     Lap Number: {summary['driver1']['lap_number']}")
        print(f"     Max Speed: {summary['driver1']['max_speed']:.1f} km/h")
        print(f"     Avg Speed: {summary['driver1']['avg_speed']:.1f} km/h")
        
        print(f"\n🏎️  {summary['driver2']['name']} ({summary['driver2']['team']})")
        print(f"     Lap Time: {summary['driver2']['lap_time']}")
        print(f"     Lap Number: {summary['driver2']['lap_number']}")
        print(f"     Max Speed: {summary['driver2']['max_speed']:.1f} km/h")
        print(f"     Avg Speed: {summary['driver2']['avg_speed']:.1f} km/h")
        
        print(f"\n🏆 Faster Driver: {summary['faster_driver']}")
        print(f"⏱️  Time Difference: {abs(summary['time_difference_seconds']):.3f} seconds")
        
        # Save data if requested
        if SAVE_CSV:
            filename = f"f1_{YEAR}_{RACE}_{SESSION}_{DRIVER1}_vs_{DRIVER2}.csv"
            analyzer.save_data(filename)
        
        # Create and save plots if requested
        if SAVE_PLOTS or SHOW_PLOTS:
            analyzer.plot_speed_comparison(save_plot=SAVE_PLOTS)
            
            # Generate advanced interactive visualizations
            from f1_advanced_visuals import F1AdvancedVisualizer
            visualizer = F1AdvancedVisualizer(analyzer)
            visualizer.generate_all_visualizations()
        
        print("\n" + "=" * 60)
        print("✅ Analysis Complete!")
        print("=" * 60)
        
        if SAVE_CSV:
            print(f"📊 Telemetry data saved as CSV")
        if SAVE_PLOTS:
            print(f"📈 Comparison plots saved as PNG")
        
        print("\nNext steps:")
        print("- Examine the CSV file for detailed telemetry data")
        print("- Analyze the speed and throttle comparison plots")
        print("- Try different driver combinations or race sessions")
        print("- Modify f1_config.py to analyze other races/drivers")
        
        return True
    else:
        print("\n❌ Failed to compare drivers. Please check:")
        print("- Driver codes are correct (3-letter codes like 'VER', 'HAM')")
        print("- Both drivers participated in the selected session")
        print("- The session has valid lap data")
        return False

if __name__ == "__main__":
    try:
        run_analysis()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        print("\nPlease check your configuration and try again.")

