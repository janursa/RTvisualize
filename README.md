# Real time visualization
This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. The program reads the data from CSV files and generates graphs on a web browser. The graphs will be updated automatically upon changes to the files.

### Quick start
```
pip install RTvisualize
```
***Usage type 1, build-in plots***: in this approach, all you need is to [format the CSV files](#CSV-formating), determine the type of plot together with some other options and run the program.
```python
from realtime import monitor
settings = {
    "plot1": {
            "graph_dir" = "path/to/CSV/file1.csv",
            "graph_type" = "scatter",
            "graph_size" = 600
           },
    "plot2":{
            "graph_dir" = "path/to/CSV/file2.csv",
            "graph_type" = "lines",
            "graph_size" = 500,
            "x-axis-moves" = True,
            "x-axis-length" = 50
    }
}
monitor.watch(settings).run()
```
An example of this type can be found [here](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/).
***Usage type 2, custom plots***: this approach enables the user to construct the plot in a desired way and pass it to the program together with CSV file address and some other options.
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
def figure2(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["x1"], y=data["y1"],
                        mode='lines',
                        name='lines'))
    fig.add_trace(go.Scatter(x=data["x2"], y=data["y2"],
                        mode='lines+markers',
                        name='lines+markers'))
    return fig

settings = {
    "plot1": {
            "graph_dir" : "path/to/CSV/file1.csv",
            "graph_type" : 'custom',
            "figure" : figure1,
            "graph_size" : 800,
            'x-axis-moves': False
           },
    "plot2":{
            "graph_dir" : "path/to/CSV/file2.csv",
            "graph_type" : custom,
            "figure" : figure2,
            "graph_size" : 700,
    }
}
monitor.watch(settings).run()
```
An example of this type can be found [here](https://github.com/janursa/RTvisualize/blob/master/examples/custom/).
### CSV formating
For a line plot, the data needs to be formated in a vertical shape with the name of the variable as column title. User can use as many variables as intended to be plotted on the same graph. See [lineDataFormat](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/linesdata.csv). For scatter plots, the information x,y,type,size needs to be provided for each scatter point (see [scatterDataFormat](https://github.com/janursa/RTvisualize/blob/master/examples/builtin/scatterdata.csv)). For 3D scatter plot, the format should follow x,y,z,type,size. 
### Installation
This package can be installed using pip:
```
pip install RTvisualize
```
or download the package and command:
```
python install setup.py
```
### License
This project is licensed under the MIT License - see the LICENSE.md file for details

### Authors
* Jalil Nourisa

See also the list of contributors who participated in this project.

### Acknowledgments
Inspired by [sentdex](https://www.youtube.com/channel/UCfzlCWGWYyIQ0aLC5w48gBQ)
