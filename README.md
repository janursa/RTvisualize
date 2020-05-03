# Real time plotting

This program enables users to conveniently visualize their data in a real-time manner using the power of Dash and Plotly. The program reads the data from CSV files and generates graphs on a web browser. The graphs will be updated automatically upon changes to the files. Currently, there are two ways of using this code:

* **Using build-in plots:** So far, there are only two types of plots that are available with limited flexibilities, i.e. [lines and scatter](https://plotly.com/python/line-and-scatter/). In this approach, the format of data given in the files must be one the followings:

  * **Lines**: The program assumes that the X-axis shows steps/time intervals, and the data of each column are the inputs for the Y-axis. Several columns can be given. Separate lines are generated for each column with the label that appears as the column name.

pip install module or python setup.py install

