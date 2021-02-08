import pathlib
import os, sys
import plotly.graph_objs as go

# current_file_path = pathlib.Path(__file__).parent.absolute()
# sys.path.insert(1,os.path.join(current_file_path,'../..'))
from realtime import monitor


def figure(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["x"], y=data["var1"],
                        mode='lines',
                        name='lines'))
    fig.add_trace(go.Scatter(x=data["x"], y=data["var2"],
                        mode='lines+markers',
                        name='lines+markers'))
    return fig

settings = {
    "fig2": {
            "graph_dir" : "linesdata.csv",
            "graph_type" : 'custom',
            "figure" : figure,
            "col" : 'col s4',
           },

}
monitor.watch(settings).run()