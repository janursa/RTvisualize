
import sys,os
sys.path.append(os.path.join(os.getcwd(), "monitor"))
from monitor import watch
import monitor
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

# help(monitor)
file = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
agents_traj_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_count_data.csv"

data = pd.read_csv(agents_traj_data)
def plot_1(data):
    fig = px.scatter(
        data,
        x=data["x"],
        y=data["y"],
        color=data["type"],
        size=data["size"],
        size_max=15,
        # size_min=min_agent_size,
        hover_name = data["type"],
        render_mode='webgl',
        width = 700,
        height = 400
    )
    # fig.update_layout(
    #     title=dict(
    #         text= '<b>'+"custom fig"+'</b>',
    #         y= .9,
    #         x= 0.5,
    #         xanchor= 'center',
    #         yanchor= 'top',
    #         font=dict(
    #             family='sans-serif',
    #             size=20,
    #             color='#100'
    #         )),
    #     # autosize=False,
    #     # width=1200,
    #     # height=1200
    #     margin=dict(
    #         l=50,
    #         r=150,
    #         b=100,
    #         t=100,
    #         pad=4
    #     )
    #     # paper_bgcolor="#b6e2f5"
    #     )
    fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
    fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
    return fig
def plot_2(data):
    fig = go.Figure()
    line_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    i =0
    for key,value in data.items():
        print(key)
        fig.add_trace(go.Scatter(
            y=value,
            name=key,
            line = dict(width=3, dash=line_types[i])
        ))
        i+=1

    fig.update_layout(
        
        xaxis = dict(title = "Intervals", zeroline = False,range=
                    [min(data.index) - 0.5,
                     max(data.index) + 0.5]),
        yaxis = dict(title = "Values", zeroline = False, range =
                    [min([min(data[key]) for key in data.keys()]) - 0.5,
                     max([max(data[key]) for key in data.keys()]) + 0.5]),
        legend=dict(
            x=1,
            y=.95,
            traceorder='normal',
            font=dict(
                family='sans-serif',
                size=12,
                color='#000'
            ),
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
    )
    return fig
fig = plot_2(data)
# fig.save("pic.png")
fig.write_image("sphnix/source/lines.svg")
# fig.show()
# # sys.path.append(, "lib"))
if __name__ == "__main__":
    agents_scatter_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
    agents_traj_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_traj_data.csv"
    agents_count_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_count_data.csv"
    patches_densitymap_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_densitymap_data.csv"
    patches_ph_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_ph_data.csv"
    patches_lactate_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_lactate_data.csv"
    info = {
        "agents_scatter_data": {
            "figure": plot_1,
            "graph_type": "custom",
            "graph_dir": agents_scatter_data
        },
        "agents_count_data": {
            "plot":"custom",
            "graph_type": "lines",
            "graph_size": 1000,
            "graph_dir": agents_count_data
        }
        # "patches_lactate_data": {
        #     "type": "lines",
        #     "dir": patches_lactate_data
        # },
        # "patches_ph_data": {
        #     "type": "lines",
        #     "dir": patches_ph_data
        # }
    }
    # watch(info).run() #TODO: try to update the figure upon a change in these files
