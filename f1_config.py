#!/usr/bin/env python3
"""
F1 Analysis Configuration

Modify this file to change which race, session, and drivers you want to analyze.
"""

# =============================================================================
# CONFIGURATION - MODIFY THESE VALUES
# =============================================================================

# Race Configuration
YEAR = 2024
RACE = "Monaco"  # Examples: "Monaco", "Silverstone", "Spa", "Monza", "Singapore", etc.
SESSION = "Q"    # "Q" for Qualifying, "R" for Race, "FP1", "FP2", "FP3" for practice

# Driver Configuration (use 3-letter driver codes)
DRIVER1 = "VER"  # Max Verstappen
DRIVER2 = "LEC"  # Charles Leclerc

# Output Configuration
SAVE_CSV = True          # Save telemetry data to CSV
SAVE_PLOTS = True        # Save plots as PNG files
SHOW_PLOTS = True        # Display plots on screen

# =============================================================================
# COMMON DRIVER CODES FOR REFERENCE
# =============================================================================
"""
Common F1 Driver Codes (2024 season):

Red Bull Racing:
- VER: Max Verstappen
- PER: Sergio Perez

Ferrari:
- LEC: Charles Leclerc
- SAI: Carlos Sainz

Mercedes:
- HAM: Lewis Hamilton
- RUS: George Russell

McLaren:
- NOR: Lando Norris
- PIA: Oscar Piastri

Aston Martin:
- ALO: Fernando Alonso
- STR: Lance Stroll

Alpine:
- OCO: Esteban Ocon
- GAS: Pierre Gasly

Williams:
- ALB: Alexander Albon
- SAR: Logan Sargeant

AlphaTauri/RB:
- TSU: Yuki Tsunoda
- RIC: Daniel Ricciardo

Alfa Romeo/Kick Sauber:
- BOT: Valtteri Bottas
- ZHO: Zhou Guanyu

Haas:
- MAG: Kevin Magnussen
- HUL: Nico Hulkenberg
"""

# =============================================================================
# RACE EXAMPLES
# =============================================================================
"""
Popular races to analyze:

- "Bahrain"      - Season opener, good for car comparison
- "Monaco"       - Street circuit, low speeds, precision driving
- "Canada"       - Mix of straights and tight corners
- "Silverstone"  - High-speed British GP
- "Hungary"      - Tight, twisty circuit
- "Spa"          - High-speed with elevation changes
- "Monza"        - Temple of speed, slipstream battles
- "Singapore"    - Night street race
- "Japan"        - Technical Suzuka circuit
- "United States" - Circuit of the Americas
- "Brazil"       - Wet weather and drama
- "Abu Dhabi"    - Season finale
"""

