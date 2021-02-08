from realtime import monitor
settings = {
    'fig1': {
            'graph_dir' : 'linesdata.csv',
            'graph_type' : 'lines',
            'graph_size' : (800,700),
            'col':'col s5',
            'x-axis-moves': False
           },
    'fig2': {
            'graph_dir' : 'scatterdata.csv',
            'graph_type' : 'scatter',
            'graph_size' : (600,600),
            'col':'col s8'
           },

}
monitor.watch(settings).run()