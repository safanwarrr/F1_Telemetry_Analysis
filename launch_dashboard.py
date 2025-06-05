#!/usr/bin/env python3
"""
F1 Dashboard Launcher

Simple script to launch the F1 Interactive Dashboard with proper setup.
"""

import subprocess
import sys
import webbrowser
import time
import os
from f1_dashboard_config import DASHBOARD_PORT, DASHBOARD_HOST

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['dash', 'plotly', 'fastf1', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def launch_dashboard():
    """Launch the F1 dashboard."""
    if not check_dependencies():
        return
    
    print("🏁 F1 Telemetry Dashboard Launcher")
    print("=" * 50)
    print(f"Starting dashboard on http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
    print()
    print("Features:")
    print("• Interactive telemetry analysis")
    print("• Real-time chart updates")
    print("• Multiple visualization types")
    print("• Driver and lap filtering")
    print("• Professional F1 data insights")
    print()
    print("Instructions:")
    print("1. Select year, race, and session")
    print("2. Click 'Load Session' to fetch data")
    print("3. Choose drivers to compare")
    print("4. Select chart types to explore")
    print("5. Use filters for detailed analysis")
    print()
    print("Press Ctrl+C to stop the dashboard")
    print("=" * 50)
    
    # Ask if user wants to auto-open browser
    try:
        auto_open = input("Open dashboard in browser automatically? (y/n): ").lower().strip()
        if auto_open in ['y', 'yes', '']:
            # Delay to ensure server starts
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
            
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
    except KeyboardInterrupt:
        print("\nStarting dashboard...")
    
    # Import and run the dashboard
    try:
        from f1_dashboard import app
        print(f"\n🌐 Dashboard available at: http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
        app.run(debug=False, host=DASHBOARD_HOST, port=DASHBOARD_PORT)
    except ImportError as e:
        print(f"❌ Error importing dashboard: {e}")
        print("Make sure f1_dashboard.py is in the current directory")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")

if __name__ == '__main__':
    try:
        launch_dashboard()
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

