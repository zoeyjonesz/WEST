import pandas as pd
import time

# Define a constant for pressure calculation (adjust based on your system)
C = 100  # This constant should be determined based on your system's parameters (for illustration)

def calculate_pressure(flowrate):
    """Calculate pressure based on flow rate (simple inverse relation)."""
    if flowrate == 0:
        return float('inf')  # No flow, infinite pressure (adjust as needed)
    else:
        return C / flowrate

def main():
    # Replace with the actual path to your Excel file
    file_path = 'sensor_data.xlsx'

    # Read the necessary columns (TIME, SEC 1, SEC 2, SEC 3, SEC R)
# Try to read the Excel file
    try:
        df = pd.read_excel(file_path, usecols=["TIME", "SEC 1", "Flowrate 1", "SEC 2", "Flowrate 2", "SEC 3", "Flowrate 3", "SEC R", "Flowrate R"])
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
    
    # Loop through the data rows and calculate pressure for each vessel
    for index, row in df.iterrows():
        # Extract flowrates and vessel types
        sec_1_vessel = row['SEC 1']
        sec_1_flowrate = row['Flowrate 1']

        sec_2_vessel = row['SEC 2']
        sec_2_flowrate = row['Flowrate 2']

        sec_3_vessel = row['SEC 3']
        sec_3_flowrate = row['Flowrate 3']

        sec_r_vessel = row['SEC R']
        sec_r_flowrate = row['Flowrate R']

        # Calculate pressure for each vessel using flowrate
        sec_1_pressure = calculate_pressure(sec_1_flowrate)
        sec_2_pressure = calculate_pressure(sec_2_flowrate)
        sec_3_pressure = calculate_pressure(sec_3_flowrate)
        sec_r_pressure = calculate_pressure(sec_r_flowrate)

        # Print results for this time step
        print(f"Time: {row['TIME']}")
        print(f"Sec 1 {sec_1_vessel} Pressure: {sec_1_pressure:.2f} (Flowrate: {sec_1_flowrate})")
        print(f"Sec 2 {sec_2_vessel} Pressure: {sec_2_pressure:.2f} (Flowrate: {sec_2_flowrate})")
        print(f"Sec 3 {sec_3_vessel} Pressure: {sec_3_pressure:.2f} (Flowrate: {sec_3_flowrate})")
        print(f"Sec R {sec_r_vessel} Pressure: {sec_r_pressure:.2f} (Flowrate: {sec_r_flowrate})")
        print("-" * 40)

        # Simulate waiting for the next set of data (e.g., 1 second delay)
        time.sleep(1)

if __name__ == "__main__":
    main()
