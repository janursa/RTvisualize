
from realtime import monitor


file = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
agents_traj_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_count_data.csv"

if __name__ == "__main__":
    agents_scatter_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
    agents_traj_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_traj_data.csv"
    agents_count_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_count_data.csv"
    patches_densitymap_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_densitymap_data.csv"
    patches_ph_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_ph_data.csv"
    patches_lactate_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_lactate_data.csv"
    info = {
        # "agents_scatter_data": {
        #     "figure": plot_1,
        #     "graph_type": "custom",
        #     "graph_dir": agents_scatter_data
        # },
        "agents_count_data": {
            "graph_type": "lines",
            "graph_size": 600,
            "graph_dir": agents_count_data
        }

    }
    monitor.watch(info).run() #TODO: try to update the figure upon a change in these files
