import time
import pandas as pd

# Define constants for system settings
FILE_PATH = 'Sensor_Data.xlsx'

# Pressure thresholds (in psi)
HIGH_PRESSURE = 8
MODERATE_PRESSURE = 6
LOW_PRESSURE = 3

# Valve positions (%)
FULLY_OPEN = 100
FULLY_CLOSED = 0

# Compressor speed settings (%)
MAX_COMPRESSOR_SPEED = 100
SPEED_INCREMENT = 5

# Valve settings for tanks
BTA_VALVE_INITIAL = 50
BTB_VALVE_INITIAL = 50

# Sleep duration between checks
SLEEP_DURATION = 10

def adjust_compressor_speed(current_speed: int) -> int:
    """Increase the compressor speed by a fixed increment."""
    if current_speed < (MAX_COMPRESSOR_SPEED - SPEED_INCREMENT):
        current_speed += SPEED_INCREMENT
    return current_speed

def adjust_valve_position(current_valve: int, target_position: int) -> int:
    """Adjust valve position to a target."""
    if current_valve != target_position:
        current_valve = target_position
    return current_valve

def main():
    """Main function to simulate the system's operation."""
    # Initialize system pressures and valves
    recycle_pressure = MODERATE_PRESSURE
    bta_pressure = LOW_PRESSURE
    btb_pressure = HIGH_PRESSURE

    bta_valve = BTA_VALVE_INITIAL
    btb_valve = BTB_VALVE_INITIAL
    compressor_speed = MAX_COMPRESSOR_SPEED

    # Main loop: Continue operation while certain conditions hold
    while recycle_pressure == MODERATE_PRESSURE and bta_pressure == LOW_PRESSURE and btb_pressure == HIGH_PRESSURE:
        # Adjust valves and compressor speed based on conditions
        btb_valve = adjust_valve_position(btb_valve, FULLY_OPEN)
        compressor_speed = adjust_compressor_speed(compressor_speed)
        bta_valve = adjust_valve_position(bta_valve, FULLY_CLOSED)

        # Store the initial pressure for change tracking
        original_recycle_pressure = recycle_pressure

        # Wait for the pressure to change
        time.sleep(SLEEP_DURATION)

        # Calculate the change in recycle tank pressure
        pressure_change = recycle_pressure - original_recycle_pressure

        # Check whether the pressure is decreasing (ideal scenario)
        if pressure_change < 0:
            time.sleep(SLEEP_DURATION)

        # Pressure is increasing, try to adjust the compressor speed
        elif pressure_change >= 0 and compressor_speed <= (MAX_COMPRESSOR_SPEED - SPEED_INCREMENT):
            compressor_speed = adjust_compressor_speed(compressor_speed)

if __name__ == "__main__":
    main()
