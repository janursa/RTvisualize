import  sys, time, os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly
import numpy as np

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"
]
external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']


class watch:
    def __init__(self,info):
        #TODO: check that files, types, and tags have the same length
        self.df = info
    app = 0
    df = {}
    def process_data(self,df,fig_type):
        if "Unnamed: 0" in df.keys(): # processing some errors
            df = df.drop("Unnamed: 0", axis=1)

        if fig_type == "custom": #custom plot is given
            pass
        else: # add these items if custom plot is not given
            # add size if it's not there
            if fig_type == "scatter":  #if it's a scatter plot, add missin items, i.e. size and type
                if "size" not in df.keys():
                    fixed_size = np.ones(len(df["x"]))
                    df["size"] = fixed_size
        
                if "agent_type" not in df.keys():
                    fixed_agent_type = "agent"
                    df["agent_type"] = fixed_agent_type
        return df
    def read_file(self,file):
        try:
            # print("*****reading the filee****")
            data = pd.read_csv(file)
            # data = data.loc[0:100,:]
        except FileNotFoundError:
            print("Document is not found")
        return data
    def update_db(self):
        any_update_flag = False  # if any of the files has changed
        for name in self.df.keys(): # main keys such as plot names
            file = self.df[name]["graph_dir"]
            last_moddate = os.stat(file)[8] # last modification time
            if "moddate" not in self.df[name].keys() : # in this case, file is not upload for the first optimizer
                data = self.read_file(file)
                data = self.process_data(data,self.df[name]["graph_type"])

                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
                any_update_flag = True
            elif self.df[name]["moddate"] != last_moddate:# if the new date is different
                data = self.read_file(file)
                data = self.process_data(data,self.df[name]["graph_type"])

                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
                any_update_flag = True

            else:
                continue
        return any_update_flag
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
            # html.Button(id='pause', children='Pause'),
            html.Button(id='flag', children='update'),
            html.Div(children=html.Div(id='graphs'), className='row'),

            html.Div(id = "dummy1"),
            html.Div(id = "dummy2"),

            dcc.Interval(
                id='time',
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
                        [min([min(self.df[name]["data"][key]) for key in self.df[name]["data"].keys()]) - 0.5,
                         max([max(self.df[name]["data"][key]) for key in self.df[name]["data"].keys()]) + 0.5]),
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

        df = self.df[name]["data"]
        mean_length = (x_length + y_length)/2
        max_agent_size = max(df["size"])
        min_agent_size = min(df["size"])
        # marker_max_size = 2.*(max_agent_size / 20**2)
        # df["size"]=df["size"].apply(lambda x:x/marker_max_size)
        fig = px.scatter(
            self.df[name]["data"],
            x=self.df[name]["data"]["x"],
            y=self.df[name]["data"]["y"],
            color=self.df[name]["data"]["agent_type"],
            size=self.df[name]["data"]["size"],
            # size_max=marker_max_size,
            # size_min=min_agent_size,
            hover_name = self.df[name]["data"]["agent_type"],
            render_mode='webgl',
            width = self.df[name]["graph_size"],
            height = self.df[name]["graph_size"]*(y_length / x_length)
        )
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= .9,
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
    def callbacks(self):
        @self.app.callback(
            dash.dependencies.Output('graphs','children'),
            [dash.dependencies.Input('list_of_plots', 'value'),
            dash.dependencies.Input('flag','n_clicks')
            ]
            )
        def update_graph(req_graph_tags,n_clicks):
            graphs = []
            if len(req_graph_tags)>2:
                class_choice = 'col s12 m6 l6'
            elif len(req_graph_tags) == 2:
                class_choice = 'col s12 m6 l6'
            else:
                class_choice = 'col s12'
            for req_graph_tag in req_graph_tags: # iterate through requested graph tags
                if self.df[req_graph_tag]["graph_type"] == "custom": # if the plot is given, just add it to the graph list
                    figure_func = self.df[req_graph_tag]["figure"]
                    figure = figure_func(self.df[req_graph_tag]["data"])
                    graph = html.Div(dcc.Graph(
                                    id=req_graph_tag,
                                    figure=figure
                                    ), className=class_choice)
                    graphs.append(graph)
                else:
                    if self.df[req_graph_tag]["graph_type"] == "lines":
                        sub_graph,layout = self.generate_lines_graph(req_graph_tag)
                        graph = html.Div(dcc.Graph(
                                        id=req_graph_tag,
                                        figure={'data': sub_graph,'layout' : layout}
                                        ), className=class_choice)
                        graphs.append(graph)
                    elif self.df[req_graph_tag]["graph_type"] == "scatter":
                        figure = self.express_based_scatter_graph(req_graph_tag)
                        graph = html.Div(dcc.Graph(
                                        id=req_graph_tag,
                                        figure=figure
                                        ), className=class_choice)
                        graphs.append(graph)
                    else:
                        print("Graph type is not defined. It should be either lines or scatter")
                        sys.exit()

            return graphs

        @self.app.callback(dash.dependencies.Output('flag','n_clicks'),
            [dash.dependencies.Input('time', 'n_intervals')]
        )
        def check(n_intervals):
            any_update_flag = self.update_db()
            if any_update_flag:
                return 1
            else:
                raise dash.exceptions.PreventUpdate()

    def run(self):
        self.app = dash.Dash(__name__,
                            external_stylesheets = external_stylesheets,
                            external_scripts = external_scripts)
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.set_frame()
        self.callbacks()
        self.app.run_server(debug=True)
