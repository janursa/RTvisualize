from visualization import Monitor
if __name__ == "__main__":
    agents_scatter_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_scatter_data.csv"
    agents_traj_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_traj_data.csv"
    agents_count_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/agents_count_data.csv"
    patches_densitymap_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_densitymap_data.csv"
    patches_ph_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_ph_data.csv"
    patches_lactate_data = "/Users/matin/Downloads/testProjs/CA/build/outputs/patches_lactate_data.csv"
    info = {
        "agents_count_data": {
            "type": "lines",
            "dir": agents_count_data
        },
        "patches_lactate_data": {
            "type": "lines",
            "dir": patches_lactate_data
        },
        "patches_ph_data": {
            "type": "lines",
            "dir": patches_ph_data
        }
    }
    Monitor(info).watch() #TODO: try to update the figure upon a change in these files
