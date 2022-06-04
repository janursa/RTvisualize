import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import random
class plots:
    line_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    line_colors = ['black','black','black','black','black','black','black']
    font = 'sans-serif'
    @staticmethod
    def map(data,name,color_range=None):
        """
        Constructs a scatter plot using continous range of legends.
        """
        max_size = max(data["size"])
        fig = px.scatter(
            data,
            x = data["x"],
            y = data["y"],
            color = data["type"],
            size = data["size"],
            size_max = max_size,
            # hover_name = data["type"],
            range_color=color_range,
            render_mode='webgl',
            color_continuous_scale=px.colors.sequential.Jet
        )
        fig.update_traces(marker=dict(size=12,
                              line=dict(width=0.001,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))
        fig.update_layout(
            title=dict(
                # text= '<b>'+name+'</b>',
                y= .9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family='sans-serif',
                    size=20,
                    color='#100'
                )
                ),
             margin=dict(
                              l=10,
                              r=50,
                              b=10,
                              t=10
                          ),

            xaxis = dict(title = '', visible=False, zeroline = False,range=
                        [min(data["x"]) ,
                         max(data["x"]) ]),
            yaxis = dict(title = '',visible=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend = dict(title= '',font = dict(family = "Times New Romans", size = 20, color = "black")),
            showlegend=False    
            )
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        return fig

    @staticmethod
    def lines(specs,name,x_range):
        """Constructs a lines plot using Plotly Go

        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
            x_range (list): min and max of x axis
        
        Returns:
            Figure: Returns a figure object
        """
        random.shuffle(plots.line_colors)
        fig = go.Figure()
        i =0
        data = specs['data']
        for key,value in data.items():
            fig.add_trace(go.Scatter(
                y=value,
                name=key,
                line = dict(width=3, dash=plots.line_types[i],color = plots.line_colors[i])
            ))
            i+=1

        fig = plots.update_layout(fig,name)
        fig.update_xaxes(range=[x_range[0] - 0.5,x_range[1] + 0.5])
        if 'yrange' in specs:
            yrange = specs['yrange']
        else:
            yrange = [min([min(data[key]) for key in data.keys()]) - 0.5,
                         max([max(data[key]) for key in data.keys()]) + 0.5]
        fig.update_yaxes(range =yrange)
        
        fig.update_layout(
            # title="",
            xaxis_title="Time (hours)",
            yaxis_title="Concentration (ng/ml)",
            # legend_title="Cell state",
            font=dict(
                family="Times",
                size=22,
                color="black"
            )
        )
        return fig
    @staticmethod
    def update_layout(fig,name):
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= 0.9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family=plots.font,
                    size=20,
                    color='black'
                )),

            xaxis = dict(
                    title =dict(
                        text = 'X',
                        font=dict(
                            family=plots.font,
                            size=20,
                            color='black'
                        )
                    ),
                    showgrid=True,
                    mirror=True,
                    showline=True,
                    # zeroline = False,
                    linecolor = 'black',
                    gridwidth = 20,
                    tickfont = dict(
                        family = plots.font,
                        size = 20,
                        color = 'black'
                    )                    
                ),
            
            yaxis = dict(
                    title =dict(
                        text = 'Y',
                        font=dict(
                            family=plots.font,
                            size=20,
                            color='black'
                        )
                    ),
                    showgrid=True,
                    mirror=True,
                    showline=True,
                    linecolor = 'black',
                    gridwidth = 20,
                    tickfont = dict(
                        family = plots.font,
                        size = 20,
                        color = 'black'
                    ),
                    zeroline = False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                x=1.05,
                y=.95,
                traceorder='normal',
                font=dict(
                    family=plots.font,
                    size=20,
                    color='black'
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
        
        # fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        # fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        return fig
    @staticmethod
    def scatter(specs,name,color_map):
        """Constructs a 2D scatter plot using Plotly express
        
        Args:
            specs (dict): specs
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        markersize = None
        if 'markersize' in specs:
            markersize = specs['markersize']

        fig = go.Figure()
        i =0
        for agent_type,agent_data in specs['data'].items():
            if agent_type == 'Empty':
                opacity = 0
            else:
                opacity = 1
            fig.add_trace(go.Scatter(
                x = agent_data['x'],
                y= agent_data['y'],
                name=agent_type,
                mode='markers',
                opacity = opacity,
                marker=dict(size=markersize,
                           # line=dict(width=2,color=color_map[agent_type])
                            )   
            ))
            i+=1
        fig = plots.update_layout(fig,name)
        xrange = None
        yrange = None
        if 'xrange' in specs:
            xrange = specs['xrange']
        if 'yrange' in specs:
            yrange = specs['yrange']
        fig.update_xaxes(range = xrange)
        fig.update_yaxes(range = yrange)
        return fig
    @staticmethod
    def scatter3(specs,name,color_map):
        """Constructs a 3 Dscatter plot using Plotly express
        
        Args:
            specs (DataFrame): specs in the python dict
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        markersize = None
        if 'markersize' in specs:
            markersize = specs['markersize']
            
        fig = go.Figure()
        i =0

        for agent_type,agent_data in specs['data'].items():
            if agent_type == 'Empty':
                opacity = 0
            else:
                opacity = 1
            fig.add_trace(go.Scatter3d(
                x = agent_data['x'],
                y= agent_data['y'],
                z= agent_data['z'],
                name=agent_type,
                mode='markers',
                opacity = opacity,
                marker=dict(size=markersize,
                           line=dict(width=2)
                            )   
            ))
            i+=1
        fig = plots.update_layout(fig,name)
        xrange = None
        yrange = None
        zrange = None
        if 'xrange' in specs:
            xrange = specs['xrange']
        if 'yrange' in specs:
            yrange = specs['yrange']
        if 'zrange' in specs:
            zrange = specs['zrange']
        fig.update_scenes(xaxis = dict(range=xrange,visible=False, showticklabels=False),
                     yaxis = dict(range=yrange,visible=False, showticklabels=False),
                     zaxis = dict(range=zrange,visible=False, showticklabels=False),)
        
        return fig
