

from realtime import monitor

def linefigure(data):
    fig = px.scatter(
        data,
        x=data["x"],
        y=data["y"],
        size=data["size"]
    )
    return fig
def scatterfigure(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data["x1"], y=data["y1"],
                        mode='lines',
                        name='lines'))
    fig.add_trace(go.Scatter(x=data["x2"], y=data["y2"],
                        mode='lines+markers',
                        name='lines+markers'))
    return fig

settings = {
    "fig1": {
            "graph_dir" : "linesdata.csv",
            "graph_type" : 'custom',
            "figure" : linefigure,
            "graph_size" : (800,700),
            'x-axis-moves': False
           },
    "fig2": {
            "graph_dir" : "scatterdata.csv",
            "graph_type" : 'custom',
            "figure" : scatterfigure,
            "graph_size" : (700,700)
           },

}
monitor.watch(settings).run()