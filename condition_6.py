import time 
import pandas as pd


def main():

  # Hard coding values just to have these variables in the code
  file_path = 'Sensor_Data.xlsx'
  current_index = 0

  high = 8
  moderate = 6
  low = 3
  
  recycle_pressure = moderate
  bta_pressure = low
  btb_pressure = high
  bta_valve = 50
  btb_valve = 50
  fully_open = 100
  fully_closed = 0
  compressor_speed = 100
  highest_speed = 100

  while recycle_pressure == moderate and bta_pressure == low and btb_pressure == high:
    if btb_valve != fully_open:
      btb_valve = fully_open

    if compressor_speed < (highest_speed - 5):
      compressor_speed = (compressor_speed + 5)

    if bta_valve != fully_closed:
      bta_valve = fully_closed

    # Original pressure in the recycle tank before changes are made
    original_recycle_pressure = recycle_pressure

    # Waiting for pressure to change in the recycle tank, add reading through 10 seconds of the spreadsheet
    time.sleep(10) 

    # Finding the change in pressure in the recycle tank
    pressure_change = recycle_pressure - original_recycle_pressure 

    # Check whether the pressure is decreasing in the recycle tank (which is ideal)
    if pressure_change < 0: 
      # Continue from were we were in the spreadsheet
      time.sleep(10)
               
    # Pressure is increasing in the recycle tank (this is not ideal)          
    elif pressure_change >= 0 and compressor_speed <= (highest_speed - 5): 
      # If possible, increase the compressor speed
      compressor_speed = compressor_speed + 5 

            
if __name__ =="__main__":
  main()
