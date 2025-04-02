from sensor_data import parse_input
from sensor_data import input_flowrate
import pandas as pd
import time

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
        self.lowest_compressor_speed = 80
        self.max_compressor_speed = 400
        self.max_buffer_valve_flow = 0.1      # changed from 0.5 to 0.1 
        self.max_recycle_valve_flow = 0.6 

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


    def remove_volume(self, volume_type)-> None:
        '''
        Removes volume from the specified tank type, ensuring the volume doesn't become negative.

        Parameters:
        volume_type (str): Type of tank ('recycling', 'bta', 'btb').

        Returns:
        None (modifies the object's state directly). 
        '''
        if volume_type == "recycling":
            if self.recycling_volume - (self.max_recycle_valve_flow * (self.compressor_speed/self.max_compressor_speed)) >= 0:
                self.recycling_volume -= (self.max_recycle_valve_flow *(self.compressor_speed/self.max_compressor_speed)) 
            else:
                print("Error: Cannot remove more volume than the current amount in 'recycling'.")
            
        elif volume_type == "bta":
            if self.valve_BA == 0:
                print("'bta' valve closed.")
            elif self.bta_volume - self.max_buffer_valve_flow >= 0:
                self.bta_volume -= self.max_buffer_valve_flow
                self.add_volume('recycling', self.max_buffer_valve_flow)
            else:
                print("Error: Cannot remove more volume than the current amount in 'bta'.")
            
        elif volume_type == "btb":
            if self.valve_BB == 0:
                print("'btb' valve closed.")
            elif self.btb_volume - self.max_buffer_valve_flow >= 0:
                self.btb_volume -= self.max_buffer_valve_flow
                self.add_volume('recycling', self.max_buffer_valve_flow)
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


    def adjust_valve_position(self, valve_name: str, target_position: int):
        """
        Adjust the specified valve position to a target.

        Parameters:
        valve_name (str): Name of the valve ('BA' or 'BB').
        target_position (int): Desired valve position (0 to 100%).

        Returns:
        None (modifies the object's state directly).
        """
        if valve_name == 'BA':
            if self.valve_BA != target_position:
                self.valve_BA = target_position
        elif valve_name == 'BB':
            if self.valve_BB != target_position:
                self.valve_BB = target_position
        else:
            print("Error: Invalid valve name. Use 'BA' or 'BB'.")



    def volume_threshold(self, tank_type):
        '''
        Determine the volume threshold for a specified tank.
        
        Parameters:
        tank_type (str): Type of tank ('recycling', 'bta', 'btb').
        
        Returns:
        str: Volume status ('LO', 'MOD', 'HI', 'HIHI').
        '''
        if tank_type == 'recycling':
            if self.recycling_volume <= 2.0:
                return 'LO'
            elif self.recycling_volume <= 4.5:
                return 'MOD'
            elif self.recycling_volume <= 6.5:
                return 'HI'
            else:
                return 'HIHI'
        
        elif tank_type in ['bta', 'btb']:
            volume = self.bta_volume if tank_type == 'bta' else self.btb_volume
            if volume <= 1.1:
                return 'LO'
            elif volume < 2.3:
                return 'HI'
            else:
                return 'HIHI'
        else:
            return 'Invalid tank type'
            

    def changes_in_tanks(self, df, index:int):
        """
        Update the tank volumes based on flow rates for 10 iterations starting from the specified index.

        Parameters:
        df (dataframe): Excel spreadsheet dataframe containing flow rates.
        index (int): The current place in the spreadsheet.

        Returns:
        None (modifies the object's state directly).
        
        """
        for i in range(index, index + 10):  # Loop 10 times from the specified index
            recycle_flowrate, bta_flowrate, btb_flowrate, time_value = input_flowrate(df, i)
        
            if recycle_flowrate is not None:
                self.add_volume('recycling', recycle_flowrate)
            if bta_flowrate is not None:
                self.add_volume('bta', bta_flowrate)
            if btb_flowrate is not None:
                self.add_volume('btb', btb_flowrate)

            self.remove_volume('recycling')
            self.remove_volume('bta')
            self.remove_volume('btb')
            print(f"Updated volumes: Recycling: {self.recycling_volume}, BTA: {self.bta_volume}, BTB: {self.btb_volume}")
            # NO ERROR HANDLING HERE, SHOULD CONSIDER ADDING IT
            # Add a delay to simulate time passing
        time.sleep(10)

