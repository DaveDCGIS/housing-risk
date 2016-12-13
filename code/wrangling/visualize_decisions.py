from math import pi

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, CategoricalColorMapper
from bokeh.plotting import figure
import pandas as pd


#Get our data from the CSV export. TODO -we can later switch this to run the SQL queries directly.
decisions_filename_noending = "random200_decisions"
decisions_path = "summary_outputs/" + decisions_filename_noending + ".csv"
decisions_df = pd.read_csv(decisions_path, encoding="utf8")

source = ColumnDataSource(data = decisions_df)
contracts = decisions_df.contract_number.unique().tolist()
snapshots = decisions_df.snapshot_id.unique().tolist()
snapshots.sort()

# Start making the plot
output_name = decisions_filename_noending + '.html'
output_file(output_name)

# Colors are red, green, gray, and blue, mapping to the factors list in the same order
colors = ['#CD5C5C','#C0D9AF', '#d3d3d3', '#0099CC', '#d3bfe0']
mapper = CategoricalColorMapper(factors=['out','in', 'no change', 'suspicious','first'], palette=colors)

TOOLS = "hover,save,pan,box_zoom,wheel_zoom"
plot_height = len(contracts)*30

p = figure(title="Snapshot tracking",
           x_range=snapshots, y_range=contracts,
           x_axis_location="above", plot_width=900, plot_height=plot_height,
           tools=TOOLS)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "9pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='snapshot_id', y='contract_number', width=0.95, height=0.9,
       #x=["c2006-02","c2006-02"], y=[1,2], width=1, height=1, #
       source=source,
       fill_color={'field': 'decision', 'transform': mapper}, #'#0099CC',
       line_color='#d3d3d3')

p.select_one(HoverTool).tooltips = [
    ('snapshot', '@snapshot_id'),
    ('decision', '@decision'),
    ('expiration_extended_test', '@expiration_extended_test'),
    ('status_test', '@status_test'),
    ('expiration_passed_test', '@expiration_passed_test'),

    ('tracs_overall_expiration_date', '@tracs_overall_expiration_date'),
    ('previous_expiration_date', '@previous_expiration_date'),
    ('change in expiration from previous snapshot', '@time_diff'),

    ('current contract duration (months)', '@contract_term_months_qty'),
    ('tracs_status_name', '@tracs_status_name'),
    ('previous_status', '@previous_status'),
    ('contract_number', '@contract_number')
]

show(p)      # show the plot
