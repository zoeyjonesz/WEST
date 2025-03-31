class GasSystem:
    
    # range for max pressure = 2.3 highest (I kind of forgot the values)
    # 0.75 -> 1.3 = moderate 
    # 1.3 -> 2.3 = high 
    # 0 -> 0.75 = low 
    
    # modeling the following condition
    # Recycle Tank – Moderate Pressure
    # BTA – Low Pressure
    # BTB – High Pressure

    
    def __init__(self, recycling_volume, bta_volume, btb_volume):
        # Tank Pressure 
        self.recycling_volume = 1.0  # starting pressure moderate
        self.bta_volume = 0.5        # starting low
        self.btb_volume = 1.3        # starting high
        
        self.compressor_speed = 50  # curr compressor speed (will need to determin)
        self.valve_BA = 0           # 0 = closed, 100 = fully open
        self.valve_BB = 100 
        
        # bounds 
        self.lowest_compressor_speed = 80 
        self.max_compressor_speed = 400
        self.max_buffer_valve_flow = 0.5        # max outflow when buffer valve is fully open
        self.max_recycle_valve_flow = 0.231     # max outflow when compressor speed is at it's highest
        self.time_stamp = 0
        
        # flow rates
        self.bta_input = 0
        self.btb_input = 0
        self.recycle_input = 0
    
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
         
    
    # function to parse excel files 
    # Note: in main function will have to add line counter to the equation
    # Note: also not very efficient to always open excel file
    def parse_data(self):
        
        df = pd.read_excel("Flow_Test_Updated.xlsx", sheet_name="Input Flows")
        # print(df.head())
        row = df.iloc[line_counter]

        # pull row information & save to variables
        self.recycle_input = row['Recycle Tank Input']
        self.bta_input = row['BTA Input']
        self.btb_input = row['BTB Input']
    
    
        
    def control_loop(self): 
                    
        # logic open valve BA to release pressure
        if self.valve_BB != 0: 
            self.valve_BB = 0
                
        # logic close valv BB to increase pressure
        if self.valve_BB != 100: 
            self.valve_BB = 100
            
        # take the derivative 
        original_pressure = self.recycling_pressure
            
        
        # simulating the volume change in tanks over 10 seconds 
        for _ in range(10): 
            
            # recycle tank will turn high and will have to deal with that ?
            # read row data from excel 
            parse_data()

            # update tank volume 
            update_volumes(recycling_volume, bta_volume, btb_volume)

            # increment time stamp 
            self.time_stamp += 1
        
        # classify tank volumes for each tank 
        # Note: E a more efficient way to do this but for leave as is 
        classify_volume(self, recycling_volume)
        classify_volume(self, bta_volume)
        classify_volume(self, btb_volume)
        
        
        # actually waiting 10 seconds so it's realistic 
        wait(10)
                
            
        # calculate the difference
        derivative = self.recycling_pressure - original_pressure 

        if derivative > 0: 
            # simulate 10 seconds
            for _ in range(10): 
                self.update_pressure()

        # if the buffer tank is not filling up fast enough 
        elif derivative <= 0 and self.compressor_speed > self.lowest_compressor_speed + 10: 
            self.compressor_speed -= 10 
     
        
    def run_simulation(self, max_steps=100): 
            
        for t in range(max_steps):
            if not (self.recycling_volume == "moderate" and self.bta_volume == "low" and self.btb_volume == "high"):
                print(f"recycle pressure: {self.recycling_volume}")
                print(f"bta pressure: {self.bta_volume}")
                print(f"btb pressure: {self.btb_volume}")
                print(f"Condition has changed at time {t} Stopping simulation")
                break
                
            print(f"Time {t}, Pressure: {self.recycling_volume:.2f}, Compressor: {self.compressor_speed}, BA: {self.bta_volume}, BB: {self.btb_volume}")
            self.control_loop()
        
            
# call the system 
system = GasSystem()
system.run_simulation()
