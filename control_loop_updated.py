import time 
import pandas as pd 

# can I use backflow to 

class GasSystem:
    
    # range for max pressure = 2.3 highest (I kind of forgot the values)
    # 0.75 -> 1.3 = moderate 
    # 1.3 -> 2.3 = high 
    # 0 -> 0.75 = low 
    
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
        self.compressor_speed = 50
        self.valve_BA = 50
        self.valve_BB = 50

        # System Limits
        self.lowest_compressor_speed = 80
        self.max_compressor_speed = 400
        self.max_buffer_valve_flow = 0.5
        self.max_recycle_valve_flow = 0.231


        # Flow rates (updated from Excel)
        self.bta_input = 0
        self.btb_input = 0
        self.recycle_input = 0
        self.line_counter = 0

        self.data = pd.read_excel("Flow_Test_Updated.xlsx", sheet_name="Input Flows")
        
        
    # function to parse data in excel files 
    def parse_data(self):
        
        if self.line_counter < len(self.data):
            row = df.iloc[self.line_counter]
            
            # pull row information & save to variables
            self.recycle_input = row['Recycle Tank Input']
            self.bta_input = row['BTA Input']
            self.btb_input = row['BTB Input']
            
            print(f"Recycle: {self.recycle_input}, BTA: {self.bta_input}, BTB: {self.btb_input}")
            
            # increment time stamp 
            self.line_counter += 1
        else: 
            print("End of data.")

    
    
    # function to classify pressure 
    def classify_volume(self, volume):
        if 0 <= volume < 0.75:
            return "low"
        elif 0.75 <= volume < 1.3:
            return "moderate"
        elif 1.3 <= volume <= 2.3:
            return "high"
        else:
            return "out of range"
    
    
    # update tank volumes 
    def update_volumes(self): 
        
        if self.recycling_volume is not None:
            self.recycling_volume = self.recycle_input + self.recycling_volume - ((self.compressor_speed/ self.max_compressor_speed) * self.max_recycle_valve_flow)
            
        if self.bta_volume is not None:
            self.bta_volume = self.bta_input + self.bta_volume - (self.max_buffer_valve_flow  * (self.valve_BA/100))
            
        if self.btb_volume is not None:
            self.btb_volume = self.btb_input + self.btb_volume - (self.max_buffer_valve_flow  * (self.valve_BB/100))
    
    
    # adjust the volume in BA
    def adjust_BA(self): 
        bta_status = self.classify_volume(self.bta_volume)
        recycle_status = self.classify_volume(self.recycling_volume)
        
        if self.bta_volume > self.recycling_volume:
            
            # working with simplified conditions for now
            if bta_status == "high": 
                self.valve_BA = 100     # open bta valve 100 %
            elif bta_status == "low": 
                self.valve_BA = 0
        else: 
            print("Closing valve B: Buffer too low to flow")
            self.valve_BA = 0
            
            
            
    # adjust the volume in BB
    def adjust_BB(self): 
        btb_status = self.classify_volume(self.btb_volume)
        recycle_status = self.classify_volume(self.recycling_volume)
        
        if self.btb_volume > self.recycling_volume:
            
            # working with simplified conditions for now 
            if btb_status == "high": 
                self.valve_BB = 100     # open bta valve 100 %
            elif btb_status == "low": 
                self.valve_BB = 0
        else: 
            print("Closing valve B: Buffer too low to flow")
            self.valve_BB = 0
                   
                
                
    # adjust volume in recycle compressor 
    def adjust_recycle(self): 
        recycle_status = self.classify_volume(self.recycling_volume)
        
        if recycle_status == "low": 
            self.compressor_speed = max(self.compressor_speed - 10, self.lowest_compressor_speed)
            print("Recycle low → Decreasing compressor speed")
        elif recycle_status == "high": 
            self.compressor_speed = min(self.compressor_speed + 10, self.max_compressor_speed)
            print("Recycle high → Increase compressor speed")
        
        
        
    def control_loop(self): 
            
        # take the derivative 
        original_pressure = self.recycling_volume
            
        
        # simulating the volume change in tanks over 10 seconds 
        for _ in range(10): 
            
            self.parse_data()       # read row data from excel 
            self.update_volumes()   # update tank volume 
            
            # apply logic here NOTE might change this 
            self.adjust_recycle()
            self.adjust_BA()
            self.adjust_BB()
            
            self.line_counter += 1
            print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # sleep 10 seconds  
        time.sleep(10)
                
            
        # calculate the difference
        derivative = self.recycling_volume - original_pressure 

        # derivative < 0 pressure is decreasing in recycle tank
        if derivative < 0: 
            print("Recycle tank volume decreasing. Holding pressure.")
            
            # simulating the volume change in tanks over 10 seconds 
            for _ in range(10): 
      
                self.parse_data()
                self.update_volumes()   # update tank volume 
                # apply logic here NOTE might change this 
                self.adjust_recycle()
                self.adjust_BA()
                self.adjust_BB()
                
                self.line_counter += 1
                print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # actually waiting 10 seconds so it's realistic 
        time.sleep(10)

        
        if derivative >= 0 and self.compressor_speed <= self.max_compressor_speed - 10: 
            print("Recycle tank stable or rising. Increasing compressor speed to maintain.")
            self.compressor_speed += 5
            
            # Note decided if I want to update compressor speed here right away 
     
      
        
    
    def run_simulation(self, max_steps=100):
        
        for t in range(max_steps):
            recycle_status = self.classify_volume(self.recycling_volume)
            bta_status = self.classify_volume(self.bta_volume)
            btb_status = self.classify_volume(self.btb_volume)
            print(recycle_status)
            print(bta_status)
            print(btb_status)
            
            
            print(f"Recycle {t}: {recycle_status}, BTA: {bta_status}, BTB: {btb_status}")

            self.control_loop()
        
            
# call the system 
system = GasSystem()
system.run_simulation()
        
