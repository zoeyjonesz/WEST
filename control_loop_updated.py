class GasSystem:
    
    # range for max pressure = 2.3 highest 
    # 0.75 -> 1.3 = moderate 
    # 1.3 -> 2.3 = high 
    # 0 -> 0.75 = low 
    
    # Recycle Tank – Moderate Pressure
    # BTA – Low Pressure
    # BTB – High Pressure

    
    def __init__(self, recycling_volume, bta_volume, btb_volume):
        # Tank Pressure 
        self.recycling_volume = 1.0  # starting pressure moderate
        self.bta_volume = 0.5        # starting low
        self.btb_volume = 1.3        # starting high
        
        self.compressor_speed = 50  # arbitrary unit
        self.valve_BA = 0           # 0 = closed, 100 = fully open
        self.valve_BB = 100         
        self.lowest_compressor_speed = 30
        self.max_compressor_speed = 50
        self.max_valve_flow = 5        # max rate when valve is fully open
    
    
    # function to classify pressure 
    def classify_volume(self, volume):
        if 0 <= pressure < 0.75:
            return "low"
        elif 0.75 <= pressure < 1.3:
            return "moderate"
        elif 1.3 <= pressure <= 2.3:
            return "high"
        else:
            return "out of range"
    
    # update tank volumes 
    def update_volumes(self, recycling_volume=None, bta_volume=None, btb_volume=None): 
        
        if recycling_volume is not None:
            self.recycling_volume = recycling_volume
        if bta_volume is not None:
            self.bta_volume = bta_volume
        if btb_volume is not None:
            self.btb_volume = btb_volume
         
        
        

    def control_loop(self): 
                    
        # logic open valve BA to release pressure
        if self.valve_BA != 100: 
            self.valve_BA = 100
            
            
        # logic slow compressor speed 
        if self.compressor_speed > self.compressor_speed + 10: 
            self.compressor_speed -= 10 
                
                
        # logic close valv BB to increase pressure
        if self.valve_BB != 0: 
            self.valve_BB = 0
                
                
        # take the derivative 
        original_pressure = self.recycling_pressure
            
        # simulate 10 seconds -> update pressure 
        for _ in range(10): 
            self.update_pressure()
                
            
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
            if not (self.calc_recycle_pressure() == "low" and self.calc_bta_pressure() == "high" and self.calc_btb_pressure() == "low"):
                print(f"recycle pressure: {self.calc_recycle_pressure()}")
                print(f"bta pressure: {self.calc_bta_pressure()}")
                print(f"btb pressure: {self.calc_bta_pressure()}")
                print(f"Condition has changed at time {t} Stopping simulation")
                break
                
            print(f"Time {t}, Pressure: {self.recycling_pressure:.2f}, Compressor: {self.compressor_speed}, BA: {self.bta_pressure}, BB: {self.btb_pressure}")
            self.control_loop()
        
            
# call the system 
system = GasSystem()
system.run_simulation()
