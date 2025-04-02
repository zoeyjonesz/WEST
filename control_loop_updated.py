import time 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class GasSystem:
    
    # buffer cubic meter range - max capacity 2.5 cubic m
    # low = 0.0 -0.7
    # moderate = 0.7-1.5
    # high = 1.5 - 2.3 
    # hihi = 2.3 -2.5
    # since no moderate in buffer tank: low - 0.0 - 1.5
    
    # recycle 
    # low = 0.0 - 0.2
    # moderate = 2 - 4.5
    # high = 4.5 - 6.5
    # hihi = 6.5 - 7
    
    # modeling the following condition 3
    # Recycle Tank – Low
    # BTA – High
    # BTB – Low

    
    def __init__(self, recycling_volume=0.5, bta_volume=1.5, btb_volume=0.6):
        # Tank Volumes
        self.recycling_volume = recycling_volume
        self.bta_volume = bta_volume
        self.btb_volume = btb_volume

        # Control Parameters - Note: Problem where do we start? 
        self.compressor_speed = 80
        self.valve_BA = 50
        self.valve_BB = 50

        # System Limits
        self.lowest_compressor_speed = 80
        self.max_compressor_speed = 400
        self.max_buffer_valve_flow = 0.05
        self.max_recycle_valve_flow = 0.231


        # Flow rates (updated from Excel)
        self.bta_input = 0
        self.btb_input = 0
        self.recycle_input = 0
        self.line_counter = 0
        self.time = 0
        
        # history
        self.time_history = []
        self.recycle_history = []
        self.bta_history = []
        self.btb_history = []


        self.data = pd.read_excel("Flow_Test_Updated.xlsx", sheet_name="Input Flows")
        
        
    # function to parse data in excel files 
    def parse_data(self):
        
        if self.line_counter < len(self.data):
            row = df.iloc[self.line_counter]
            
            # pull row information & save to variables
            self.time = pd.to_datetime(row['Time'], format="%H:%M:%S")
            self.recycle_input = row['Recycle Tank Input']
            self.bta_input = row['BTA Input']
            self.btb_input = row['BTB Input']
            
            print(f"Time: {self.time}:  Recycle: {self.recycle_input}, BTA: {self.bta_input}, BTB: {self.btb_input}")
            
            # increment time stamp 
            self.line_counter += 1
        else: 
            print("End of data.")

    
    
    def classify_buffer_volume(self, volume):
        if 0 <= volume < 1.5:
            return "low"
        elif 1.5 <= volume <= 2.3:
            return "high"
        elif 2.3 <= volume <= 2.5:
            return "hihi"
        else: 
            return "Error Pressure is out of range"
            
   
    def classify_recycle_volume(self, volume):
        if 0 <= volume < 2.0:
            return "low"
        elif 2.0 <= volume <= 4.5:
            return "moderate"
        elif 4.5 <= volume <= 6.5:
            return "high"
        elif 6.5 <= volume <= 7.0: 
            return "hihi"
        else: 
            return "Error Pressure is out of range"
    
    
    # update tank volumes 
    def update_volumes(self): 
        
        if self.recycling_volume is not None:
            self.recycling_volume = self.recycle_input + (self.max_buffer_valve_flow  * (self.valve_BA/100)) + (self.max_buffer_valve_flow  * (self.valve_BB/100))+ self.recycling_volume - ((self.compressor_speed/ self.max_compressor_speed) * self.max_recycle_valve_flow)
            print(f"Input: {self.recycle_input}")
            print(f"Buffer flow A: {(self.max_buffer_valve_flow  * (self.valve_BA/100))}")
            print(f"Buffer flow B: {(self.max_buffer_valve_flow  * (self.valve_BB/100))}")

            print(f"Tank Volume: {self.recycling_volume}")
            print(f"Subtract: {(self.compressor_speed/ self.max_compressor_speed) * self.max_recycle_valve_flow}")
            
        if self.bta_volume is not None:
            self.bta_volume = self.bta_input + self.bta_volume - (self.max_buffer_valve_flow  * (self.valve_BA/100))
            print(f"BTA: {self.bta_volume}")
        if self.btb_volume is not None:
            self.btb_volume = self.btb_input + self.btb_volume - (self.max_buffer_valve_flow  * (self.valve_BB/100))
    
    
    # adjust the volume in BA
    def adjust_BA(self):
        
        bta_status = self.classify_buffer_volume(self.bta_volume)
        recycle_status = self.classify_recycle_volume(self.recycling_volume)
        
        if self.bta_input == 0 and bta_status == "low":
            self.valve_BA = 0
            return 
   
        if self.bta_volume > self.recycling_volume and recycle_status == "low":
            self.valve_BA = 100
            
        # Also allow flow if BTB is high and Recycle is moderate
        elif bta_status == "high" and recycle_status == "moderate":
            self.valve_BA = 100

        else:
            self.valve_BA = 0
                   
            
            
            
    # adjust the volume in BB
    def adjust_BB(self): 
        
        
        btb_status = self.classify_buffer_volume(self.btb_volume)
        recycle_status = self.classify_recycle_volume(self.recycling_volume)
        
        # if idle close valve
        if self.btb_input == 0 and btb_status == "low":
            self.valve_BB = 0
            return 
        
        if self.btb_volume > self.recycling_volume and recycle_status == "low":
            self.valve_BB = 100
            
        # Also allow flow if BTB is high and Recycle is moderate
        elif btb_status == "high" and recycle_status == "moderate":
            self.valve_BB = 100

        else:
            self.valve_BB = 0
                   
                
                
    # adjust volume in recycle compressor 
    def adjust_recycle(self): 
        recycle_status = self.classify_recycle_volume(self.recycling_volume)
        
        if recycle_status == "low": 
            self.compressor_speed = max(self.compressor_speed - 5, self.lowest_compressor_speed)
#             print("Recycle low → Decreasing compressor speed")
        elif recycle_status == "high": 
            self.compressor_speed = min(self.compressor_speed + 5, self.max_compressor_speed)
#             print("Recycle high → Increase compressor speed")
        
        
    def control_loop(self):
            
        # take the derivative 
        original_pressure = self.recycling_volume
            
        
        # simulating the volume change in tanks over 10 seconds 
        for _ in range(10): 
            
            self.parse_data()       # read row data from excel 
            
            # apply logic here NOTE location of these calls
            self.adjust_recycle()
            self.adjust_BA()
            self.adjust_BB()
            
            self.update_volumes()   # update tank volume 
            
            self.time_history.append(self.time)
            self.recycle_history.append(self.recycling_volume)
            self.bta_history.append(self.bta_volume)
            self.btb_history.append(self.btb_volume)

            
            self.line_counter += 1
#             print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # sleep 10 seconds  
        time.sleep(1)
                
            
        # calculate the difference
        derivative = self.recycling_volume - original_pressure 

        # derivative < 0 pressure is decreasing in recycle tank
        if derivative < 0: 
            
            print("Recycle tank volume decreasing. Holding pressure.")
            
            # simulating the volume change in tanks over 10 seconds 
            for _ in range(10): 
      
                self.parse_data()
                # apply logic here NOTE might change location of these calls 
                self.adjust_recycle()
                self.adjust_BA()
                self.adjust_BB()
                self.update_volumes()   # update tank volume 
                
                
                self.time_history.append(self.time)
                self.recycle_history.append(self.recycling_volume)
                self.bta_history.append(self.bta_volume)
                self.btb_history.append(self.btb_volume)

                
                self.line_counter += 1
#                 print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # actually waiting 10 seconds so it's realistic 
        time.sleep(1)

        
        if derivative >= 0 and self.compressor_speed <= self.max_compressor_speed - 10: 
#             print("Recycle tank stable or rising. Increasing compressor speed to maintain.")
            self.compressor_speed += 5
            
            # Note decided if I want to update compressor speed here right away 
     
      
        
    
    def run_simulation(self, max_steps=200):
        
        for t in range(max_steps):
            recycle_status = self.classify_recycle_volume(self.recycling_volume)
            bta_status = self.classify_buffer_volume(self.bta_volume)
            btb_status = self.classify_buffer_volume(self.btb_volume)
            
            print(f"Recycle {t}: {recycle_status}, BTA: {bta_status}, BTB: {btb_status}")

            self.control_loop()
        
            
# call the system 
system = GasSystem()
system.run_simulation()
