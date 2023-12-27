from networkdesigntool import input_schema
from networkdesigntool.calculate_max_dist_par import calculate_max_dist_par
from networkdesigntool.calculate_high_service_dist_par import calculate_high_service_dist_par
from networkdesigntool.maximize_demand_within_a_distance import maximize_demand_within_a_distance
from networkdesigntool.input_visual import input_visual
from networkdesigntool.output_visual import output_visual



# Recieves input data
path = "data/inputs"
dat = input_schema.csv.create_pan_dat(path)

# Calculates high service and max distance nodes
dat = calculate_high_service_dist_par(dat)
dat = calculate_max_dist_par(dat)


# Creates new files taking in account max_dist_par and high_service_par
printing_path = "data/inputs/data_completed"
input_schema.csv.write_directory(dat,printing_path)

sln = maximize_demand_within_a_distance(dat)

input_visual(dat)
output_visual(dat, sln)
