import remi.gui as gui
from remi import start, App

import ladder
import sports


class LadderApp(App):

    def __init__(self, *args):
        super(LadderApp, self).__init__(*args)

    def main(self):
        self.base_width = 500
        self.base_height = 200

        self.element_height = 20
        self.table_row_height = 20
        self.side_padding = 50

        self.container = gui.VBox(width=self.base_width + 2*self.side_padding,
                                  height=self.base_height)

        self.error_message = gui.Label('')
        self.container.append(self.error_message)

        # Begin first stage (sport selection)
        self.sport_select()

        return self.container

    def stage_2(self):
        '''Called by the next button in stage 1, initialise team table.'''
        parameters = self.sport['parameters']
        self.editable_table(parameters)

    def stage_3(self):
        '''Called by the next button in stage 2, initialise tournament
        settings.'''
        self.tournament_select()

        # Create button to advance to stage 4
        simulate_button = gui.Button('Simulate')
        simulate_button.set_on_click_listener(self, 'stage_4')
        self.container.append(simulate_button)

    def stage_4(self):
        '''Called by the next button in stage 3, run simulation.'''
        self.simulate()

    def sport_select(self):
        '''Builds sport selection area.'''

        label = gui.Label('Select sport to simulate:')

        # Load sports from library specification.
        self.available_sports = sports.games

        self.sport_dropdown = gui.DropDown(width=self.base_width,
                                           height=self.element_height)
        self.sport_dropdown.set_on_change_listener(self, 'set_sport')

        # Loop through sports and add to dropdown
        for sport in self.available_sports:
            self.sport_dropdown.append(gui.DropDownItem(sport,
                                       width=self.base_width,
                                       height=self.element_height))

        # Set default sport
        first_sport = list(self.available_sports.keys())[0]
        self.sport_dropdown.set_value(first_sport)
        self.sport = self.available_sports[first_sport]

        # Create button for settings and to finalise selection
        settings_button = gui.Button('Settings')
        settings_button.set_on_click_listener(self, 'sport_settings_dialog')
        next_button = gui.Button('Next')
        next_button.set_on_click_listener(self, 'stage_2')

        sport_select_container = gui.HBox(width=self.base_width,
                                          height=self.element_height)
        sport_select_container.append(label)
        sport_select_container.append(self.sport_dropdown)
        sport_select_container.append(settings_button)
        sport_select_container.append(next_button)

        # Add selection to main container and initialise settings panel
        self.container.append(sport_select_container)

    def set_sport(self, value):
        '''On change in dropdown selection, set new selected sport.'''
        self.sport = self.available_sports[value]

    def sport_settings_dialog(self):
        '''Build sport settings dialog.'''

        self.settings_dialog = gui.GenericDialog(title='Sport Settings',
                                                 width=self.base_width)

        # Get the settings dictionary of the currently selected sport. Loop
        # through the dictionary, creating text fields for each setting
        # populated with the default value and add each to the dialog with
        # the setting name as the unique identifier.
        for setting, default in self.sport['settings'].items():
            text_input = gui.TextInput(width=200)
            text_input.set_value(default)
            self.settings_dialog.add_field_with_label(setting, setting,
                                                      text_input)

        self.settings_dialog.set_on_confirm_dialog_listener(self,
            'sport_settings_dialog_confirm')
        self.settings_dialog.show(self)

    def sport_settings_dialog_confirm(self):
        '''When the sport settings dialog is accepted, sets the current sport's
        settings to the new values.'''

        new_settings = {}

        for setting in self.sport['settings']:
            value = self.settings_dialog.get_field(setting).get_value()
            new_settings[setting] = value

        self.sport['settings'] = new_settings

    def tournament_select(self):
        '''Builds tournament selection area.'''
        tournament_label = gui.Label('Tournament structure:')
        finals_label = gui.Label('Finals structure:')

        # Load structures from library specification.
        self.available_tournaments = ladder.tournament_structures
        self.available_finals = ladder.finals_structures

        self.tournament_dropdown = gui.DropDown(width=self.base_width,
                                                height=self.element_height)
        self.tournament_dropdown.set_on_change_listener(self, 'set_tournament')

        self.finals_dropdown = gui.DropDown(width=self.base_width,
                                            height=self.element_height)
        self.finals_dropdown.set_on_change_listener(self, 'set_finals')

        # Loop through tournaments and add to dropdown
        for tournament in self.available_tournaments:
            self.tournament_dropdown.append(gui.DropDownItem(tournament,
                                            width=self.base_width,
                                            height=self.element_height))

        for finals in self.available_finals:
            self.finals_dropdown.append(gui.DropDownItem(finals,
                                        width=self.base_width,
                                        height=self.element_height))

        # Set default tournament
        first_tournament = list(self.available_tournaments.keys())[0]
        self.tournament_dropdown.set_value(first_tournament)
        self.tournament = self.available_tournaments[first_tournament]

        first_finals = list(self.available_finals.keys())[0]
        self.finals_dropdown.set_value(first_finals)
        self.finals = self.available_finals[first_finals]

        # Create button for settings
        tournament_settings_button = gui.Button('Settings')
        tournament_settings_button.set_on_click_listener(self,
            'build_tournament_settings_dialog')

        finals_settings_button = gui.Button('Settings')
        finals_settings_button.set_on_click_listener(self,
            'build_finals_settings_dialog')

        tournament_select_container = gui.HBox(width=self.base_width,
                                               height=self.element_height)
        tournament_select_container.append(tournament_label)
        tournament_select_container.append(self.tournament_dropdown)
        tournament_select_container.append(tournament_settings_button)

        finals_select_container = gui.HBox(width=self.base_width,
                                           height=self.element_height)
        finals_select_container.append(finals_label)
        finals_select_container.append(self.finals_dropdown)
        finals_select_container.append(finals_settings_button)

        # Add selection to main container and initialise settings panel
        self.container.append(tournament_select_container)
        self.container.append(finals_select_container)

    def set_tournament(self, value):
        '''On change in dropdown selection, set new selected tournament.'''
        self.tournament = self.available_tournaments[value]

    def set_finals(self, value):
        '''On change in dropdown selection, set new selected finals.'''
        self.finals = self.available_finals[value]

    def build_tournament_settings_dialog(self):
        '''Build tournament settings dialog.'''

        self.tourn_set_dialog = gui.GenericDialog(title='Tournament Settings',
                                                  width=self.base_width)

        # Get the settings dictionary of the currently selected tournament.
        # Loop through the dictionary, creating text fields for each setting
        # populated with the default value and add each to the dialog with
        # the setting name as the unique identifier.
        for setting, default in self.tournament['settings'].items():
            text_input = gui.TextInput(width=200)
            text_input.set_value(default)
            self.tourn_set_dialog.add_field_with_label(setting, setting,
                                                       text_input)

        self.tourn_set_dialog.set_on_confirm_dialog_listener(self,                  'tourn_set_dialog_confirm')
        self.tourn_set_dialog.show(self)
 
    def tourn_set_dialog_confirm(self):
        '''When the tournament settings dialog is accepted, sets the
        tournament's settings to the new values.'''

        new_settings = {}

        for setting in self.tournament['settings']:
            value = self.tourn_set_dialog.get_field(setting).get_value()
            new_settings[setting] = value

        self.tournament['settings'] = new_settings

    def build_finals_settings_dialog(self):
        '''Build finals settings dialog.'''

        self.finals_settings_dialog = gui.GenericDialog(title='Finals Settings',
                                                        width=self.base_width)

        # Get the settings dictionary of the currently selected finals.
        # Loop through the dictionary, creating text fields for each setting
        # populated with the default value and add each to the dialog with
        # the setting name as the unique identifier.
        for setting, default in self.finals['settings'].items():
            text_input = gui.TextInput(width=200)
            text_input.set_value(default)
            self.finals_settings_dialog.add_field_with_label(setting, setting,
                                                             text_input)

        self.finals_settings_dialog.set_on_confirm_dialog_listener(self,            'finals_settings_dialog_confirm')
        self.finals_settings_dialog.show(self)

    def finals_settings_dialog_confirm(self):
        '''When the finals settings dialog is accepted, sets the finals'
        settings to the new values.'''

        new_settings = {}

        for setting in self.finals['settings']:
            value = self.finals_settings_dialog.get_field(setting).get_value()
            new_settings[setting] = value

        self.finals['settings'] = new_settings

    def editable_table(self, team_parameters, populate=False):
        '''Builds editable table for team settings, with columns specified in
        the team_parameters list.'''

        # Create and initialise table, where:
        #   self.teams_table is the GUI element
        #   self.teams is the data element for later processing
        self.teams_table_height = self.table_row_height
        self.teams_table_entries = 0
        self.teams_table = gui.Table(width=self.base_width,
                                     height=self.teams_table_height,
                                     margin='10px')

        # The populate variable may be a table array, in which case the table
        # is pre-populated
        if populate is not False:
            # Set internal teams structure to the whole populate array
            self.teams = populate

            # Set GUI table to the first row of the populate array, namely the
            # list of parameters.
            self.teams_table.from_2d_matrix([populate[0]])

            # Loop through remaining teams, building rows
            for team in populate[1:]:
                row = gui.TableRow()
                for item in team:
                    row.append(gui.TableItem(item))

                # Add row to table, assigning it a new ID
                self.teams_table_entries += 1
                self.teams_table.append(row, key=str(self.teams_table_entries))

            # Set table height correctly
            self.teams_table_height = len(populate) * self.table_row_height
        else:
            # Othwerwise, just create a table with the supplied parameters.
            self.teams_table.from_2d_matrix([team_parameters])
            self.teams = [team_parameters]

        # Create editable row
        self.new_row = gui.TextInput(width=self.base_width,
                                     height=self.table_row_height)
        self.new_row.set_text('Input new row here, fields seperated by commas')
        self.new_row.set_on_change_listener(self, 'edit_table_row')

        # Create function buttons and add callbacks, inside a HBox container
        buttons = gui.HBox(width=self.base_width, height=self.element_height)

        self.add_row = gui.Button('Add row')
        self.add_row.set_on_click_listener(self, 'add_table_row')
        buttons.append(self.add_row)

        self.delete_row = gui.Button('Delete row')
        self.delete_row.set_on_click_listener(self, 'delete_table_row')
        buttons.append(self.delete_row)

        self.load_teams = gui.Button('Load teams')
        self.load_teams.set_on_click_listener(self, 'load_table_file_select')
        buttons.append(self.load_teams)

        self.save_teams = gui.Button('Save teams')
        self.save_teams.set_on_click_listener(self, 'save_table_file_select')
        buttons.append(self.save_teams)

        # Add widgets to main container. Keys are specified to ensure that
        # the table is replaced in case of loading.
        self.container.append(self.teams_table, key='teams_table')
        self.container.append(self.new_row, key='new_row')
        self.container.append(buttons, key='buttons')

        # Create button to to advance to the next stage
        next_button = gui.Button('Next')
        next_button.set_on_click_listener(self, 'stage_3')

        self.container.append(next_button, key='next_button')

        # Set container and table height
        self.container.set_size(self.base_width + 2 * self.side_padding,
                                self.teams_table_height
                                + 4 * self.element_height
                                + self.base_height)
        self.teams_table.set_size(self.base_width, self.teams_table_height)

    def load_table_file_select(self):
        '''Open a file selection dialog to choose a team csv file
        to load.'''
        self.load_table_dialog = gui.FileSelectionDialog('Load Teams',
            'Select csv file to load',
            False, '.')

        self.load_table_dialog.set_on_confirm_value_listener(self,
            'load_table_teams')

        self.load_table_dialog.show(self)

    def save_table_file_select(self):
        '''Open a file selection dialog to choose a team csv file
        to load.'''
        self.save_table_dialog = gui.InputDialog('Save Teams', 'Input file name', width=self.base_width)
        self.save_table_dialog.set_on_confirm_value_listener(self, 'save_table_teams')
        self.save_table_dialog.show(self)

    def load_table_teams(self, filelist):
        '''Load from file an array of teams, which are loaded into the
        editable teams table.'''

        # Get the filename selected from file selection dialog
        filename = filelist[0]

        # Load teams from file
        teams = ladder.load_teams(filename)

        # By running the build table function again, the widgets are
        # overwritten with the values in the populate variable, namely
        # the loaded teams.
        self.editable_table(False, populate=teams)

    def save_table_teams(self, value):
        '''Saves the internal teams array to a filename, specified by value.'''
        ladder.save_teams(self.teams, value)

    def simulate(self):
        '''Use current settings to run a simulation.'''

        # Add teams to ladder module
        ladder.add_teams(self.teams)

        # Create main season simulator, represented by a generator.
        season_simulator = ladder.simulate_season(game=self.sport,
                                                  structure=self.tournament)

        # Iterate through the season, stopping if the status returned is not an
        # integer, in which case the final ladder has been returned.
        generator_status = 0
        self.simulation_progress()

        while type(generator_status) == int:
            self.simulation_progress(generator_status)
            generator_status = next(season_simulator)

        ladder_class = generator_status

        # Print the ladder after the main season
        ladder_class.print_ladder()
        self.output_ladder(ladder_class)

        # Simulate finals
        finals = ladder.simulate_finals(ladder=ladder_class, structure=self.finals)
        self.output_finals(finals)

    def simulation_progress(self, message=''):
        '''Updates an output label with the contents of message.'''
        self.container.append(gui.Label(str(message)), key='progress_message')

    def output_ladder(self, ladder):
        '''Adds a ladder object as a table to the GUI.'''

        row_no = len(ladder.matrix()) + 1

        self.ladder_table = gui.Table(width=self.base_width,
                                      height=self.table_row_height * row_no,
                                      margin='10px')

        self.ladder_table.from_2d_matrix(ladder.matrix())

        self.container.append(self.ladder_table, key='ladder_table')

    def output_finals(self, finals):
        '''Adds a table displaying finals games.'''
        row_no = len(finals) + 1

        self.finals_table = gui.Table(width=self.base_width,
                                      height=self.table_row_height * row_no,
                                      margin='10px')
        self.finals_table.from_2d_matrix(finals)
        self.container.append(self.finals_table, key='finals_table')

    def add_table_row(self):
        '''Adds row (from the input text area) to the end of the editable team
        table.'''

        # Ensure there is new data to be added
        try:
            row_parameters = self.new_team_parameters
        except AttributeError:
            self.display_error('No new data inputted!')
            return 1

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

        self.teams_table_height += self.table_row_height

        # Set container and table height
        self.container.set_size(self.base_width + 2 * self.side_padding,
                                self.teams_table_height
                                + 4 * self.element_height
                                + self.base_height)
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
