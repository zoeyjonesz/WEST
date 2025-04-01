class GasSystem:
    
    # range for max pressure = 2.3 highest (I kind of forgot the values)
    # 0.75 -> 1.3 = moderate 
    # 1.3 -> 2.3 = high 
    # 0 -> 0.75 = low 
    
    # modeling the following condition
    # Recycle Tank – Moderate Pressure
    # BTA – Low Pressure
    # BTB – High Pressure

    
    def __init__(self, recycling_volume=1.0, bta_volume=0.5, btb_volume=1.3):
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
    def update_volumes(self, recycling_volume=None, bta_volume=None, btb_volume=None): 
        
        if recycling_volume is not None:
            self.recycling_volume = recycle_input + recycling_volume - ((compressor_speed/max_compressor_speed) * max_recycle_valve_flow)
            
        if bta_volume is not None:
            self.bta_volume = bta_input + bta_volume - (self.max_buffer_valve_flow  * (valve_BA/100))
            
        if btb_volume is not None:
            self.btb_volume = btb_input + btb_volume - (self.max_buffer_valve_flow  * (valve_BB/100))
         
    
        
    def control_loop(self): 
                    
        # logic open valve BA to release pressure
        if self.valve_BB != 0: 
            self.valve_BB = 0
                
        # logic close valv BB to increase pressure
        if self.valve_BB != 100: 
            self.valve_BB = 100
            
        # take the derivative 
        original_pressure = self.recycling_volume
            
        
        # simulating the volume change in tanks over 10 seconds 
        for _ in range(10): 
            # read row data from excel 
            self.parse_data()
            # update tank volume 
            self.update_volumes()
            self.line_counter += 1
            print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # actually waiting 10 seconds so it's realistic 
        time.sleep(10)
                
            
        # calculate the difference
        derivative = self.recycling_volume - original_pressure 

        # derivative < 0 pressure is decreasing in recycle tank
        if derivative < 0: 
            print("Recycle tank volume decreasing. Holding pressure.")
            
            # simulating the volume change in tanks over 10 seconds 
            for _ in range(10): 
            # read row data from excel 
                self.parse_data()
                # update tank volume 
                self.update_volumes()
                self.line_counter += 1
                print(f"[t={self.line_counter}] Recycle: {self.recycling_volume:.3f}, BTA: {self.bta_volume:.3f}, BTB: {self.btb_volume:.3f}, Speed: {self.compressor_speed}, BA: {self.valve_BA}, BB: {self.valve_BB}")

        # actually waiting 10 seconds so it's realistic 
        time.sleep(10)

        
        if derivative >= 0 and self.compressor_speed <= self.max_compressor_speed - 10: 
            print("Recycle tank stable or rising. Increasing compressor speed.")
            self.compressor_speed += 10 
     
      
        
    
    def run_simulation(self, max_steps=100):
        
        for t in range(max_steps):
            recycle_status = self.classify_volume(self.recycling_volume)
            bta_status = self.classify_volume(self.bta_volume)
            btb_status = self.classify_volume(self.btb_volume)
            
            
            if recycle_status != "moderate" or bta_status != "low" or btb_status != "high":
                print(f"\nCondition changed at t={t}.\nRecycle: {recycle_status}, BTA: {bta_status}, BTB: {btb_status}")
                break

            self.control_loop()
        
            
# call the system 
system = GasSystem()
system.run_simulation()
