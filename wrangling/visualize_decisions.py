from math import pi

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, CategoricalColorMapper
from bokeh.plotting import figure
import pandas as pd


#Get our data from the CSV export. TODO -we can later switch this to run the SQL queries directly.
decisions_path = "summary_outputs/sample_decisions.csv"
decisions_df = pd.read_csv(decisions_path, encoding="utf8")

source = ColumnDataSource(data = decisions_df)
contracts = decisions_df.contract_number.unique().tolist()
snapshots = decisions_df.snapshot_id.unique().tolist()
snapshots.sort()

# Start making the plot
output_file('decisions_graph.html')

# Colors are red, green, gray, and blue, mapping to the factors list in the same order
colors = ['#CD5C5C','#C0D9AF', '#d3d3d3', '#0099CC']
mapper = CategoricalColorMapper(factors=['out','in', 'no change', 'other'], palette=colors)

TOOLS = "hover,save,pan,box_zoom,wheel_zoom"
plot_height = len(contracts)*10

p = figure(title="Snapshot tracking",
           x_range=snapshots, y_range=contracts,
           x_axis_location="above", plot_width=900, plot_height=plot_height,
           tools=TOOLS)

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "5pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = pi / 3

p.rect(x='snapshot_id', y='contract_number', width=1, height=1,
       #x=["c2006-02","c2006-02"], y=[1,2], width=1, height=1, #
       source=source,
       fill_color={'field': 'decision', 'transform': mapper}, #'#0099CC',
       line_color='#d3d3d3')

p.select_one(HoverTool).tooltips = [
    ('snapshot', '@snapshot_id'),
    ('decision', '@decision'),
    ('tracs_overall_expiration_date', '@tracs_overall_expiration_date'),
    ('change in expiration from previous snapshot', '@time_diff'),
    ('current contract duration (months)', '@contract_term_months_qty'),
    ('tracs_status_name', '@tracs_status_name'),
    ('previous_status', '@previous_status'),
    ('contract_number', '@contract_number')
]

show(p)      # show the plot
