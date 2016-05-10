import remi.gui as gui
from remi import start, App

import ladder

class LadderApp(App):
    
    def __init__(self, *args):
        super(LadderApp, self).__init__(*args)
       
    def main(self):
        self.container = gui.VBox(width=400, height=400)
        
        self.error_message = gui.Label('')
        self.container.append(self.error_message)
        
        self.editable_table(['Name', 'Strength'])
        
        return self.container
    
    def editable_table(self, team_parameters):
        '''Builds editable table for team settings, with columns specified in the team_parameters list.'''

        # Create and initialise table, where:
        #   self.teams_table is the GUI element
        #   self.teams is the data element for later processing
        self.teams_table_height = 20
        self.teams_table_entries = 0
        self.teams_table = gui.Table(width=200,
                                     height=self.teams_table_height,
                                     margin='10px')
        self.teams_table.from_2d_matrix([team_parameters])
        self.teams = [team_parameters]
        
        # Create editable row
        self.new_row = gui.TextInput(width=200, height=20)
        self.new_row.set_text('Input new row here with fields seperated by commas')
        self.new_row.set_on_change_listener(self, 'edit_table_row')
        
        # Create function buttons and add callbacks, inside a HBox container
        buttons = gui.HBox(width=200, height=20)
        
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
        ladder.simple_simulate()
       
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

        self.teams_table_height += 20
        self.teams_table.set_size(200, self.teams_table_height)

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