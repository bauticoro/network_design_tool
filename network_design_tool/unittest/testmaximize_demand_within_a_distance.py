import unittest
from network_design_tool.maximize_demand_within_a_distance import maximize_demand_within_a_distance
from network_design_tool import input_schema
from network_design_tool import output_schema
from network_design_tool.calculate_high_service_dist_par import calculate_high_service_dist_par
from network_design_tool.calculate_max_dist_par import calculate_max_dist_par




class testmaximize_demand_within_a_distance(unittest.TestCase):

    def test_highservicehuge(self):
    # In this test we define that high service distance is extremely big, then, every customer is behind that high service distance
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': float('inf'),
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 0,
            'Max Distance Constraint': "False",
            'Maximum Distance': 0,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "False",
            'Maximum Number of Warehouses': 0
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        params = input_schema.create_full_parameters_dict(dat)
        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)
        self.assertEqual(sln.status[1], 100)


    def test_recievefromonlyone(self):
    # In this test we define that each customer can be sourced by only one warehouse
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': (dat.customer_demand['Demand Value'].sum() / 10)*1.1,
            'Recieve from Only One': "True",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 1000,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 0,
            'Max Distance Constraint': "False",
            'Maximum Distance': 0,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "True",
            'Maximum Number of Warehouses': 10
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        params = input_schema.create_full_parameters_dict(dat)
        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)
        self.assertEqual(sln.customer_assignment['Distance'].count(), dat.customers['Customer ID'].count())

    def test_capacitycero(self):
    # In this test we define a capacity constraint but we make every warehouse to have 0 capacity
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "Every Warehouse the same Capacity",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 1000,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 0,
            'Max Distance Constraint': "False",
            'Maximum Distance': 0,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "False",
            'Maximum Number of Warehouses': 0
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        params = input_schema.create_full_parameters_dict(dat)
        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)
        self.assertEqual(sln.status[0], "Infeasible")

    def test_capacitybigenoughnochanges(self):
    # In this test we run the same engine using an extremely big constraint, and a no constraint setting. They should give the same output
        def setUp(self):
            # Configuración: Se ejecuta antes de cada prueba
            self.path = "data/inputs"
            self.dat = input_schema.csv.create_pan_dat(self.path)

        def tearDown(self):
            # Limpieza: Se ejecuta después de cada prueba
            self.dat = None

        def _set_parameters(self, column_values_mapping):
            for column, value in column_values_mapping.items():
                self.dat.parameters.loc[self.dat.parameters['Name'] == column, 'Value'] = value

        def test_capacitybigenoughnochanges(self):
            # Test No Constraint
            params = input_schema.create_full_parameters_dict(self.dat)
            column_values_mapping_1 = {
                'Capacity Constraint Type': "No Constraint",
                'Every warehouse Capacity (If constraint is active)': 0,
                'Recieve from Only One': "False",
                'High Service Distance-Demand Constraint': "False",
                'High Service Distance': 1000,
                'High Service Demand (If constraint active)': 0,
                'Avg Service Distance Constraint': "False",
                'Maximum Average Distance': 0,
                'Max Distance Constraint': "False",
                'Maximum Distance': 0,
                'Total Cost Constraint': "False",
                'Maximum Cost': 0,
                'Total Number of Warehouses': "False",
                'Maximum Number of Warehouses': 0
            }
            self._set_parameters(column_values_mapping_1)
            self.dat = calculate_high_service_dist_par(self.dat)
            self.dat = calculate_max_dist_par(self.dat)
            sln1 = maximize_demand_within_a_distance(self.dat)

            # Test Constraint extremely big
            column_values_mapping_2 = {
                'Capacity Constraint Type': "Every Warehouse the same Capacity",
                'Every warehouse Capacity (If constraint is active)': float('inf'),
                'Recieve from Only One': "False",
                'High Service Distance-Demand Constraint': "False",
                'High Service Distance': 1000,
                'High Service Demand (If constraint active)': 0,
                'Avg Service Distance Constraint': "False",
                'Maximum Average Distance': 0,
                'Max Distance Constraint': "False",
                'Maximum Distance': 0,
                'Total Cost Constraint': "False",
                'Maximum Cost': 0,
                'Total Number of Warehouses': "False",
                'Maximum Number of Warehouses': 0
            }
            self._set_parameters(column_values_mapping_2)
            self.dat = calculate_high_service_dist_par(self.dat)
            self.dat = calculate_max_dist_par(self.dat)
            sln2 = maximize_demand_within_a_distance(self.dat)

            # Verificación
            self.assertEqual(sln1.customer_assignment, sln2.customer_assignment)

    def test_numberofwarehouses(self):
    # In this test we define a capacity constraint but we make every warehouse to have 0 capacity
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)

        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 1000,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 0,
            'Max Distance Constraint': "False",
            'Maximum Distance': 0,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "True",
            'Maximum Number of Warehouses': 10
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        params = input_schema.create_full_parameters_dict(dat)
        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)

        self.assertEqual(sln.opened_warehouses['Warehouse ID'].count(), params['Maximum Number of Warehouses'])

    def test_averagedistance(self):
    # In this test we make sure that maximum average distance constraint works
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)

        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 1000,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "True",
            'Maximum Average Distance': 500,
            'Max Distance Constraint': "False",
            'Maximum Distance': 0,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "False",
            'Maximum Number of Warehouses': 0
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value
        params = input_schema.create_full_parameters_dict(dat)
        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)

        self.assertTrue((sln.customer_assignment['Distance'] * sln.customer_assignment['Customer Demand']).sum() / (sln.customer_assignment['Customer Demand']).sum() < params['Maximum Average Distance'])

    def test_maxdistance(self):
    # In this test we make sure that maximum average distance constraint works
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 500,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 500,
            'Max Distance Constraint': "True",
            'Maximum Distance': 1000,
            'Total Cost Constraint': "False",
            'Maximum Cost': 0,
            'Total Number of Warehouses': "False",
            'Maximum Number of Warehouses': 0
        }
        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        params = input_schema.create_full_parameters_dict(dat)

        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)

        self.assertTrue(sln.customer_assignment['Distance'].max() < params['Maximum Distance'])

    def test_maxcost(self):
    # In this test we make sure that maximum average distance constraint works
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        params = input_schema.create_full_parameters_dict(dat)
        # Capacity Constraint Type
        column_values_mapping = {
            'Capacity Constraint Type': "No Constraint",
            'Every warehouse Capacity (If constraint is active)': 0,
            'Recieve from Only One': "False",
            'High Service Distance-Demand Constraint': "False",
            'High Service Distance': 1000,
            'High Service Demand (If constraint active)': 0,
            'Avg Service Distance Constraint': "False",
            'Maximum Average Distance': 500,
            'Max Distance Constraint': "False",
            'Maximum Distance': 1000,
            'Total Cost Constraint': "True",
            'Maximum Cost': 1000000,
            'Total Number of Warehouses': "False",
            'Maximum Number of Warehouses': 0
        }

        for column, value in column_values_mapping.items():
            dat.parameters.loc[dat.parameters['Name'] == column, 'Value'] = value

        dat = calculate_high_service_dist_par(dat)
        dat = calculate_max_dist_par(dat)
        sln = maximize_demand_within_a_distance(dat)

        self.assertTrue((sln.customer_assignment['Rates'] * sln.customer_assignment['Customer Demand']).sum() < params['Maximum Cost'])


if __name__ == '__main__':
    unittest.main()
