import pathlib
import os, sys
# current_file_path = pathlib.Path(__file__).parent.absolute()
# sys.path.insert(1,os.path.join(current_file_path,'../..'))
from realtime import monitor

settings = {
    'fig1': {
            'graph_dir' : 'linesdata.csv',
            'graph_type' : 'lines',
            'col':'col s4',
            'x-axis-moves': False
           },
    'fig2': {
            'graph_dir' : 'scatterdata.csv',
            'graph_type' : 'scatter2',
            'col':'col s4'
           },
    'fig3': {
            'graph_dir' : 'scatter3data.csv',
            'graph_type' : 'scatter3',
            'col':'col s6'
           },

}
monitor.watch(settings).run()