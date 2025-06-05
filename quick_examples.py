#!/usr/bin/env python3
"""
Quick F1 Analysis Examples

Run this file to see some pre-configured interesting comparisons.
"""

from f1_telemetry_analysis import F1TelemetryAnalyzer

def example_championship_battle():
    """Compare championship contenders at a high-speed circuit."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Championship Battle - Verstappen vs Norris at Monza")
    print("=" * 60)
    
    analyzer = F1TelemetryAnalyzer()
    
    if analyzer.load_session(2024, "Italy", "Q"):
        if analyzer.compare_drivers("VER", "NOR"):
            summary = analyzer.get_comparison_summary()
            print(f"\n🏆 Faster: {summary['faster_driver']}")
            print(f"⏱️  Gap: {abs(summary['time_difference_seconds']):.3f}s")
            analyzer.save_data("monza_ver_vs_nor.csv")

def example_teammates():
    """Compare teammates at a technical circuit."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Teammate Battle - Hamilton vs Russell at Hungary")
    print("=" * 60)
    
    analyzer = F1TelemetryAnalyzer()
    
    if analyzer.load_session(2024, "Hungary", "Q"):
        if analyzer.compare_drivers("HAM", "RUS"):
            summary = analyzer.get_comparison_summary()
            print(f"\n🏆 Faster: {summary['faster_driver']}")
            print(f"⏱️  Gap: {abs(summary['time_difference_seconds']):.3f}s")
            analyzer.save_data("hungary_ham_vs_rus.csv")

def example_different_teams():
    """Compare drivers from different teams at Monaco."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Cross-Team Battle - Leclerc vs Piastri at Monaco")
    print("=" * 60)
    
    analyzer = F1TelemetryAnalyzer()
    
    if analyzer.load_session(2024, "Monaco", "Q"):
        if analyzer.compare_drivers("LEC", "PIA"):
            summary = analyzer.get_comparison_summary()
            print(f"\n🏆 Faster: {summary['faster_driver']}")
            print(f"⏱️  Gap: {abs(summary['time_difference_seconds']):.3f}s")
            analyzer.save_data("monaco_lec_vs_pia.csv")

def run_all_examples():
    """Run all example comparisons."""
    print("F1 Telemetry Analysis - Quick Examples")
    print("=====================================")
    print("\nThis will run several interesting driver comparisons...")
    
    try:
        example_championship_battle()
        example_teammates() 
        example_different_teams()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed!")
        print("=" * 60)
        print("\nCheck the generated CSV files for detailed telemetry data.")
        print("\nTo run your own custom analysis:")
        print("1. Edit f1_config.py with your desired race/drivers")
        print("2. Run: python3 run_f1_analysis.py")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nThis might happen if:")
        print("- You don't have internet connection")
        print("- The race data isn't available")
        print("- Driver codes are incorrect")

if __name__ == "__main__":
    run_all_examples()

