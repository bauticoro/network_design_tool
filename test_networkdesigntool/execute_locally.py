from network_design_tool import input_schema
from network_design_tool.calculate_max_dist_par import calculate_max_dist_par
from network_design_tool.calculate_high_service_dist_par import calculate_high_service_dist_par
from network_design_tool.maximize_demand_within_a_distance import maximize_demand_within_a_distance
from network_design_tool.minimize_total_distance import minimize_total_distance
from network_design_tool.investment_decision_minimize_total_costs import investment_decision_minimize_total_costs
from network_design_tool.input_visual import input_visual
from network_design_tool.output_visual import output_visual
from network_design_tool.unittest.testminimize_total_distance import testminimize_total_distance
import unittest


# Recieves input data
path = "data/inputs"
dat = input_schema.csv.create_pan_dat(path)
"""
print(dat.rates['Rate'].count())
if dat.rates['Rate'].count() == 0:
    print("Entra")


#We will run tests
def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(testminimize_total_distance)
    #Esto es necesario para hacer correr el otro test
    suite.addTest(loader.loadTestsFromTestCase(testminimize_total_distance))


    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    return result.wasSuccessful()

success = run_tests()

if success:
    print("Todos los tests pasaron.")
else:
    print("Al menos un test falló.")
    
"""

column_values_mapping = {
    'Total Number of Warehouses': "True",
    'Maximum Number of Warehouses': 4,

    'Fixed Warehouses' : "True",

    'Capacity Constraint Type': "Capacity Determined by Operation Type",
    'Every warehouse Capacity (If constraint is active)': 1750000,

    'Recieve from Only One': "False",

    'High Service Distance-Demand Constraint': "False",
    'High Service Distance': 600,
    'High Service Demand (If constraint active)': 500100100,

    'Avg Service Distance Constraint': "True",
    'Maximum Average Distance': 150,

    'Max Distance Constraint': "True",
    'Maximum Distance': 450,

    'Total Cost Constraint': "False",
    'Maximum Cost': 0,

    'Include Distance Bands': "False",
    'Distance Band 1': 200,
    'Distance Band 2': 400,
    'Distance Band 3': 800,
    'Distance Band 4': 1600
}

for column, value in column_values_mapping.items():
    dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

params = input_schema.create_full_parameters_dict(dat)



# Calculates high service and max distance nodes
dat = calculate_high_service_dist_par(dat)
dat = calculate_max_dist_par(dat)

# Creates new files taking in account max_dist_par and high_service_par
#printing_path = "data/inputs"
#input_schema.csv.write_directory(dat,printing_path)
sln = investment_decision_minimize_total_costs(dat)

#print(sln)
#input_visual(dat)
#output_visual(dat, sln)

