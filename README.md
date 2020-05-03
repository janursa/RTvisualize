# Real time plotting
This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. 
### Quick start
***install***
```
pip install realtime_visualization
```
***Usage type 1***: build-in plots
```python
from monitor import watch
settings = {
    "plot1": {
            "graph_dir" = "path/to/CSV/file1.csv",
            "graph_type" = scatter,
            "graph_size" = 600
           },
    "plot2":{
            "graph_dir" = "path/to/CSV/file2.csv",
            "graph_type" = lines,
            "graph_size" = 500,
            "x-axis-moves" = True,
            "x-axis-length" = 50
    }
}
watch(settings).run()
```
***Usage type 2***: custom plots
```python
from monitor import watch
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
            "graph_dir" = "path/to/CSV/file1.csv",
            "graph_type" = custom,
            "figure" = figure1
           },
    "plot2":{
            "graph_dir" = "path/to/CSV/file2.csv",
            "graph_type" = custom,
            "figure" = figure2
    }
}
watch(settings).run()
```
See [Documentation](https://janursa.github.io/realtime_plotting/) for further information and examples.

### Installation
This package can be installed using pip:
```
pip install realtime_plotting
```
or conda:
```
conda install -c realtime_plotting
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


This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. The program reads the data from CSV files and generates graphs on a web browser. The graphs will be updated automatically upon changes to the files. Currently, there are two ways of using this code:

* **Using build-in plots:** So far, there are only two types of plots that are available, i.e. [lines and scatter](https://plotly.com/python/line-and-scatter/). Using this approach, the format of data given in the files must be one the followings:
# Real time plotting
This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. The program reads the data from CSV files and generates graphs on a web browser. The graphs will be updated automatically upon changes to the files. To use this program, after installation, command:
```
from monitor import watch
watch(info).run()
```
The info consists the information of the graphs as a Python dictionary object. It can take up to as many graphs as desired, each tagged with the graph name (which will be shown in the browser) and assosiated settings.  
```json
{
  "graph_name1":graph_1_settings,
  "graph_name2":graph_2_settings,
}
```
Each graph settings is another Python dictionary that specifies few items depending on the type of the approach chosen for plotting. In the following, it is discussed in more detail.

* **Using build-in plots:** In this approach, the user needs to provide these settings:

```json
            {
              "graph_dir" = "path/to/CSV/file.csv",
              "graph_type" = scatter or lines
              "graph_size" = graph width in px, e.g. 700
              "x-axis-move" = True or false. If true, the x-axis moves as it receives more data
              "x-axis-span" = a number. The length of x axis (if "x-axis-move" is true)
            }
```
            
Currently, there are two ways of using this code:

* So far, there are only two types of plots that are available, i.e. [lines and scatter](https://plotly.com/python/line-and-scatter/).
  * **Lines**: The program assumes that the X-axis shows steps/time intervals, and the data of the Y-axis is given in in the file as columns. Separate lines are generated for each column with the label that appears as the column name. For example, if there are two sets of data that needs to be visualized together, organize them in two columns and give a name to each, e.g. Y1 and Y2.
  
       | **y1** | **y2** |
       | ------ | ------ |
       | 1.2    | 5.2 |
       | 2.1   | 0.1        |
       | ...   | ...        |

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
pip install module or python setup.py install


  * **Lines**: The program assumes that the X-axis shows steps/time intervals, and the data the Y-axis is given in columns. Separate lines are generated for each column with the label that appears as the column name.
  
       | **y1** | **y2** |
       | ------ | ------ |
       | 1.2    | 5.2 |
       | 2.1   | 0.1        |
       | ...   | ...        |

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```
pip install module or python setup.py install

