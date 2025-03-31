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

         # Max volumes for tanks
        self.max_recycling_volume = 7
        self.max_bta_volume = 2.5
        self.max_btb_volume = 2.5

    def add_volume(self, volume_type, amount: int) -> None:
        '''
        Adds volume to the specified tank type.

        Parameters:
        volume_type (str): Type of tank ('recycling', 'bta', 'btb').
        amount (int): Amount of volume to add.

        Returns:
        None (modifies the object's state directly). 
        '''
        if volume_type == "recycling":
            if self.recycling_volume + amount <= self.max_recycling_volume:
                self.recycling_volume += amount
            else:
                print(f"Error: Cannot exceed max recycling volume of {self.max_recycling_volume}.")
        
        elif volume_type == "bta":
            if self.bta_volume + amount <= self.max_bta_volume:
                self.bta_volume += amount
            else:
                print(f"Error: Cannot exceed max bta volume of {self.max_bta_volume}.")
        
        elif volume_type == "btb":
            if self.btb_volume + amount <= self.max_btb_volume:
                self.btb_volume += amount
            else:
                print(f"Error: Cannot exceed max btb volume of {self.max_btb_volume}.")
        
        else:
            print("Invalid volume type. Please use 'recycling', 'bta', or 'btb'.")


    def remove_volume(self, volume_type, amount: int)-> None:
        '''
        Removes volume from the specified tank type, ensuring the volume doesn't become negative.

        Parameters:
        volume_type (str): Type of tank ('recycling', 'bta', 'btb').
        amount (int): Amount of volume to remove.

        Returns:
        None (modifies the object's state directly). 
        '''
        if volume_type == "recycling":
            if self.recycling_volume - amount >= 0:
                self.recycling_volume -= amount
            else:
                print("Error: Cannot remove more volume than the current amount in 'recycling'.")
            
        elif volume_type == "bta":
            if self.bta_volume - amount >= 0:
                self.bta_volume -= amount
            else:
                print("Error: Cannot remove more volume than the current amount in 'bta'.")
            
        elif volume_type == "btb":
            if self.btb_volume - amount >= 0:
                self.btb_volume -= amount
            else:
                print("Error: Cannot remove more volume than the current amount in 'btb'.")
            
        else:
            print("Invalid volume type. Please use 'recycling', 'bta', or 'btb'.")


    def adjust_compressor_speed(self, speed_increment: int) -> None:
        """ 
        Increase the compressor speed by a fixed increment.
           
        Parameters:
        speed_increment (int): The amount to change the compressor speed by. 

        Returns:
        None (modifies the object's state directly). 
        
        """
        if self.compressor_speed < (self.max_compressor_speed - speed_increment):
            self.compressor_speed += speed_increment