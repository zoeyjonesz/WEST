import time
import pandas as pd
from system import System 
from sensor_data import parse_input

# Define constants for system settings
FILE_PATH = 'non-variable-input-flows.xlsx'

# Valve positions (%)
FULLY_OPEN = 100
FULLY_CLOSED = 0

# Compressor speed settings (%)
SPEED_INCREMENT = 5

# Valve settings for tanks
BTA_VALVE_INITIAL = 50
BTB_VALVE_INITIAL = 50

# Sleep duration between checks
SLEEP_DURATION = 10

def main():
    """Main function to simulate the system's operation using the System class."""
    # Initialize the system with initial volumes and valve positions
    system = System(
        recycling_volume = 3.5,
        bta_volume = 2.0,
        btb_volume = 2.0,
        compressor_speed = 50,
        valve_BA = BTA_VALVE_INITIAL,
        valve_BB = BTB_VALVE_INITIAL
    )

    # Simulating sensor data reading from an Excel file
    flowrates = parse_input(FILE_PATH)

    # Main loop: Continue operation while conditions hold
    while (system.volume_threshold('recycling') == 'MOD' and
           system.volume_threshold('bta') == 'LO' and
           system.volume_threshold('btb') == 'HI'):
        # Check the BTB valve and make sure it is fully open because the tank is full
        if system.valve_BB != FULLY_OPEN:
            system.adjust_valve_position('BB', FULLY_OPEN)

        if system.compressor_speed < (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)
       
        # Check the BTA valve and make sure it is fully closed because the tank is low
        if system.valve_BA != FULLY_CLOSED:
            system.adjust_valve_position('BA', FULLY_CLOSED)

        # Store the initial pressure for change tracking
        original_recycle_volume = system.recycling_volume

        # Wait for the pressure to change
        time.sleep(SLEEP_DURATION)
        # ADD EXCEL READING HERE, UPDATING TANKS

        # Simulate pressure changes (replace this with actual sensor data later)
        volume_change = system.recycle_volume - original_recycle_volume

        # Check whether the pressure is decreasing (ideal scenario)
        if volume_change < 0:
            time.sleep(SLEEP_DURATION)
            # ADD EXCEL READING HERE, UPDATING TANKS

        
        # Pressure is increasing, try to adjust the compressor speed using class methods
        elif volume_change >= 0 and system.compressor_speed <= (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)
            print(f"Compressor speed increased to {system.compressor_speed}%")

if __name__ == "__main__":
    main()