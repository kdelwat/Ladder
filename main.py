import remi.gui as gui
from remi import start, App

class LadderApp(App):
    
    def __init__(self, *args):
        super(LadderApp, self).__init__(*args)
       
    def main(self):
        self.container = gui.VBox(width=400, height=400)
        
        self.editable_table(['Name', 'Strength'])
        
        return self.container
    
    def editable_table(self, team_parameters):
        '''Builds editable table for team settings, with columns specified in the team_parameters list.'''

        # Create and initialise table
        self.teams_table = gui.Table(width=200, height=200, margin='10px')
        self.teams_table.from_2d_matrix([team_parameters])

        # Create function buttons and add callbacks
        self.add_row = gui.Button('Add row')
        self.add_row.set_on_click_listener(self, 'add_table_row')
           
        # Add widgets to main container
        self.container.append(self.teams_table)
        self.container.append(self.add_row)

    def add_table_row(self):
        '''Adds row (in the form of a list) to the end of the editable team table.'''
        
        row_parameters = ['Team Cool', '5']
        
        row = gui.TableRow()
        
        for item in row_parameters:
            row.append(gui.TableItem(item))
        
        self.teams_table.append(row)
        

start(LadderApp, address='0.0.0.0', debug=True, start_browser=False)