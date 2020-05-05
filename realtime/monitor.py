

"""This module is designed to visualize csv files on a browser in a real time fashion. 
Author: Jalil Nourisa

"""
import  sys, time, os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
import dash
import dash_core_components as dcc
import dash_html_components as html
from   dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly
import numpy as np

from .buildin import plots

def _get_docs_index_path(): # returns dir of the documentation file
    # my_package_root = os.path.dirname(os.path.dirname(__file__))
    docs_index = os.path.join('docs', 'build', 'html', 'index.html')
    return docs_index
def _docstring_parameter(*args, **kwargs): # addes keywords to the docstring
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj
    return dec
    
class _externals:
    @staticmethod
    def get_stylesheets():
        return [ "https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
    @staticmethod
    def get_scripts():
        return ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']


@_docstring_parameter(_get_docs_index_path())
class watch:
    """This is the main class to read the files, construct plots and monitor changes.
    For documentation, see {}

    """
    
    def __init__(self,info):
        """Initialize the app by setting up the framework py::meth:`frame` and callback functions py::meth:`callbacks`.
        
        Args:
            info (dict): The information of the plots entered by the user.
        """
        self.df = info 

        self.app = dash.Dash(__name__,
                            external_stylesheets = _externals.get_stylesheets(),
                            external_scripts = _externals.get_scripts())

        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True

        self.frame()
        self.callbacks()

    app = 0
    df = {}
    def postprocess(self,df,fig_type):
        """
            - Catches some errors in the input file.
            - Addes generic size and type columns in case they are not given in the file. 
                    For the case of custom plots, the process is skipped.
        
        Args:
            df (DataFrame): Data read from the directory file. This data needs processing.
            fig_type (TYPE): The type of the plot, i.e. lines and scatter.
        
        Returns:
            DataFrame: The processed data.
        """
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
        
                if "type" not in df.keys():
                    fixed_type = "agent"
                    df["type"] = fixed_type
        return df
    def read(self,file_dir):
        """Reads the data files in csv and converts them into pandas DataFrame.
        
        Args:
            file_dir (string): file directory
        
        Returns:
            DataFrame: content of the file

        """
        try:
            data = pd.read_csv(file_dir)
        except FileNotFoundError:
            print("Given file directory {} is invalid".format(file_dir))
            sys.exit()
        return data
    def update_db(self):
        """Updates the global database in case there are changes in the files. 
        It queries modification date of files and upon change in the modification date, it calles :py:meth:`read`,
        to import the new data and then :py:meth:`postprocess` to process. 
        
        Returns:
            bool: if any changes occures, this flag will be true
        """
        any_update_flag = False  # if any of the files has changed
        for name in self.df.keys(): # main keys such as plot names
            file = self.df[name]["graph_dir"]
            last_moddate = os.stat(file)[8] # last modification time
            if "moddate" not in self.df[name].keys() : # in this case, file is not upload for the first optimizer
                data = self.read(file)
                data = self.postprocess(data,self.df[name]["graph_type"])

                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
                any_update_flag = True
            elif self.df[name]["moddate"] != last_moddate:# if the new date is different
                data = self.read(file)
                data = self.postprocess(data,self.df[name]["graph_type"])

                self.df[name].update({"data":data})
                self.df[name].update({"moddate":last_moddate})
                any_update_flag = True

            else:
                continue
        return any_update_flag
    def frame(self):
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
            html.Button(id='flag', children='update'),
            html.Div(children=html.Div(id='graphs'), className='row'),

            dcc.Interval(
                id='time',
                interval=1000,
                n_intervals = 0)
        ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})
    def callbacks(self):
        """Contains two call back functions. py::meth:`update_graph`.
        """
        @self.app.callback(
            dash.dependencies.Output('graphs','children'),
            [dash.dependencies.Input('list_of_plots', 'value'),
            dash.dependencies.Input('flag','n_clicks')
            ]
            )
        def update_graph(req_graph_tags,n_clicks):
            """Summary
            
            Args:
                req_graph_tags (TYPE): Description
                n_clicks (TYPE): Description
            
            Returns:
                TYPE: Description
            """
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
                        max_x = max(self.df[req_graph_tag]["data"].index)
                        if self.df[req_graph_tag]["x-axis-moves"] == True:
                            min_x = max_x - self.df[req_graph_tag]["x-axis-length"]
                        else:
                            min_x = min(self.df[req_graph_tag]["data"].index)
                        x_limits = [min_x,max_x]

                        sub_graph,layout = plots.lines(self.df[req_graph_tag]["data"],req_graph_tag,x_limits)
                        graph = html.Div(dcc.Graph(
                                        id=req_graph_tag,
                                        figure={'data': sub_graph,'layout' : layout}
                                        ), className=class_choice)
                        graphs.append(graph)
                    elif self.df[req_graph_tag]["graph_type"] == "scatter":
                        figure = plots.scatter(self.df[req_graph_tag]["data"],req_graph_tag)
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
            """If any of the files are changed, sets the buttom flag to 1 (a change) to intrigue py::meth:`update_graph`. 
            
            Args:
                n_intervals (int): time
            
            Returns:
                int: value of the buttom 
            
            Raises:
                dash.exceptions.PreventUpdate
                if there is no update, simply raise an exception to prevent alteration of the button value.
            """
            any_update_flag = self.update_db()
            if any_update_flag:
                return 1
            else:
                raise dash.exceptions.PreventUpdate()

    def run(self):
        """Summary
        """

        self.app.run_server(debug=True, host='127.0.0.1')
