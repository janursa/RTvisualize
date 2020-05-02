import sys,os
sys.path.append(os.path.join(os.getcwd(), "monitor"))
from monitor import watch
import plotly.express as px
import pandas as pd

file = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
data1 = pd.read_csv(file)
def plot_1(data):
	fig = px.scatter(
	    data,
	    x=data["x"],
	    y=data["y"],
	    color=data["agent_type"],
	    size=data["size"],
	    # size_max=marker_max_size,
	    # size_min=min_agent_size,
	    hover_name = data["agent_type"],
	    render_mode='webgl',
	    width = 600,
	    height = 600
	)
	fig.update_layout(
	    title=dict(
	        text= '<b>'+"custom fig"+'</b>',
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


fig = plot_1(data1)
fig.show()
