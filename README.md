
# Real time visualization
This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. The program reads the data from CSV files and generates graphs on a web browser. The graphs will be updated automatically upon changes to the files.  
## Installation
This package can be installed using pip:
```
pip install RTvisualize
```
or download the package and command:
```
python install setup.py
```
## Quick start
The library requires a setting variable for execution, where the user can specify as many plots as desired for simultaneous visualization.  A generic template looks like this,
```python
from realtime import monitor
settings = {
    'name1': {...}, # specifications for the 1st graph
    'name2':{...} # specifications for the 2nd graph
monitor.watch(settings).run(IP='0.0.0.0`) # runs the server and maps the graphs on the specified IP:8050 address
   ```
The specifications of each plot contains a few important entries from the user. Generally, two types of approaches can be taken in using the library; first, using [build-in plots](#build-in-plots); and second, using [custom plots](#custom-plots).
### Build-in plots
The library provides the following build-in plots:

- [Line plot](#line-plots)
- [Scatter plots 2D](#scatter-plots-2D)
- [Scatter plots 3D](#scatter-plots-3D)

See  the <a href="https://github.com/janursa/RTvisualize/tree/master/examples/builtin">example</a>.
#### Line plots
Line plots intends to monitor the progression of variables during time (see <a href="https://plotly.com/python/line-charts/" title="cppy">Plotly line plots</a>).  The required specifications entry for the line plots looks like,
```py
    'plot1':{
            'graph_dir' = 'path/to/CSV/file1.csv', # directory to csv file containing the data
            'graph_type' = 'lines', # specifies the graph type
    }
```
Additional settings available for line plots are,
```py
            'col': 'col s5', # specifies grid size for the html page
            'x-axis-moves' = True, # whether to move the x-axis by holding the x-length fixed
            'x-axis-length' = 50 # if the above flag is True, specify the x-axis length
```
For the html grid specification see  <a href="https://materializecss.com/grid.html" >here</a>. The csv file needs to be formated in a vertical shape with the name of the variable as column title. User can use as many variables as intended to be plotted on the same graph. See [example](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/linesdata.csv).
#### Scatter plots 2D
The required specifications entry for the line plots looks like,
```py
    'plot2':{
            'graph_dir' = 'path/to/CSV/file2.csv', # directory to csv file containing the data
            'graph_type' = 'scatter2', # specifies the graph type
    }
```
Additional settings available,
```py
            'col': 'col s5', # specifies grid size for the html page
```
For scatter plots, the information `x,y,type,size` needs to be provided for each scatter point (see [example](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/scatterdata.csv)). 

#### Scatter plots 3D
The specifications entry for scatter plot 3D is similar to [scatter 2D](#scatter-plot-2D) with the exeptions of:
```py
        'graph_type' = 'scatter3'
```
and the csv formatting is similar to the scatter 2D with the exception of having an additional `z`item, i.e. `x,y,z,type,size`. See [example](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/scatter3data.csv). 

### Custom plots
This approach enables the user to construct the plot in a desired way and pass it to the program together with CSV file,
```python
from realtime import monitor
def figure1(data):
    fig = px.scatter(
        data,
        x=data["x"],
        y=data["y"],
        size=data["size"]
    )
    return fig
settings = {
    "plot1": {
            "graph_dir" : "path/to/CSV/file1.csv",
            "graph_type" : 'custom', # this is different than build-in plots
            "figure" : figure1, # this provides the plotting function
            "col" : 'col s5'
           }
}
```
An example of this type can be found [here](https://github.com/janursa/RTvisualize/blob/master/examples/custom/).


### License
This project is licensed under the MIT License - see the LICENSE.md file for details

### Authors
* Jalil Nourisa

### Acknowledgments
Inspired by [sentdex](https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ)
