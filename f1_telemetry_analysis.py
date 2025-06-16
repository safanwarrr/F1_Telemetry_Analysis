#!/usr/bin/env python3
"""
F1 Telemetry Data Retrieval and Comparison Script

This script fetches F1 telemetry data using FastF1 and prepares it for
comparing mutliple drivers' telemetry data side by side.
"""

import fastf1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from typing import Tuple, Dict, Any

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Enable FastF1 cache to speed up data loading
import os
cache_dir = 'f1_cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
fastf1.Cache.enable_cache(cache_dir)

class F1TelemetryAnalyzer:
    def __init__(self):
        self.session = None
        self.driver1_data = None
        self.driver2_data = None
        self.combined_data = None
    
    def load_session(self, year: int, race: str, session_type: str) -> bool:
        """
        Load an F1 session for analysis.
        
        Args:
            year: Year of the race (e.g., 2024)
            race: Race name or location (e.g., 'Monaco', 'Silverstone')
            session_type: 'Q' for Qualifying, 'R' for Race, 'FP1', 'FP2', 'FP3' for practice
        
        Returns:
            bool: True if session loaded successfully
        """
        try:
            print(f"Loading {year} {race} {session_type} session...")
            self.session = fastf1.get_session(year, race, session_type)
            self.session.load()
            print(f"✅ Session loaded successfully!")
            print(f"Available drivers: {list(self.session.drivers)}")
            return True
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
    
    def get_fastest_lap_telemetry(self, driver: str) -> Dict[str, Any]:
        """
        Get telemetry data for a driver's fastest lap.
        
        Args:
            driver: Driver identifier (3-letter code like 'HAM', 'VER', etc.)
        
        Returns:
            dict: Dictionary containing lap data and telemetry
        """
        try:
            # Get driver's laps
            driver_laps = self.session.laps.pick_driver(driver)
            
            # Get fastest lap (excluding outliers)
            fastest_lap = driver_laps.pick_fastest()
            
            if fastest_lap.empty:
                raise ValueError(f"No valid laps found for driver {driver}")
            
            # Get telemetry for the fastest lap
            telemetry = fastest_lap.get_telemetry()
            
            # Add distance column if not present
            if 'Distance' not in telemetry.columns:
                telemetry['Distance'] = np.cumsum(telemetry['Speed'] / 3.6 * 0.1)  # Rough distance calculation
            
            driver_info = {
                'driver': driver,
                'lap_time': fastest_lap['LapTime'],
                'lap_number': fastest_lap['LapNumber'],
                'telemetry': telemetry,
                'team': fastest_lap['Team']
            }
            
            print(f"✅ Fastest lap for {driver}: {fastest_lap['LapTime']} (Lap {fastest_lap['LapNumber']})")
            return driver_info
            
        except Exception as e:
            print(f"❌ Error getting telemetry for {driver}: {e}")
            return None
    
    def compare_drivers(self, driver1: str, driver2: str) -> bool:
        """
        Compare two drivers' fastest laps and prepare combined telemetry data.
        
        Args:
            driver1: First driver's identifier
            driver2: Second driver's identifier
        
        Returns:
            bool: True if comparison data prepared successfully
        """
        if not self.session:
            print("❌ No session loaded. Please load a session first.")
            return False
        
        print(f"\nAnalyzing fastest laps for {driver1} vs {driver2}...")
        
        # Get telemetry for both drivers
        self.driver1_data = self.get_fastest_lap_telemetry(driver1)
        self.driver2_data = self.get_fastest_lap_telemetry(driver2)
        
        if not self.driver1_data or not self.driver2_data:
            print("❌ Failed to get telemetry data for one or both drivers")
            return False
        
        # Prepare combined data for comparison
        self._prepare_combined_data()
        
        return True
    
    def _prepare_combined_data(self):
        """
        Prepare combined telemetry data for easier comparison.
        """
        tel1 = self.driver1_data['telemetry'].copy()
        tel2 = self.driver2_data['telemetry'].copy()
        
        # Add driver identifier to each telemetry dataset
        tel1['Driver'] = self.driver1_data['driver']
        tel2['Driver'] = self.driver2_data['driver']
        
        # Combine the datasets
        self.combined_data = pd.concat([tel1, tel2], ignore_index=True)
        
        print(f"✅ Combined telemetry data prepared:")
        print(f"   {self.driver1_data['driver']}: {len(tel1)} data points")
        print(f"   {self.driver2_data['driver']}: {len(tel2)} data points")
    
    def get_comparison_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the comparison between the two drivers.
        
        Returns:
            dict: Summary statistics and information
        """
        if not self.driver1_data or not self.driver2_data:
            return None
        
        summary = {
            'driver1': {
                'name': self.driver1_data['driver'],
                'team': self.driver1_data['team'],
                'lap_time': self.driver1_data['lap_time'],
                'lap_number': self.driver1_data['lap_number'],
                'max_speed': self.driver1_data['telemetry']['Speed'].max(),
                'avg_speed': self.driver1_data['telemetry']['Speed'].mean()
            },
            'driver2': {
                'name': self.driver2_data['driver'],
                'team': self.driver2_data['team'],
                'lap_time': self.driver2_data['lap_time'],
                'lap_number': self.driver2_data['lap_number'],
                'max_speed': self.driver2_data['telemetry']['Speed'].max(),
                'avg_speed': self.driver2_data['telemetry']['Speed'].mean()
            }
        }
        
        # Calculate time difference
        time_diff = (self.driver1_data['lap_time'] - self.driver2_data['lap_time']).total_seconds()
        summary['time_difference_seconds'] = time_diff
        summary['faster_driver'] = self.driver1_data['driver'] if time_diff < 0 else self.driver2_data['driver']
        
        return summary
    
    def save_data(self, filename: str = 'f1_telemetry_comparison.csv'):
        """
        Save the combined telemetry data to a CSV file.
        
        Args:
            filename: Name of the output file
        """
        if self.combined_data is not None:
            self.combined_data.to_csv(filename, index=False)
            print(f"✅ Data saved to {filename}")
        else:
            print("❌ No data to save. Please run comparison first.")
    
    def plot_speed_comparison(self, save_plot: bool = True):
        """
        Create a basic speed comparison plot.
        
        Args:
            save_plot: Whether to save the plot as an image
        """
        if not self.driver1_data or not self.driver2_data:
            print("❌ No data to plot. Please run comparison first.")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Plot speed vs distance for both drivers
        tel1 = self.driver1_data['telemetry']
        tel2 = self.driver2_data['telemetry']
        
        plt.subplot(2, 1, 1)
        plt.plot(tel1['Distance'], tel1['Speed'], label=f"{self.driver1_data['driver']} ({self.driver1_data['team']})", linewidth=2)
        plt.plot(tel2['Distance'], tel2['Speed'], label=f"{self.driver2_data['driver']} ({self.driver2_data['team']})", linewidth=2)
        plt.xlabel('Distance (m)')
        plt.ylabel('Speed (km/h)')
        plt.title('Speed Comparison - Fastest Laps')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Plot throttle comparison
        plt.subplot(2, 1, 2)
        plt.plot(tel1['Distance'], tel1['Throttle'], label=f"{self.driver1_data['driver']} Throttle", linewidth=2)
        plt.plot(tel2['Distance'], tel2['Throttle'], label=f"{self.driver2_data['driver']} Throttle", linewidth=2)
        plt.xlabel('Distance (m)')
        plt.ylabel('Throttle (%)')
        plt.title('Throttle Comparison - Fastest Laps')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            plt.savefig('f1_speed_comparison.png', dpi=300, bbox_inches='tight')
            print("✅ Plot saved as f1_speed_comparison.png")
        
        plt.show()

    def plot_advanced_visuals(self):
        """
        Create advanced visualizations using Plotly.
        """
        import plotly.express as px
        import plotly.graph_objects as go

        if not self.driver1_data or not self.driver2_data:
            print("❌ No data to plot. Please run comparison first.")
            return

        # Speed vs Distance Plot
        fig1 = px.line(self.combined_data, x='Distance', y='Speed', color='Driver',
                      title='Speed vs Distance',
                      labels={'Speed': 'Speed (km/h)', 'Distance': 'Distance (m)'}
                      )
        fig1.show()

        # Gear Heatmap over Track
        fig2 = go.Figure()
        for driver in [self.driver1_data, self.driver2_data]:
            heatmap = go.Heatmap(
                z=driver['telemetry']['nGear'],
                x=driver['telemetry']['X'],
                y=driver['telemetry']['Y'],
                colorscale='Viridis',
                colorbar=dict(title='Gear')
            )
            fig2.add_trace(heatmap)

        fig2.update_layout(title='Gear Heatmap Over Track',
                           xaxis_title='X',
                           yaxis_title='Y')

        fig2.show()


def main():
    """
    Main function to demonstrate the F1 telemetry analysis.
    """
    analyzer = F1TelemetryAnalyzer()
    
    print("F1 Telemetry Analysis Tool")
    print("=" * 50)
    
    # Example usage - you can modify these parameters
    year = 2024
    race = "Monaco"  # You can change this to any race
    session_type = "Q"  # Q for Qualifying, R for Race
    driver1 = "VER"  # Max Verstappen
    driver2 = "LEC"  # Charles Leclerc
    
    print(f"\nConfiguration:")
    print(f"Year: {year}")
    print(f"Race: {race}")
    print(f"Session: {session_type}")
    print(f"Drivers: {driver1} vs {driver2}")
    
    # Load session
    if not analyzer.load_session(year, race, session_type):
        return
    
    # Compare drivers
    if analyzer.compare_drivers(driver1, driver2):
        # Get and display summary
        summary = analyzer.get_comparison_summary()
        print("\n" + "=" * 50)
        print("COMPARISON SUMMARY")
        print("=" * 50)
        print(f"{summary['driver1']['name']} ({summary['driver1']['team']})")
        print(f"  Lap Time: {summary['driver1']['lap_time']}")
        print(f"  Max Speed: {summary['driver1']['max_speed']:.1f} km/h")
        print(f"  Avg Speed: {summary['driver1']['avg_speed']:.1f} km/h")
        print()
        print(f"{summary['driver2']['name']} ({summary['driver2']['team']})")
        print(f"  Lap Time: {summary['driver2']['lap_time']}")
        print(f"  Max Speed: {summary['driver2']['max_speed']:.1f} km/h")
        print(f"  Avg Speed: {summary['driver2']['avg_speed']:.1f} km/h")
        print()
        print(f"Faster Driver: {summary['faster_driver']}")
        print(f"Time Difference: {abs(summary['time_difference_seconds']):.3f} seconds")
        
        # Save data and create plots
        analyzer.save_data()
        analyzer.plot_speed_comparison()
        analyzer.plot_advanced_visuals()
        
        print("\n✅ Analysis complete! Check the generated files for detailed data and visualizations.")


if __name__ == "__main__":
    main()

