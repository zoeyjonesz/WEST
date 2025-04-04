import time
import pandas as pd
from system import System 
from sensor_data import parse_input

# Define constants for system settings
FILE_PATH = 'non-variable-input-flows.xlsx'

# Valve positions (%)
FULLY_OPEN = 1
FULLY_CLOSED = 0

# Compressor speed settings (%)
SPEED_INCREMENT = 20

# Valve settings for tanks
BTA_VALVE_INITIAL = 0.5
BTB_VALVE_INITIAL = 0.5

def main():
    """Main function to simulate the system's operation using the System class."""
    # Initialize the system with initial volumes and valve positions
    system = System(
        recycling_volume = 0,
        bta_volume = 0,
        btb_volume = 0,
        recycling_pressure = 2,
        bta_pressure = 0.5,
        btb_pressure = 2,
        compressor_speed = 100,
        valve_BA = BTA_VALVE_INITIAL,
        valve_BB = BTB_VALVE_INITIAL
    )

    # Simulating sensor data reading from an Excel file
    flowrates = parse_input(FILE_PATH)
    flow_rate_index = 1

    system.update_volume()

    # Main loop: Continue operation while conditions hold
    while (system.pressure_threshold('recycling') == 'MOD' and
           system.pressure_threshold('bta') == 'LO' and
           system.pressure_threshold('btb') == 'HI'):
        # Check the BTB valve and make sure it is fully open because the tank is full
        if system.valve_BB != FULLY_OPEN:
            system.adjust_valve_position('BB', FULLY_OPEN)

        if system.compressor_speed < (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)
       
        # Check the BTA valve and make sure it is fully closed because the tank is low
        if system.valve_BA != FULLY_CLOSED:
            system.adjust_valve_position('BA', FULLY_CLOSED)

        # Store the initial pressure for change tracking
        original_recycle_pressure = system.recycling_pressure

        # Wait for the pressure to change
        system.changes_in_tanks(flowrates, flow_rate_index)
        flow_rate_index += 10

        # Simulate pressure changes (replace this with actual sensor data later)
        recycle_pressure_change = system.recycling_pressure - original_recycle_pressure

        # Check whether the pressure is decreasing (ideal scenario)
        if recycle_pressure_change < 0:
            print(f"Ideal: Recycle tank pressure decreased by {abs(recycle_pressure_change)} units.")
            system.changes_in_tanks(flowrates, flow_rate_index)
            flow_rate_index += 10

        # Pressure is increasing, try to adjust the compressor speed using class methods
        elif recycle_pressure_change >= 0 and system.compressor_speed <= (system.max_compressor_speed - SPEED_INCREMENT):
            print(f"Not ideal: Pressure increased by {abs(recycle_pressure_change)} units.")
            system.adjust_compressor_speed(SPEED_INCREMENT)
            print(f"Compressor speed increased to {system.compressor_speed}%")

        print(f"Post Loop Pressure Condtions:") 
        print(f"Recycling Tank: {system.pressure_threshold('recycling')}")
        print(f"BTA Tank: {system.pressure_threshold('bta')}")
        print(f"BTB Tank: {system.pressure_threshold('btb')}")

if __name__ == "__main__":
    main()