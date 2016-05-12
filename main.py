import remi.gui as gui
from remi import start, App

import ladder
import sports

class LadderApp(App):
    
    def __init__(self, *args):
        super(LadderApp, self).__init__(*args)
       
    def main(self):
        self.base_width = 400
        self.element_height = 20
        self.side_padding = 50
        
        self.container = gui.VBox(width=self.base_width + 2 * self.side_padding,
                                  height=400)
        
        self.error_message = gui.Label('')
        self.container.append(self.error_message)
        
        # Begin first stage (sport selection)
        self.sport_select()
        
        return self.container

    def stage_2(self):
        '''Called by the next button in stage 1, initialise team table.'''
        parameters = self.sport['parameters']
        self.editable_table(parameters)

    def sport_select(self):
        '''Builds sport selection area.'''
        
        label = gui.Label('Select sport to simulate:')

        # Load sports from library specification.
        self.available_sports = sports.games
        
        self.sport_dropdown = gui.DropDown(width=self.base_width, height=self.element_height)
        self.sport_dropdown.set_on_change_listener(self, 'set_sport')

        # Loop through sports and add to dropdown        
        for sport in self.available_sports:
            self.sport_dropdown.append(gui.DropDownItem(sport, width=self.base_width, height=self.element_height))
        
        # Set default sport
        first_sport = list(self.available_sports.keys())[0]
        self.sport_dropdown.set_value(first_sport)
        self.sport = self.available_sports[first_sport]
        
        # Create button to finalise selection
        next_button = gui.Button('Next')
        next_button.set_on_click_listener(self, 'stage_2')
                
        sport_select_container = gui.HBox(width=self.base_width, height=self.element_height)
        sport_select_container.append(label)
        sport_select_container.append(self.sport_dropdown)
        sport_select_container.append(next_button)
                
        self.container.append(sport_select_container)
    
    def set_sport(self, value):
        '''On change in dropdown selection, set new selected sport.'''
        self.sport = self.available_sports[value]
    
    def editable_table(self, team_parameters):
        '''Builds editable table for team settings, with columns specified in the team_parameters list.'''

        # Create and initialise table, where:
        #   self.teams_table is the GUI element
        #   self.teams is the data element for later processing
        self.teams_table_height = self.element_height
        self.teams_table_entries = 0
        self.teams_table = gui.Table(width=self.base_width,
                                     height=self.teams_table_height,
                                     margin='10px')
        self.teams_table.from_2d_matrix([team_parameters])
        self.teams = [team_parameters]
        
        # Create editable row
        self.new_row = gui.TextInput(width=self.base_width, height=self.element_height)
        self.new_row.set_text('Input new row here with fields seperated by commas')
        self.new_row.set_on_change_listener(self, 'edit_table_row')
        
        # Create function buttons and add callbacks, inside a HBox container
        buttons = gui.HBox(width=self.base_width, height=self.element_height)
        
        self.add_row = gui.Button('Add row')
        self.add_row.set_on_click_listener(self, 'add_table_row')
        buttons.append(self.add_row)
        
        self.delete_row = gui.Button('Delete row')
        self.delete_row.set_on_click_listener(self, 'delete_table_row')
        buttons.append(self.delete_row)
           
        # Add widgets to main container
        self.container.append(self.teams_table)
        self.container.append(self.new_row)
        self.container.append(buttons)
        
        self.simulate = gui.Button('Simulate')
        self.simulate.set_on_click_listener(self, 'store_teams')
        self.container.append(self.simulate)
        
    def store_teams(self):
        ladder.add_teams(self.teams)
        ladder.simple_simulate(game=self.sport)
       
    def add_table_row(self):
        '''Adds row (from the input text area) to the end of the editable team 
        table.'''
        
        # Ensure there is new data to be added
        try:
            row_parameters = self.new_team_parameters
        except AttributeError:
            self.display_error('No new data inputted!')
        
        # Create TableRow by iterating through new parameters
        row = gui.TableRow()
        raw_row = []
        for item in row_parameters:
            row.append(gui.TableItem(item))
            raw_row.append(item)
        
        # Add row to table, assigning it a new ID, and adjust table height to
        # fit new row
        self.teams_table_entries += 1
        self.teams_table.append(row, key=str(self.teams_table_entries))
        self.teams.append(raw_row)

        self.teams_table_height += self.element_height
        self.teams_table.set_size(self.base_width, self.teams_table_height)

    def delete_table_row(self):
        '''Deletes last row in teams table.'''
        
        # Ensure that there are rows to delete
        if self.teams_table_entries > 0:
        
            # Get the last row as an object and decrement the last ID
            last_row = self.teams_table.get_child(str(self.teams_table_entries))
            self.teams_table_entries -= 1
            
            # Delete the last row
            self.teams_table.remove_child(last_row)
            self.teams.pop()
        else:
            self.display_error('No rows to delete!')
        
    def edit_table_row(self, value):
        '''As table input area is edited, split the text on the comma character
        and assign it to the parameters variable for adding as row.'''
        self.new_team_parameters = value.split(',')
    
    def display_error(self, message):
        self.error_message.set_text(message)

start(LadderApp, address='0.0.0.0', debug=True, start_browser=False)