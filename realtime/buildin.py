import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import random
class plots:
    line_types = ['solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot']
    line_colors = ['black','black','black','black','black','black','black']
    font = 'sans-serif'
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
        random.shuffle(plots.line_colors)
        fig = go.Figure()
        i =0
        for key,value in data.items():
            fig.add_trace(go.Scatter(
                y=value,
                name=key,
                line = dict(width=3, dash=plots.line_types[i],color = plots.line_colors[i])
            ))
            i+=1

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
                        text = 'Time intervals',
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
                    ),
                    range=[x_limits[0] - 0.5,x_limits[1] + 0.5]
                ),
            
            yaxis = dict(
                    title =dict(
                        text = 'Values',
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
                    zeroline = False, 
                    range =
                        [min([min(data[key]) for key in data.keys()]) - 0.5,
                         max([max(data[key]) for key in data.keys()]) + 0.5]),
                    

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
        
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        fig.write_image(name+'.svg')
        return fig
    def scatter(data,name,graph_size):
        """Constructs a scatter plot using Plotly express
        
        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        fig = go.Figure()
        i =0
        for agent_type,agent_data in data.items():
            fig.add_trace(go.Scatter(
                x = agent_data['x'],
                y= agent_data['y'],
                name=agent_type,
                mode='markers'
            ))
            i+=1


        # max_size = max(data["size"])
        # marker_max_size = 2.*(max_size / 20**2)
        # fig = px.scatter(
        #     data,
        #     x = data["x"],
        #     y = data["y"],
        #     color = data["type"],
        #     size = data["size"],
        #     # size_max = max_size,
        #     # hover_name = data["type"],
        #     range_color=[0,100],
        #     # render_mode='webgl',
        #     color_continuous_scale=px.colors.sequential.Jet,
        #     width = graph_size,
        #     height =graph_size*(y_length / x_length)
        # )
        fig.update_traces(marker=dict(size=12,
                              line=dict(width=0.001,
                                        color='black')),
                  selector=dict(mode='markers'))
        fig.update_layout(
            title=dict(
                # text= '<b>'+name+'</b>',
                y= .9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family=plots.font,
                    size=20,
                    color='black'
                )
                ),
             margin=dict(
                              l=10,
                              r=50,
                              b=10,
                              t=10
                          ),

            # xaxis = dict(title = '', visible=False, zeroline = False,range=
            #             [min(data["x"]) ,
            #              max(data["x"]) ]),
            # yaxis = dict(title = '',visible=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend = dict(title= '',font = dict(family = plots.font, size = 20, color = "black")),
            showlegend=False    
            )
        fig.update_yaxes(automargin=True,showgrid=False,zeroline=False)
        fig.update_xaxes(automargin=True,showgrid=False,zeroline=False)
        # fig.write_image(name+'.svg')
        return fig
    def scatter3(data,name,graph_size,color_map):
        """Constructs a 3 Dscatter plot using Plotly express
        
        Args:
            data (DataFrame): data in the form of Pandas DataFrame
            name (str): the title of the plot
        
        Returns:
            Figure: Returns a figure object
        """
        fig = go.Figure()
        i =0

        for agent_type,agent_data in data.items():
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
                marker=dict(size=12,
                           line=dict(width=2,color=color_map[agent_type])
                            )   
            ))
            i+=1
        fig.update_layout(
            title=dict(
                text= '<b>'+name+'</b>',
                y= .9,
                x= 0.5,
                xanchor= 'center',
                yanchor= 'top',
                font=dict(
                    family=plots.font,
                    size=20,
                    color='#100'
                )),

            # xaxis = dict(title = 'yaya', visible=False, zeroline = False),
            # yaxis = dict(title = '', visible=False, zeroline = False),
            # autosize=False,
            # width=1200,
            # height=1200
            # margin=dict(
            #     l=50,
            #     r=150,
            #     b=100,
            #     t=100,
            #     pad=4
            # ),
            # scene_camera = dict(
                
            # ),
            legend=dict(
                x=1,
                y=.95,
                traceorder='normal',
                font=dict(
                    family=plots.font,
                    size=20,
                    color='#000'
                ),
                bordercolor='#FFFFFF',
                borderwidth=1
            ),
            autosize=False,
            width=graph_size[0],
            height=graph_size[1],
            # paper_bgcolor="#b6e2f5"
            )
        # fig.update_yaxes(visible=False, showticklabels=False)
        # fig.layout. xaxis. showticklabels = False
        fig.update_yaxes(showticklabels = False)
        fig.update_xaxes(showticklabels = False)
        return fig
