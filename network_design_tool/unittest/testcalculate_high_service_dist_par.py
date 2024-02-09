import unittest
from network_design_tool.calculate_high_service_dist_par import calculate_high_service_dist_par
from network_design_tool import input_schema

class testcalculate_high_service_dist_par(unittest.TestCase):

    def test_nonhighservice(self):
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        dat.parameters.loc[dat.parameters['Name'] == 'High Service Distance', 'Value'] = -1
        dat = calculate_high_service_dist_par(dat)
        quantity_of_binaries = dat.high_service_dist_par['Binary Value'].sum()
        self.assertEqual(quantity_of_binaries, 0)

    def test_allofthemhighservice(self):
        path = "data/inputs"
        dat = input_schema.csv.create_pan_dat(path)
        dat.parameters.loc[dat.parameters['Name'] == 'High Service Distance', 'Value'] = float('inf')
        dat = calculate_high_service_dist_par(dat)
        quantity_of_binaries = dat.high_service_dist_par['Binary Value'].sum()
        quantity_of_par = dat.high_service_dist_par['Binary Value'].count()
        self.assertEqual(quantity_of_binaries, quantity_of_par)

if __name__ == '__main__':
    unittest.main()
