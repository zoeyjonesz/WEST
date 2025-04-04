from sensor_data import parse_input
from sensor_data import input_flowrate
import pandas as pd
import time

class System:

    def __init__(self, recycling_volume, bta_volume, btb_volume, 
                 recycling_pressure, bta_pressure, btb_pressure, 
                 compressor_speed, valve_BA, valve_BB):
        # Initial Tank Volumes 
        self.recycling_volume = recycling_volume 
        self.bta_volume = bta_volume               
        self.btb_volume = btb_volume  

        # Initial Tank Pressures
        self.recycling_pressure = recycling_pressure
        self.bta_pressure = bta_pressure
        self.btb_pressure = btb_pressure
        
        self.compressor_speed = compressor_speed 
        self.valve_BA = valve_BA          
        self.valve_BB = valve_BB   

        # Predefined limits for compressor speed and valve flow rates      
        self.lowest_compressor_speed = 80
        self.max_compressor_speed = 400
        self.max_buffer_valve_flow = 0.29      
        self.max_recycle_valve_flow = 0.231 
        self.temperature = 298

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
                self.update_pressure()
            else:
                print(f"Error: Cannot exceed max recycling volume of {self.max_recycling_volume}.")
        
        elif volume_type == "bta":
            if self.bta_volume + amount <= self.max_bta_volume:
                self.bta_volume += amount
                self.update_pressure()
            else:
                print(f"Error: Cannot exceed max bta volume of {self.max_bta_volume}.")
        
        elif volume_type == "btb":
            if self.btb_volume + amount <= self.max_btb_volume:
                self.btb_volume += amount
                self.update_pressure()
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
            recycle_output = self.max_recycle_valve_flow * (self.compressor_speed/self.max_compressor_speed)
            if self.recycling_volume - recycle_output >= 0:
                self.recycling_volume -= recycle_output 
                self.update_pressure()
            else:
                print("Error: Cannot remove more volume than the current amount in 'recycling'.")
            
        elif volume_type == "bta":
            if self.valve_BA == 0:
                print("'bta' valve closed.")
            elif self.bta_volume - self.max_buffer_valve_flow >= 0:
                self.bta_volume -= self.max_buffer_valve_flow
                self.update_pressure()
                self.add_volume('recycling', self.max_buffer_valve_flow)
            else:
                print("Error: Cannot remove more volume than the current amount in 'bta'.")
            
        elif volume_type == "btb":
            if self.valve_BB == 0:
                print("'btb' valve closed.")
            elif self.btb_volume - self.max_buffer_valve_flow >= 0:
                self.btb_volume -= self.max_buffer_valve_flow
                self.update_pressure()
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



    def pressure_threshold(self, tank_type):
        '''
        Determine the volume threshold for a specified tank.
        
        Parameters:
        tank_type (str): Type of tank ('recycling', 'bta', 'btb').
        
        Returns:
        str: Volume status ('LO', 'MOD', 'HI', 'HIHI').
        '''
        if tank_type == 'recycling':
            if self.recycling_pressure <= 0.0 and self.recycling_pressure >= -2:
                return 'LO'
            elif self.recycling_pressure <= 3:
                return 'MOD'
            elif self.recycling_pressure <= 3:
                return 'HI'
            else:
                return 'Out of pressure range: {self.recycling_pressure} psi'
        
        elif tank_type in ['bta', 'btb']:
            pressure = self.bta_pressure if tank_type == 'bta' else self.btb_pressure
            if pressure <= 1.5 and pressure >= 0:
                return 'LO'
            elif pressure <= 3:
                return 'HI'
            else:
                return 'HIHI'
        else:
            return 'Out of pressure range: {self.bta_pressure} psi' if tank_type == 'bta' else 'Out of pressure range: {self.btb_pressure} psi'


    def update_pressure(self) -> None:
        """
        Calculate pressure based on Pressure = Density * Gas Constant * Temperature / Volume.

        Parameters:
        - None (uses internal tank values).

        Returns:
        None (modifies the object's state directly).
        """
        methane_density = 0.675
        # Calculate pressure using the ideal gas law
        recycling_pressure = methane_density * 8.314 * self.temperature / self.recycling_volume
        bta_pressure = methane_density * 8.314 * self.temperature / self.bta_volume
        btb_pressure = methane_density * 8.314 * self.temperature / self.btb_volume

        # Convert pressure from Pa to psi (1 Pa = 0 .0001450377377 psi)
        self.recycling_pressure = recycling_pressure * 0.0001450377377    
        self.bta_pressure = bta_pressure * 0.0001450377377  
        self.btb_pressure = btb_pressure * 0.0001450377377


    def update_volume(self) -> None:
        """
        Update the volume of the tanks based Volume = Density * Gas Constant * Temperature / Pressure.

        Parameters:
        - None (uses internal tank values).

        Returns:
        None (modifies the object's state directly).
        """
        # Convert psi to Pa (1 psi = 6894.76 Pa)
        recycling_pressure = self.recycling_pressure * 6894.76
        bta_pressure = self.bta_pressure * 6894.76
        btb_pressure = self.btb_pressure * 6894.76

        methane_density = 0.675
        
        self.recycling_volume = (methane_density * 8.314 * self.temperature) / recycling_pressure
        self.bta_volume = (methane_density * 8.314 * self.temperature) / bta_pressure
        self.btb_volume = (methane_density * 8.314 * self.temperature) / btb_pressure


    def equalize_pressure(self, P1, P2, V1, V2) -> float:
        """
        Equalize the pressure between the two tanks.

        Parameters:
        - P1 (float): The current pressure in tank one (in psi).
        - P2 (float): The current pressure in tank two (in psi).
        - V1 (float): The volume of tank one (in m³).
        - V2 (float): The volume of tank two (in m³).

        Returns:
        - float: Equalized pressure (in psi).
        """
        # Convert psi to absolute pressure
        abs_P1 = P1 + 14.696
        abs_P2 = P2 + 14.696 

        # Apply Boyle's Law to calculate the equalized pressure
        abs_equalized_pressure = (abs_P1 * V1 + abs_P2 * V2) / (V1 + V2)

        # Convert back to gauge pressure
        equalized_pressure = abs_equalized_pressure - 14.696
    
        return equalized_pressure


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
            print(f"Updated pressures: Recycling: {self.recycling_pressure} psi, BTA: {self.bta_pressure} psi, BTB: {self.btb_pressure} psi")

            # NO ERROR HANDLING HERE, SHOULD CONSIDER ADDING IT
            # Add a delay to simulate time passing
            time.sleep(1)

