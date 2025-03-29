import time 

def main():
  recycle_pressure = "moderate"
  bta_pressure = "low"
  btb_pressure = "high"
  bta_valve = 50
  btb_valve = 50
  fully_open = 100
  fully_closed = 0
  compressor_speed 
  highest_speed = 100
  
  while recycle_pressure == "moderate" and bta_pressure == "low" and btb_pressure == "high":
    if btb_valve != fully_open:
      btb_valve = fully_open

    if compressor_speed < (highest_speed - 5):
      compressor_speed = (compressor_speed + 5)

    if bta_valve != fully_closed:
      bta_valve = fully_closed

    original_recycle_pressure = recycle_tank # this is the original pressure in the recycle tank

    time.sleep(10) # waiting for effects of changes made above in the pressure recycle tank 

    pressure_change = recycle_tank - original_recycle_pressure # current recycle pressure minus recycle pressure before changes were made

    if pressure_change < 0: # pressure is decreasing in the recycle tank, this is good

      time.sleep(10)
               
    elif pressure_change >= 0 and compressor_speed <= (highest_speed - 5) # pressure is increasing in recycle tank, this is bad
      compressor_speed = compressor_speed + 5 # increae compressor speed even more if possible 

            
if __name__ =="__main__":
  main()
