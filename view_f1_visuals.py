#!/usr/bin/env python3
"""
F1 Visualization Viewer

This script helps you open and view the generated F1 visualizations.
"""

import os
import webbrowser
import sys

def list_visualizations():
    """List all available visualizations."""
    vis_dir = "f1_visualizations"
    
    if not os.path.exists(vis_dir):
        print("❌ No visualizations found. Please run the analysis first.")
        return []
    
    html_files = [f for f in os.listdir(vis_dir) if f.endswith('.html')]
    
    if not html_files:
        print("❌ No HTML visualizations found.")
        return []
    
    return html_files

def open_visualization(filename):
    """Open a specific visualization in the browser."""
    filepath = os.path.abspath(os.path.join("f1_visualizations", filename))
    
    if os.path.exists(filepath):
        webbrowser.open(f"file://{filepath}")
        print(f"🌐 Opening {filename} in your default browser...")
    else:
        print(f"❌ File not found: {filename}")

def main():
    print("F1 Visualization Viewer")
    print("=" * 40)
    
    # List available visualizations
    html_files = list_visualizations()
    
    if not html_files:
        return
    
    print("\nAvailable visualizations:")
    for i, filename in enumerate(html_files, 1):
        # Make filename more readable
        display_name = filename.replace('.html', '').replace('_', ' ').title()
        print(f"{i:2d}. {display_name}")
    
    print(f"{len(html_files) + 1:2d}. Open All")
    print(f"{len(html_files) + 2:2d}. Exit")
    
    while True:
        try:
            choice = input("\nSelect visualization to open (number): ")
            choice_num = int(choice)
            
            if choice_num == len(html_files) + 2:  # Exit
                print("👋 Goodbye!")
                break
            elif choice_num == len(html_files) + 1:  # Open all
                print("🌐 Opening all visualizations...")
                for filename in html_files:
                    open_visualization(filename)
                break
            elif 1 <= choice_num <= len(html_files):
                selected_file = html_files[choice_num - 1]
                open_visualization(selected_file)
                break
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()

