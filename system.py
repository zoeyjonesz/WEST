class System:

    def __init__(self, recycling_volume, bta_volume, btb_volume, compressor_speed, valve_BA, valve_BB):
        # Initial Tank Volumes 
        self.recycling_volume = recycling_volume 
        self.bta_volume = bta_volume               
        self.btb_volume = btb_volume    
        
        self.compressor_speed = compressor_speed 
        self.valve_BA = valve_BA          
        self.valve_BB = valve_BB   

        # Predefined limits for compressor speed and valve flow rates      
        self.lowest_compressor_speed = 30
        self.max_compressor_speed = 50
        self.max_valve_flow = 5

    def add_volume(self, volume_type, amount: int):
        '''
        Adds volume to the specified tank type.

        Parameters:
        volume_type (str): Type of tank ('recycling', 'bta', 'btb').
        amount (int): Amount of volume to add.

        Returns:
        None (modifies the object's state directly). 
        '''
        if volume_type == "recycling":
            self.recycling_volume += amount
        elif volume_type == "bta":
            self.bta_volume += amount
        elif volume_type == "btb":
            self.btb_volume += amount
        else:
            print("Invalid volume type. Please use 'recycling', 'bta', or 'btb'.")       
