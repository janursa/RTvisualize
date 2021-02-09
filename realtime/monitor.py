
"""This module is designed to visualize csv files on a browser in a real time fashion. 
Author: Jalil Nourisa

"""
import  sys, time, os
import dash
import dash_core_components as dcc
import dash_html_components as html
from   dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly
import numpy as np
from copy import deepcopy
from .buildin import plots
import copy

def _get_docs_index_path(): # returns dir of the documentation file
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
    """
    colors = ['blue','green','red','black','purple']
    def __init__(self,info):
        """Initialize the app by setting up the framework py::meth:`frame` and callback functions py::meth:`callbacks`.
        
        Args:
            info (dict): The specifications of the plots entered by the user.
        """
        # generated FIGs tagged with the figure name
        self.FIGS = {} 
        self.relayoutDatas = {} 
        # database
        self.specs = info 
        # class type for the arrangment of graphs
        self.cols = {}
        for key,spec in self.specs.items():
            if 'col' not in spec:
                spec.update({'col':'col s6'})
            self.cols.update({key:spec['col']})
        
        self.color_map = {} # maps color to each type in scatter plots
        self.app = dash.Dash(__name__,
                            external_stylesheets = _externals.get_stylesheets(),
                            external_scripts = _externals.get_scripts())

        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True

        self.update_iteration = 0 # to keep the record that how many time graphs are updated
        self.initialize()
    def initialize(self):
        self.update_db()
        self.frame()
        self.callbacks()

    def postprocess(self,name,df,fig_type):
        """
        This function catches  errors in the input file as well as addes generic size and type columns in case they are not given in the file. 
        For the case of custom plots, the process is skipped.
        For the case of scatter and scatter3, this function also categorize data based on given types.
        
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
            if fig_type == "scatter2" or fig_type == "scatter3" or fig_type == 'map':  #if it's a scatter plot, add missin items, i.e. size and type
                if "size" not in df.keys():
                    fixed_size = np.ones(len(df["x"]))
                    df["size"] = fixed_size
        
                if "type" not in df.keys():
                    fixed_type = "agent"
                    df["type"] = fixed_type
        ## organizing data based on given type. This is used for scatter and scatter3 to prevent color swinging
        if fig_type == 'scatter2' or fig_type == 'scatter3':
            types = df['type']
            types_unique = set(types) # remove the repeated items
            indices = {} # indices of df for each type
            for t in types_unique: # initialize with empty vectors
                indices.update({t:[]})
            for i in range(len(types)): # detect which rows below to which types and add it to the relevent indices
                for t in types_unique:
                    if types[i] == t:
                        indices[t].append(i)
                        break
            data_sorted = {} # sorted data based on types
            for t in types_unique:
                data_sorted.update({t:df.iloc[indices[t]]})
            df = data_sorted
            # add color map for the first time
            if name  not in self.color_map: #first time
                self.color_map.update({name:{}})
            taken_colors = self.color_map[name].values()
            nontaken_colors = deepcopy(self.colors)
            for c in list(taken_colors):
                nontaken_colors.remove(c)

            ii = 0
            for t in types_unique:
                if t not in self.color_map[name]:
                    self.color_map[name].update({t:nontaken_colors[ii]})
                ii+=1            
        # if fig_type == 'map':
        #     print(df['color_range'])
        #     if 'color_range' not in df:
        #         types = df['type']
        #         color_range = max(types)-min(types)
        #         df['color_range'] = color_range


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
        for name in self.specs.keys(): # main keys such as plot names
            # add the missing settings here
            if "col" not in self.specs[name]:
                self.specs[name]["col"] = 'col s5'
            if self.specs[name]['graph_type'] == "map":
                if "color_range" not in self.specs[name]:
                    self.specs[name]["color_range"] = None
            file = self.specs[name]["graph_dir"]
            last_moddate = os.stat(file)[8] # last modification time
            if "moddate" not in self.specs[name].keys() : # in this case, file is not upload for the first optimizer
                try:
                    data = self.read(file)
                except pd.errors.EmptyDataError:
                    print("No columns to parse from file")
                    continue
                data = self.postprocess(name,data,self.specs[name]["graph_type"])
                self.specs[name].update({"data":data})
                # self.specs[name].update({"color_map":color_map})
                self.specs[name].update({"moddate":last_moddate})
                any_update_flag = True
            elif self.specs[name]["moddate"] != last_moddate:# if the new date is different
                try:
                    data = self.read(file)
                except pd.errors.EmptyDataError:
                    print("No columns to parse from file") ## to block a bug
                    continue
                data = self.postprocess(name,data,self.specs[name]["graph_type"])

                self.specs[name].update({"data":data})
                self.specs[name].update({"moddate":last_moddate})
                any_update_flag = True

            else:
                continue
        return any_update_flag
    def frame(self):
        """
        Lays out the HTML and defines holders
        """
        layout_objects = []
        layout_objects.append(html.Div([
                html.H2('List of plots',
                        style={'float': 'left',
                               }),
                ]))
        layout_objects.append(dcc.Dropdown(id='list_of_plots',
                         options=[{'label': s, 'value': s}
                                  for s in self.specs.keys()],
                         value=[s for s in self.specs.keys()],
                         multi=True
                         ))
        layout_objects.append(dcc.Interval(
                id='time',
                interval=1000,
                n_intervals = 0))
        
        layout_objects.append(html.Div(html.Div(id="graphs",children=self.generate_graphs(self.specs.keys())), className='row'))
        self.app.layout = html.Div(layout_objects, className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})

    def callbacks(self):
        """
        Definition of callback functions are given here.
        """
        states = []
        for key in self.specs.keys():
            states.append(dash.dependencies.State(key,'relayoutData'))
        
        @self.app.callback(
            dash.dependencies.Output('graphs','children'),
            [dash.dependencies.Input('time', 'n_intervals'),dash.dependencies.Input('list_of_plots', 'value')],
            states
            )
        def update_graph(n_intervals,graph_tags,*relayoutDatas):
            i = 0
            for key in self.specs.keys():
                relayoutData = relayoutDatas[i]
                if relayoutData:
                    if 'xaxis.range[0]' in relayoutData or 'scene.camera' in relayoutData:
                        self.relayoutDatas.update({key:relayoutData})
                i+=1

            any_update_flag = self.update_db()
            if self.update_iteration < 10:
                self.update_iteration +=1
                return self.generate_graphs(graph_tags)
                # return new_figure
            elif not any_update_flag:
                raise dash.exceptions.PreventUpdate()
            else:
                return self.generate_graphs(graph_tags)
    def generate_graphs(self,graph_tags):
        """
        This function takes care of plot generation either using build-in plots or custom plots.
        """
        graphs = []
        for graph_tag in graph_tags: # iterate through requested graph names

            if self.specs[graph_tag]["graph_type"] == "custom": # if the plot is given, just add it to the graph list
                figure_func = self.specs[graph_tag]["figure"]
                FIG = figure_func(self.specs[graph_tag]["data"])

                
            else:
                if self.specs[graph_tag]["graph_type"] == "lines":
                    max_x = max(self.specs[graph_tag]["data"].index)
                    if self.specs[graph_tag]["x-axis-moves"] == True:
                        min_x = max_x - self.specs[graph_tag]["x-axis-length"]
                    else:
                        min_x = min(self.specs[graph_tag]["data"].index)
                    x_limits = [min_x,max_x]

                    FIG = plots.lines(self.specs[graph_tag]["data"],graph_tag,x_limits)
                    

                elif self.specs[graph_tag]["graph_type"] == "scatter2":
                    FIG = plots.scatter(self.specs[graph_tag]["data"],graph_tag)

                elif self.specs[graph_tag]["graph_type"] == "scatter3":
                    FIG = plots.scatter3(self.specs[graph_tag]["data"],graph_tag,self.color_map[graph_tag])
                
                elif self.specs[graph_tag]["graph_type"] == "map":
                    FIG = plots.map(self.specs[graph_tag]["data"],graph_tag,self.specs[graph_tag]["color_range"])

                else:
                    print(self.specs[graph_tag]["graph_type"])
                    print("Graph type is not defined. It should be either lines or scatter(3)")
                    sys.exit()

            if graph_tag in self.relayoutDatas:
                relayout_data = self.relayoutDatas[graph_tag]
                if  relayout_data:
                    watch.copy_graph_layout(relayout_data,FIG)
            self.FIGS.update({graph_tag:FIG})
        graphs = []
        for key in graph_tags:
            graphs.append(html.Div(dcc.Graph(
                id=key,
                figure=self.FIGS[key]
                ),className = self.cols[key])
            )
        return graphs
    @staticmethod
    def copy_graph_layout(relayout_data, FIG):
        if 'xaxis.range[0]' in relayout_data:
            FIG['layout']['xaxis']['range'] = [
                relayout_data['xaxis.range[0]'],
                relayout_data['xaxis.range[1]']
            ]
        if 'yaxis.range[0]' in relayout_data:
            FIG['layout']['yaxis']['range'] = [
                relayout_data['yaxis.range[0]'],
                relayout_data['yaxis.range[1]']
            ]
        if 'scene.camera' in relayout_data:
            FIG.update_layout(scene_camera = relayout_data['scene.camera'])
    def run(self,IP={}):
        """
        Activate the server and map the graphs on the given IP.
        Args:
            IP (string): the IP where the graphs intended for plotting.
        """
        if IP == {}:
            IP = '127.0.0.1'
        self.app.run_server(debug=True, host=IP)
