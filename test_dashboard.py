#!/usr/bin/env python3
"""
F1 Dashboard Test

Test script to verify dashboard components work correctly.
"""

import sys
try:
    import dash
    from dash import dcc, html
    import plotly.graph_objects as go
    import fastf1
    import pandas as pd
    import numpy as np
    print("✅ All required packages imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_fastf1_basic():
    """Test basic FastF1 functionality."""
    try:
        # Test cache setup
        import os
        cache_dir = 'f1_cache'
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        fastf1.Cache.enable_cache(cache_dir)
        print("✅ FastF1 cache setup successful")
        return True
    except Exception as e:
        print(f"❌ FastF1 setup error: {e}")
        return False

def test_plotly_chart():
    """Test basic Plotly chart creation."""
    try:
        # Create a simple test chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], name='Test'))
        fig.update_layout(title="Test Chart")
        print("✅ Plotly chart creation successful")
        return True
    except Exception as e:
        print(f"❌ Plotly chart error: {e}")
        return False

def test_dash_components():
    """Test Dash component creation."""
    try:
        # Create basic Dash components
        dropdown = dcc.Dropdown(
            options=[{'label': 'Test', 'value': 'test'}],
            value='test'
        )
        
        layout = html.Div([
            html.H1("Test Dashboard"),
            dropdown,
            dcc.Graph(figure=go.Figure())
        ])
        
        print("✅ Dash components creation successful")
        return True
    except Exception as e:
        print(f"❌ Dash components error: {e}")
        return False

def main():
    print("🏁 F1 Dashboard Test Suite")
    print("=" * 40)
    
    tests = [
        ("FastF1 Setup", test_fastf1_basic),
        ("Plotly Charts", test_plotly_chart),
        ("Dash Components", test_dash_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Dashboard should work correctly.")
        print("\nTo start the dashboard:")
        print("python3 f1_dashboard.py")
        print("\nOr use the launcher:")
        print("python3 launch_dashboard.py")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        print("\nTry installing missing packages:")
        print("pip install dash plotly fastf1 pandas numpy")

if __name__ == '__main__':
    main()

