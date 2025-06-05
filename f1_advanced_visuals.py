#!/usr/bin/env python3
"""
F1 Advanced Visualization Module

This module creates advanced interactive visualizations using Plotly
for F1 telemetry data analysis.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

class F1AdvancedVisualizer:
    def __init__(self, analyzer):
        """
        Initialize the visualizer with an F1TelemetryAnalyzer instance.
        
        Args:
            analyzer: F1TelemetryAnalyzer instance with loaded data
        """
        self.analyzer = analyzer
        self.output_dir = "f1_visualizations"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def create_speed_distance_plot(self, save_html=True):
        """
        Create interactive speed vs distance plot.
        """
        if self.analyzer.combined_data is None:
            print("❌ No data available for plotting")
            return None
        
        fig = px.line(
            self.analyzer.combined_data, 
            x='Distance', 
            y='Speed', 
            color='Driver',
            title='Speed vs Distance Comparison',
            labels={'Speed': 'Speed (km/h)', 'Distance': 'Distance (m)'},
            hover_data=['Time', 'nGear', 'Throttle', 'Brake']
        )
        
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified',
            xaxis_title='Distance (m)',
            yaxis_title='Speed (km/h)',
            legend_title='Driver',
            height=600
        )
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/speed_distance_comparison.html"
            fig.write_html(filename)
            print(f"✅ Speed vs Distance plot saved as {filename}")
        
        return fig
    
    def create_track_position_plot(self, save_html=True):
        """
        Create track position plot with speed coloring.
        """
        if not self.analyzer.driver1_data or not self.analyzer.driver2_data:
            print("❌ No driver data available for plotting")
            return None
        
        fig = go.Figure()
        
        # Add driver 1 track position with speed coloring
        tel1 = self.analyzer.driver1_data['telemetry']
        fig.add_trace(go.Scatter(
            x=tel1['X'],
            y=tel1['Y'],
            mode='markers+lines',
            marker=dict(
                color=tel1['Speed'],
                colorscale='Viridis',
                size=4,
                colorbar=dict(title='Speed (km/h)', x=1.02)
            ),
            line=dict(width=3),
            name=f"{self.analyzer.driver1_data['driver']} Track + Speed",
            hovertemplate='X: %{x}<br>Y: %{y}<br>Speed: %{marker.color} km/h<extra></extra>'
        ))
        
        # Add driver 2 track position
        tel2 = self.analyzer.driver2_data['telemetry']
        fig.add_trace(go.Scatter(
            x=tel2['X'],
            y=tel2['Y'],
            mode='lines',
            line=dict(width=3, dash='dash'),
            name=f"{self.analyzer.driver2_data['driver']} Track",
            hovertemplate='X: %{x}<br>Y: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Track Layout with Speed Heatmap',
            xaxis_title='X Position (m)',
            yaxis_title='Y Position (m)',
            template='plotly_white',
            height=600,
            showlegend=True,
            xaxis=dict(scaleanchor="y", scaleratio=1)
        )
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/track_position_speed.html"
            fig.write_html(filename)
            print(f"✅ Track position plot saved as {filename}")
        
        return fig
    
    def create_gear_heatmap(self, save_html=True):
        """
        Create gear usage heatmap over track position.
        """
        if not self.analyzer.driver1_data or not self.analyzer.driver2_data:
            print("❌ No driver data available for plotting")
            return None
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                f"{self.analyzer.driver1_data['driver']} Gear Usage",
                f"{self.analyzer.driver2_data['driver']} Gear Usage"
            ),
            specs=[[{"type": "scatter"}, {"type": "scatter"}]]
        )
        
        # Driver 1 gear heatmap
        tel1 = self.analyzer.driver1_data['telemetry']
        fig.add_trace(
            go.Scatter(
                x=tel1['X'],
                y=tel1['Y'],
                mode='markers',
                marker=dict(
                    color=tel1['nGear'],
                    colorscale='RdYlBu_r',
                    size=6,
                    colorbar=dict(title='Gear', x=0.48)
                ),
                name=f"{self.analyzer.driver1_data['driver']} Gear",
                hovertemplate='X: %{x}<br>Y: %{y}<br>Gear: %{marker.color}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Driver 2 gear heatmap
        tel2 = self.analyzer.driver2_data['telemetry']
        fig.add_trace(
            go.Scatter(
                x=tel2['X'],
                y=tel2['Y'],
                mode='markers',
                marker=dict(
                    color=tel2['nGear'],
                    colorscale='RdYlBu_r',
                    size=6,
                    colorbar=dict(title='Gear', x=1.02)
                ),
                name=f"{self.analyzer.driver2_data['driver']} Gear",
                hovertemplate='X: %{x}<br>Y: %{y}<br>Gear: %{marker.color}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title='Gear Usage Heatmap Over Track',
            template='plotly_white',
            height=600,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="X Position (m)", scaleanchor="y", scaleratio=1)
        fig.update_yaxes(title_text="Y Position (m)")
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/gear_heatmap.html"
            fig.write_html(filename)
            print(f"✅ Gear heatmap saved as {filename}")
        
        return fig
    
    def create_throttle_brake_analysis(self, save_html=True):
        """
        Create throttle and brake analysis plots.
        """
        if self.analyzer.combined_data is None:
            print("❌ No data available for plotting")
            return None
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Throttle vs Distance', 'Brake vs Distance'),
            vertical_spacing=0.1
        )
        
        # Separate data by driver
        for driver in self.analyzer.combined_data['Driver'].unique():
            driver_data = self.analyzer.combined_data[self.analyzer.combined_data['Driver'] == driver]
            
            # Throttle plot
            fig.add_trace(
                go.Scatter(
                    x=driver_data['Distance'],
                    y=driver_data['Throttle'],
                    mode='lines',
                    name=f'{driver} Throttle',
                    line=dict(width=2),
                    hovertemplate='Distance: %{x}m<br>Throttle: %{y}%<extra></extra>'
                ),
                row=1, col=1
            )
            
            # Brake plot (convert boolean to numeric)
            brake_numeric = driver_data['Brake'].astype(int) * 100
            fig.add_trace(
                go.Scatter(
                    x=driver_data['Distance'],
                    y=brake_numeric,
                    mode='lines',
                    name=f'{driver} Brake',
                    line=dict(width=2),
                    hovertemplate='Distance: %{x}m<br>Braking: %{y}%<extra></extra>'
                ),
                row=2, col=1
            )
        
        fig.update_layout(
            title='Throttle and Brake Analysis',
            template='plotly_white',
            height=800,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Distance (m)")
        fig.update_yaxes(title_text="Throttle (%)", row=1, col=1)
        fig.update_yaxes(title_text="Brake (%)", row=2, col=1)
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/throttle_brake_analysis.html"
            fig.write_html(filename)
            print(f"✅ Throttle/Brake analysis saved as {filename}")
        
        return fig
    
    def create_speed_delta_plot(self, save_html=True):
        """
        Create speed delta plot showing where each driver is faster.
        """
        if not self.analyzer.driver1_data or not self.analyzer.driver2_data:
            print("❌ No driver data available for plotting")
            return None
        
        tel1 = self.analyzer.driver1_data['telemetry']
        tel2 = self.analyzer.driver2_data['telemetry']
        
        # Interpolate to common distance points
        min_distance = max(tel1['Distance'].min(), tel2['Distance'].min())
        max_distance = min(tel1['Distance'].max(), tel2['Distance'].max())
        common_distance = np.linspace(min_distance, max_distance, 500)
        
        speed1_interp = np.interp(common_distance, tel1['Distance'], tel1['Speed'])
        speed2_interp = np.interp(common_distance, tel2['Distance'], tel2['Speed'])
        
        speed_delta = speed1_interp - speed2_interp
        
        fig = go.Figure()
        
        # Positive delta (driver1 faster)
        positive_mask = speed_delta >= 0
        fig.add_trace(go.Scatter(
            x=common_distance[positive_mask],
            y=speed_delta[positive_mask],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(0, 255, 0, 0.3)',
            line=dict(color='green', width=2),
            name=f'{self.analyzer.driver1_data["driver"]} faster',
            hovertemplate='Distance: %{x}m<br>Speed advantage: +%{y:.1f} km/h<extra></extra>'
        ))
        
        # Negative delta (driver2 faster)
        negative_mask = speed_delta < 0
        fig.add_trace(go.Scatter(
            x=common_distance[negative_mask],
            y=speed_delta[negative_mask],
            mode='lines',
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.3)',
            line=dict(color='red', width=2),
            name=f'{self.analyzer.driver2_data["driver"]} faster',
            hovertemplate='Distance: %{x}m<br>Speed advantage: %{y:.1f} km/h<extra></extra>'
        ))
        
        # Add zero line
        fig.add_hline(y=0, line_dash="dash", line_color="black", opacity=0.5)
        
        fig.update_layout(
            title=f'Speed Delta: {self.analyzer.driver1_data["driver"]} vs {self.analyzer.driver2_data["driver"]}',
            xaxis_title='Distance (m)',
            yaxis_title='Speed Delta (km/h)',
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/speed_delta.html"
            fig.write_html(filename)
            print(f"✅ Speed delta plot saved as {filename}")
        
        return fig
    
    def create_comprehensive_dashboard(self, save_html=True):
        """
        Create a comprehensive dashboard with multiple visualizations.
        """
        if not self.analyzer.driver1_data or not self.analyzer.driver2_data:
            print("❌ No driver data available for plotting")
            return None
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Speed vs Distance',
                'Track Position with Speed',
                'Throttle Application',
                'Gear Usage',
                'RPM Comparison',
                'Brake Points'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.08
        )
        
        # Get data
        tel1 = self.analyzer.driver1_data['telemetry']
        tel2 = self.analyzer.driver2_data['telemetry']
        
        # 1. Speed vs Distance
        fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['Speed'], 
                                name=f"{self.analyzer.driver1_data['driver']} Speed",
                                line=dict(width=2)), row=1, col=1)
        fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['Speed'], 
                                name=f"{self.analyzer.driver2_data['driver']} Speed",
                                line=dict(width=2)), row=1, col=1)
        
        # 2. Track Position
        fig.add_trace(go.Scatter(x=tel1['X'], y=tel1['Y'], mode='lines',
                                name=f"{self.analyzer.driver1_data['driver']} Track",
                                line=dict(width=3)), row=1, col=2)
        fig.add_trace(go.Scatter(x=tel2['X'], y=tel2['Y'], mode='lines',
                                name=f"{self.analyzer.driver2_data['driver']} Track",
                                line=dict(width=3, dash='dash')), row=1, col=2)
        
        # 3. Throttle
        fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['Throttle'],
                                name=f"{self.analyzer.driver1_data['driver']} Throttle",
                                line=dict(width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['Throttle'],
                                name=f"{self.analyzer.driver2_data['driver']} Throttle",
                                line=dict(width=2)), row=2, col=1)
        
        # 4. Gear Usage
        fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['nGear'],
                                name=f"{self.analyzer.driver1_data['driver']} Gear",
                                mode='lines+markers', line=dict(width=2)), row=2, col=2)
        fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['nGear'],
                                name=f"{self.analyzer.driver2_data['driver']} Gear",
                                mode='lines+markers', line=dict(width=2)), row=2, col=2)
        
        # 5. RPM
        fig.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['RPM'],
                                name=f"{self.analyzer.driver1_data['driver']} RPM",
                                line=dict(width=2)), row=3, col=1)
        fig.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['RPM'],
                                name=f"{self.analyzer.driver2_data['driver']} RPM",
                                line=dict(width=2)), row=3, col=1)
        
        # 6. Brake Points
        brake1 = tel1['Brake'].astype(int) * 100
        brake2 = tel2['Brake'].astype(int) * 100
        fig.add_trace(go.Scatter(x=tel1['Distance'], y=brake1,
                                name=f"{self.analyzer.driver1_data['driver']} Brake",
                                line=dict(width=2)), row=3, col=2)
        fig.add_trace(go.Scatter(x=tel2['Distance'], y=brake2,
                                name=f"{self.analyzer.driver2_data['driver']} Brake",
                                line=dict(width=2)), row=3, col=2)
        
        # Update layout
        fig.update_layout(
            title=f'F1 Telemetry Dashboard: {self.analyzer.driver1_data["driver"]} vs {self.analyzer.driver2_data["driver"]}',
            template='plotly_white',
            height=1200,
            showlegend=True
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Distance (m)", row=1, col=1)
        fig.update_xaxes(title_text="X Position (m)", row=1, col=2)
        fig.update_xaxes(title_text="Distance (m)", row=2, col=1)
        fig.update_xaxes(title_text="Distance (m)", row=2, col=2)
        fig.update_xaxes(title_text="Distance (m)", row=3, col=1)
        fig.update_xaxes(title_text="Distance (m)", row=3, col=2)
        
        fig.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
        fig.update_yaxes(title_text="Y Position (m)", row=1, col=2)
        fig.update_yaxes(title_text="Throttle (%)", row=2, col=1)
        fig.update_yaxes(title_text="Gear", row=2, col=2)
        fig.update_yaxes(title_text="RPM", row=3, col=1)
        fig.update_yaxes(title_text="Brake (%)", row=3, col=2)
        
        fig.show()
        
        if save_html:
            filename = f"{self.output_dir}/comprehensive_dashboard.html"
            fig.write_html(filename)
            print(f"✅ Comprehensive dashboard saved as {filename}")
        
        return fig
    
    def generate_all_visualizations(self):
        """
        Generate all available visualizations.
        """
        print(f"\n📈 Generating Advanced F1 Visualizations...")
        print(f"Output directory: {self.output_dir}")
        print("=" * 60)
        
        self.create_speed_distance_plot()
        self.create_track_position_plot()
        self.create_gear_heatmap()
        self.create_throttle_brake_analysis()
        self.create_speed_delta_plot()
        self.create_comprehensive_dashboard()
        
        print("\n" + "=" * 60)
        print("✅ All visualizations generated successfully!")
        print(f"\nCheck the '{self.output_dir}' folder for interactive HTML files.")
        print("Open any .html file in your web browser for interactive exploration.")

