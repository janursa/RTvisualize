import  sys, time, os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"
]
external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']



class Monitor:
    def __init__(self,info):
        #TODO: check that files, types, and tags have the same length
        self.df = info
    app = 0
    df = {}
    def process_data(self,df):
        """
        checks for the errors in the files
        """
        if "Unnamed: 0" in df.keys(): # processing some errors
            df = df.drop("Unnamed: 0", axis=1)

        return df
    def read_file(self,file):
        try:
            print("*****reading the filee****")
            data = pd.read_csv(file)
            # data = data.loc[0:100,:]
        except FileNotFoundError:
            print("Document is not found")
        data = self.process_data(data)
        return data
    def update_db(self):
        for name in self.df.keys():
            file = self.df[name]["dir"]
            last_moddate = os.stat(file)[8] # last modification time
            if "moddate" not in self.df[name].keys(): # in this case, file is not upload for the first optimizer
                data = self.read_file(file)
                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
            elif self.df[name]["moddate"] != last_moddate:# if the new date is different
                data = self.read_file(file)
                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
            else:
                continue
    def set_frame(self):
        """
        Lays out the HTML and defines holders
        """
        self.app.layout = html.Div([
            html.Div([
                html.H2('List of plots',
                        style={'float': 'left',
                               }),
                ]),
            dcc.Dropdown(id='list_of_plots',
                         options=[{'label': s, 'value': s}
                                  for s in self.df.keys()],
                         value=[s for s in self.df.keys()],
                         multi=True
                         ),
            html.Div(children=html.Div(id='graphs'), className='row'),
            dcc.Interval(
                id='graph_update',
                interval=1000,
                n_intervals = 0)
        ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})
    def generate_lines_graph(self,name):
        line_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
        traces = []
        i =0
        for key,value in self.df[name]["data"].items():
            traces.append(go.Scatter(
                y=value,
                name=key,
                # line = dict(width=4, dash=line_types[i])
                line = dict(width=3, dash=line_types[i])
            ))
            i+=1

        layout = go.Layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= 0.9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )),
            xaxis = dict(title = "Intervals", zeroline = False,range=
                        [min(self.df[name]["data"].index) - 0.5,
                         max(self.df[name]["data"].index) + 0.5]),
            yaxis = dict(title = "Values", zeroline = False, range =
                        [min([min(self.df[name]["data"][key]) for key in self.df[name]["data"].keys()]) - 0.1,
                         max([max(self.df[name]["data"][key]) for key in self.df[name]["data"].keys()]) + 0.1]),
            legend=dict(
                x=1,
                y=.95,
                traceorder='normal',
                font=dict(
                    family='sans-serif',
                    size=12,
                    color='#000'
                ),
                # bgcolor='#E2E2E2',
                bordercolor='#FFFFFF',
                borderwidth=1
            ),
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
            # annotations=[
            #     dict(
            #         x=1.16,
            #         y=1,
            #         xref='paper',
            #         yref='paper',
            #         text='<I> Quantities: </I>',
            #         showarrow=False
            #     )
            # ]
        )
        return traces, layout
    def express_based_scatter_graph(self,name):
        x_length = max(self.df[name]["data"]["x"]) - min(self.df[name]["data"]["x"])
        y_length = max(self.df[name]["data"]["y"]) - min(self.df[name]["data"]["y"])
        mean_length = (x_length + y_length)/2
        max_agent_size = max(self.df[name]["data"]["size"])
        marker_max_size = 290*(max_agent_size / mean_length)+2.7290
        fig = px.scatter(
            self.df[name]["data"],
            x=self.df[name]["data"]["x"],
            y=self.df[name]["data"]["y"],
            color=self.df[name]["data"]["type"],
            size=self.df[name]["data"]["size"],
            size_max=marker_max_size,
            hover_name = self.df[name]["data"]["type"],
            render_mode='webgl',
            width = 700*(x_length/y_length),
            height = 700
        )
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= 0.9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )),
            # autosize=False,
            # width=1200,
            # height=1200
            margin=dict(
                l=50,
                r=150,
                b=100,
                t=100,
                pad=4
            )
            # paper_bgcolor="#b6e2f5"
            )
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        return fig
    def generate_scatter_graph(self,name):

        # def NORMALIZE_SIZE(sizes):
        #     min_size = min(sizes)
        #     max_size = max(sizes)
        #     diff = max_size - min_size
        #     base_size = 5
        #     std_sizes = []
        #     for size in sizes:
        #         std_size = base_size * (1 + (size-min_size)/diff)
        #         std_sizes.append(std_size)
        #     return std_sizes

        trace=go.Scatter(
            x=self.df[name]["data"]["x"],
            y=self.df[name]["data"]["y"],
            mode='markers'
        )

        layout = go.Layout(
            # xaxis = dict(title = "X position", zeroline = False,range =[
            #             min(self.df[name]["data"]["x"]) - 15,
            #             max(self.df[name]["data"]["x"]) +15
            #         ]),
            # yaxis = dict(title = "Y position", zeroline = False,
            #         range =[
            #             min(self.df[name]["data"]["y"]) - 15,
            #             max(self.df[name]["data"]["y"]) +15
            #         ]),
            # height=600,
            # width=600,
            # legend=dict(
            #     x=1,
            #     y=.95,
            #     traceorder='normal',
            #     font=dict(
            #         family='sans-serif',
            #         size=12,
            #         color='#000'
            #     ),
            #     # bgcolor='#E2E2E2',
            #     bordercolor='#FFFFFF',
            #     borderwidth=1
            # ),
            annotations=[
                dict(
                    x=1.16,
                    y=1,
                    xref='paper',
                    yref='paper',
                    text='<I> Cell types: </I>',
                    showarrow=False
                )
            ]

        )
        return [trace],layout
    def callbacks(self):
        @self.app.callback(
            dash.dependencies.Output('graphs','children'),
            [dash.dependencies.Input('list_of_plots', 'value'),
            dash.dependencies.Input('graph_update', 'n_intervals')]
            )
        def update_graph(req_graph_tags,n_intervals):
            graphs = []
            self.update_db()  #TODO
            if len(req_graph_tags)>2:
                class_choice = 'col s12 m6 l4'
            elif len(req_graph_tags) == 2:
                class_choice = 'col s12 m6 l6'
            else:
                class_choice = 'col s12'
            for req_graph_tag in req_graph_tags: # iterate through requested graph tags
                if self.df[req_graph_tag]["type"] == "lines":
                    sub_graph,layout = self.generate_lines_graph(req_graph_tag)
                    graphs.append(html.Div(dcc.Graph(
                        id=req_graph_tag,
                        figure={'data': sub_graph,'layout' : layout}
                        ), className=class_choice))
                if self.df[req_graph_tag]["type"] == "scatter":
                    graph = self.express_based_scatter_graph(req_graph_tag)
                    # sub_graph,layout = self.generate_scatter_graph(req_graph_tag)
                    graphs.append(html.Div(dcc.Graph(
                        id=req_graph_tag,
                        figure=graph
                        ), className=class_choice))
                    # graphs.append(html.Div(dcc.Graph(
                    #     id=req_graph_tag,
                    #     figure={'data': sub_graph,'layout' : layout}
                    #     ), className=class_choice))


            return graphs



    def monitor(self):
        self.app = dash.Dash(__name__,
                            external_stylesheets = external_stylesheets,
                            external_scripts = external_scripts)
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.set_frame()
        self.callbacks()
        self.app.run_server(debug=True)
if __name__ == "__main__":
    # file1 = "/Users/matin/Downloads/testProjs/ABM/interface/outputs/errors.csv"
    # file2 = "/Users/matin/Downloads/testProjs/ABM/interface/outputs/file2.csv"
    # file2 = "/Users/matin/Downloads/testProjs/ABM/interface/outputs/abs_errors.csv"
    cell_dist = "/Users/matin/Downloads/testProjs/ABM/build/outputs/cell_dist.csv"
    error = "/Users/matin/Downloads/testProjs/NN/outputs/errors.csv"
    abs_error = "/Users/matin/Downloads/testProjs/NN/outputs/abs_errors.csv"
    info = {
        "cell_dist": {
            "type": "scatter",
            "dir": cell_dist
        },
        "error": {
            "type": "lines",
            "dir": error
        },
        # "abs_error": {
        #     "type": "lines",
        #     "dir": abs_error
        # },
    }
    Monitor(info).monitor() #TODO: try to update the figure upon a change in these files
