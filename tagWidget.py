# Usage: This is a widget that allows you to edit csv files within an output cell of a jupyter notebook, and save the changes to a new csv file. Example drawn from: https://medium.com/@williams.evanpaul/edit-pandas-dataframes-within-jupyterlab-36f129129496
# 1) import tagWidget (i.e. this .py file) from the current directory
# 2) from tagWidget import qgrid (contains settings from tagWidget.py)
# 3) qgrid_df = qgrid.show_grid(df) (displays the dataframe with editable columns within the notebook)
# 4) call qgrid_df and make edits in any column
# 5) q = qgrid_df.get_changed_df() (create new df containing the changes made to the dataframe)
# 6) q.to_csv(...) (save the 'q' table output to a new file)

import pandas as pd
import qgrid
import ipywidgets as widgets

# set display options
qgrid.set_grid_option('forceFitColumns', True)
qgrid.set_grid_option('defaultColumnWidth', 400)
qgrid.set_grid_option('enableColumnReorder', True)
qgrid.set_grid_option('rowHeight', 120)

pd.options.display.max_columns = 25
pd.set_option('max_colwidth', 1000)
"""--------------------------------------
    1. display output for current row
-----------------------------------------"""
# Create and display output widget for the currently selected row
current_row = widgets.Output(layout=widgets.Layout(border='1px solid black', 
                                                   height='99%', 
                                                   width='99%', 
                                                   overflow_x='auto', 
                                                   overflow_y='auto', 
                                                   overflow='auto'#,
#                                                    display='inline-flex',
#                                                    flex_wrap='wrap',
# #                                                    flex='auto',
#                                                    flex_flow='row wrap',
#                                                    align_content='center'
                                                  ))
#     overflow-wrap: break-word;

# The widget will appear as the output of this cell
# Right-click it and select "Create New View for Output", then drag it to the right side of the screen
# Finally, hide the cell's output by clicking the blue bar to the left of the output

"""--------------------------------------
    2. display the output widget for edited rows, and create the DataFrame to hold the edits
-----------------------------------------"""
# Make the DataFrame to hold edited rows
edit_cols = ['data', 'index', 'column', 'old', 'new']
edits = pd.DataFrame(columns=edit_cols)

# Make the three components for the edited rows widget
edited_cells = widgets.Output(layout=widgets.Layout(border='1px solid black', overflow_y='auto'))#, height='150px',overflow_x='auto',  overflow='auto',display='inline-flex',flex_wrap='wrap',flex_flow='row wrap',align_content='center'))
#  flex='auto',
                                                   
edits_file_name = widgets.Text(placeholder='File name')
export_button = widgets.Button(description='Export to CSV', tooltip='Export your edits to CSV')
clear_button = widgets.Button(description='Clear edits', tooltip='Clear the output widget and all stored edits')

# Function to use when the 'Export to CSV' button is clicked
def export_edits(sender):
    name = edits_file_name.value
    edits.to_csv(f'{name}.csv')

# Function to use when the 'Clear edits' button is clicked
def clear_edits(sender):
    edited_cells.clear_output()
    global edits
    edits = pd.DataFrame(columns=edit_cols)
    
# Construct and display the widget
# The widget will appear as the output of this cell
# Right-click it and select "Create New View for Output", then drag it to the right side of the screen
# Finally, hide the cell's output by clicking the blue bar to the left of the output
export_button.on_click(export_edits)
clear_button.on_click(clear_edits)
export_features = widgets.HBox([edits_file_name, export_button, clear_button])
widgets.VBox([export_features, edited_cells])

# This cell creates two Qgrid event handlers and links them with the appropriate output widgets

# Display the currently selected row from any Qgrid widget in the current_row output widget
# This will be activated when Qgrid detects that a new row is selected
def get_current_row(event, qgrid_widget):
    output_area = current_row
    with output_area:
        display(qgrid_widget.get_selected_df().T)
        output_area.clear_output(wait=True)
        

# Display the edits in the edited_cells output widget and store them in the edits DataFrame
# This will be activated when Qgrid detects that a cell is edited
def get_edits(event, qgrid_widget):
    output_area = edited_cells
    with output_area:
        event['data']=[name for name, val in globals().items() if val is qgrid_widget.df][0]
        event_index = event['index']
        event_column = event['column']
        event_old = event['old']
        event_new = event['new']
        event_data = event['data']
        print(f'{event_data}[{event_index}, {event_column}] \t old: {event_old} \t new: {event_new}')
        relevant = ['index', 'column', 'data', 'old', 'new']
        global edits
        edits = edits.append({k: event[k] for k in relevant}, ignore_index=True)
        

# Link the two functions above to the appropriate Qgrid events
qgrid.on(['selection_changed'], get_current_row)
qgrid.on(['cell_edited'], get_edits)