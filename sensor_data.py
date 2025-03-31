import pandas as pd
import time

def parse_input(file_path):
    """Parse the input file to extract input flow rates."""
    try:
        df = pd.read_excel(file_path, usecols=["Recycle Tank Input", "BTA Input", "BTB Input", "Time"])
        return df
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None
    

def input_flowrate(df, index: int):
    """Extract flowrate values from the dataframe."""
    try:
        recycle_flowrate = df.at[index, 'Recycle Tank Input']
        bta_flowrate = df.at[index, 'BTA Input']
        btb_flowrate = df.at[index, 'BTB Input']
        time_value = df.at[index, 'Time']
        return recycle_flowrate, bta_flowrate, btb_flowrate, time_value
    except KeyError as e:
        print(f"Error: Missing column in the dataframe - {e}")
        return None
    
   # need to determine the output of a tank still, def output_flowrate():
