import plotly.graph_objs as go
import plotly.express as px
import numpy as np
class plots:
    line_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    @staticmethod
    def lines(data,name,x_limits):
        """Constructs a lines plot using Plotly Go

        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
            x_limits (list): min and max of x axis
        
        Returns:
            Figure: Returns a figure object
        """
        traces = []
        i =0
        for key,value in data.items():
            traces.append(go.Scatter(
                y=value,
                name=key,
                line = dict(width=3, dash=plots.line_types[i])
            ))
            i+=1

        layout = go.Layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= 0.9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )),
            xaxis = dict(title = "Intervals", zeroline = False,range=
                        [x_limits[0] - 0.5,
                         x_limits[1] + 0.5]),
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
        return traces, layout
    def scatter(data,name,graph_size):
        """Constructs a scatter plot using Plotly express
        
        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        x_length = max(data["x"]) - min(data["x"])
        y_length = max(data["y"]) - min(data["y"])

        max_size = max(data["size"])
        # min_agent_size = min(data["size"])
        marker_max_size = 2.*(max_size / 20**2)
        fig = px.scatter(
            data,
            x = data["x"],
            y = data["y"],
            color = data["type"],
            # size = data["size"],
            # size_max = marker_max_size,
            # size_min=min_agent_size,
            hover_name = data["type"],
            render_mode='webgl',
            width = graph_size,
            height =graph_size*(y_length / x_length)
        )
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= .9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )),
            # autosize=False,
            # width=1200,
            # height=1200
            margin=dict(
                l=50,
                r=150,
                b=100,
                t=100,
                pad=4
            )
            # paper_bgcolor="#b6e2f5"
            )
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        return fig
    def scatter3(data,name,graph_size):
        """Constructs a scatter plot using Plotly express
        
        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        x_length = max(data["x"]) - min(data["x"])
        y_length = max(data["y"]) - min(data["y"])

        max_size = max(data["size"])
        # min_agent_size = min(data["size"])
        marker_max_size = 2.*(max_size / 20**2)
        fig = px.scatter_3d(
            data,
            x = data["x"],
            y = data["y"],
            z = data["z"],
            color = data["type"],
            # size = data["size"],
            # size_max = marker_max_size,
            # size_min=min_agent_size,
            width = graph_size,
            height =graph_size*(y_length / x_length)
        )
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= .9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )),
            # autosize=False,
            # width=1200,
            # height=1200
            margin=dict(
                l=50,
                r=150,
                b=100,
                t=100,
                pad=4
            )
            # paper_bgcolor="#b6e2f5"
            )
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        return fig
