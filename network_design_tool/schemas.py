"""
Defines the input and output schemas of an adapted version of the diet problem.
"""

from ticdat import PanDatFactory


# region INPUT SCHEMA
input_schema = PanDatFactory(
    # syntax: table_name=[['Primary Key One', 'Primary Key Two'], ['Data Field One', 'Data Field Two']]
    parameters=[['Name'], ['Value']],
    warehouses=[['Warehouse ID'], ['Name', 'City', 'State', 'Zipcode', 'Lat', 'Lon', 'Production Capacity', 'Default Active']],
    customers=[['Customer ID'], ['Name', 'City', 'State', 'Zipcode', 'Lat', 'Lon']],
    customer_demand=[['Customer ID','Time Period'], ['Demand Value']],
    distance=[['Origin', 'Destination'], ['Distance']],
    rates=[['Origin', 'Destination'], ['Rate']],
    high_service_dist_par=[['Warehouse ID', 'Customer ID'], ['Binary Value']],
    maximum_dist_par=[['Warehouse ID', 'Customer ID'], ['Binary Value']],
    operation=[['Operation ID'],['Operation Type Name','Production Capacity','Operation Cost']])


# endregion

# region USER PARAMETERS
input_schema.add_parameter('Scenario Name', default_value='scenario_1', number_allowed=False, strings_allowed='*')

input_schema.add_parameter('Type of Cost', default_value='Rate per Unit', number_allowed=False,
                           strings_allowed=['Rate per Unit', 'Rate per Route'])

input_schema.add_parameter('Location', default_value='US', number_allowed=False,
                           strings_allowed=['Global', 'US', 'Asia', 'LATAM'])

input_schema.add_parameter('Optimization Type', default_value='Maximize Demand Within Distance', number_allowed=False,
                           strings_allowed=['Maximize Demand Within Distance', 'Minimize Total Distance', 'Minimize Total Weighted Demand', 'Minimize Total Costs', 'Minimize Total Warehouses'])

input_schema.add_parameter('Capacity Constraint Type', default_value='No Constraint', number_allowed=False,
                           strings_allowed=['No Constraint', 'Every Warehouse the same Capacity', 'Capacity Specific for each Warehouse','Capacity Determined by Operation Type'])
input_schema.add_parameter('Every warehouse Capacity (If constraint is active)', default_value=1000000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Recieve from Only One', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])

input_schema.add_parameter('High Service Distance-Demand Constraint', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('High Service Distance', default_value=1000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.add_parameter('High Service Demand (If constraint active)', default_value=1000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Avg Service Distance Constraint', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Maximum Average Distance', default_value=2000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Max Distance Constraint', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Maximum Distance', default_value=1000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Total Cost Constraint', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Maximum Cost', default_value=10000000, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Total Number of Warehouses', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Maximum Number of Warehouses', default_value=5, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Fixed Warehouses', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])

input_schema.add_parameter('Number of Time Periods', default_value=1, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Include Distance Bands', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Distance band 1', default_value=200, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.add_parameter('Distance band 2', default_value=400, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.add_parameter('Distance band 3', default_value=800, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.add_parameter('Distance band 4', default_value=1600, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0.0, inclusive_min=False, max=float('inf'), inclusive_max=False)

input_schema.add_parameter('Input Map', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
input_schema.add_parameter('Output Map', default_value='False', number_allowed=False,
                           strings_allowed=['True', 'False'])
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    opened_warehouses=[['Warehouse ID'], ['City', 'State', 'Zipcode', 'Lat', 'Lon', 'Total Demand to Warehouse']],
    customer_assignment=[['Warehouse ID', 'Customer ID'], ['Customer Demand', 'Distance', 'Warehouse Lat', 'Warehouse Lon', 'Customers Lat', 'Customers Lon', 'Transportation Cost', 'Rates']],
    status = [['Status'],['Result']])
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA
# region warehouses
table = 'warehouses'
input_schema.set_data_type(table=table, field='Warehouse ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
for field in ['Name', 'City', 'State']:
    input_schema.set_data_type(table=table, field=field, number_allowed=False, strings_allowed='*', nullable=True)
input_schema.set_data_type(table=table, field='Zipcode', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Lat', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-90, inclusive_min=True, max=90, inclusive_max=True)
input_schema.set_data_type(table=table, field='Lon', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-180, inclusive_min=True, max=180, inclusive_max=True)
input_schema.set_data_type(table=table, field='Production Capacity', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Default Active', number_allowed=False, strings_allowed='*', nullable=True)
# endregion

# region customers
table = 'customers'
input_schema.set_data_type(table=table, field='Customer ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
for field in ['Name', 'City', 'State']:
    input_schema.set_data_type(table=table, field=field, number_allowed=False, strings_allowed='*')
input_schema.set_data_type(table=table, field='Zipcode', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Lat', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-90, inclusive_min=True, max=90, inclusive_max=True)
input_schema.set_data_type(table=table, field='Lon', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-180, inclusive_min=True, max=180, inclusive_max=True)
# endregion


# region customer_demand
table = 'customer_demand'
input_schema.set_data_type(table=table, field='Customer ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.set_data_type(table=table, field='Time Period', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Demand Value', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
# endregion

# region distance
table = 'distance'
input_schema.set_data_type(table=table, field='Origin', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.set_data_type(table=table, field='Destination', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
input_schema.set_data_type(table=table, field='Distance', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)

input_schema.add_foreign_key(native_table=table, foreign_table='warehouses', mappings=[('Origin', 'Warehouse ID')])
input_schema.add_foreign_key(native_table=table, foreign_table='customers', mappings=[('Destination', 'Customer ID')])
# endregion

# region rates
table = 'rates'
input_schema.set_data_type(table=table, field='Origin', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Destination', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Rate', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False, nullable=True)

input_schema.add_foreign_key(native_table=table, foreign_table='warehouses', mappings=[('Origin', 'Warehouse ID')])
input_schema.add_foreign_key(native_table=table, foreign_table='customers', mappings=[('Destination', 'Customer ID')])
# endregion

# region high_service_dist_par
table = 'high_service_dist_par'
input_schema.set_data_type(table=table, field='Warehouse ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Customer ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Binary Value', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=1, inclusive_max=True, nullable=True)

input_schema.add_foreign_key(native_table=table, foreign_table='warehouses', mappings=[('Warehouse ID', 'Warehouse ID')])
input_schema.add_foreign_key(native_table=table, foreign_table='customers', mappings=[('Customer ID', 'Customer ID')])
# endregion

# region maximum_dist_par
table = 'maximum_dist_par'
input_schema.set_data_type(table=table, field='Warehouse ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Customer ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Binary Value', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=1, inclusive_max=True, nullable=True)

input_schema.add_foreign_key(native_table=table, foreign_table='warehouses', mappings=[('Warehouse ID', 'Warehouse ID')])
input_schema.add_foreign_key(native_table=table, foreign_table='customers', mappings=[('Customer ID', 'Customer ID')])
# endregion

# region operation
table = 'operation'
input_schema.set_data_type(table=table, field='Operation ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Operation Type Name', number_allowed=False, strings_allowed='*')
input_schema.set_data_type(table=table, field='Production Capacity', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False, nullable=True)
input_schema.set_data_type(table=table, field='Operation Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False, nullable=True)
# endregion
# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA
# region opened_warehouses
table = 'opened_warehouses'
output_schema.set_data_type(table=table, field='Warehouse ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
for field in ['City', 'State']:
    output_schema.set_data_type(table=table, field=field, number_allowed=False, strings_allowed='*')
output_schema.set_data_type(table=table, field='Zipcode', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Lat', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-90, inclusive_min=True, max=90, inclusive_max=True)
output_schema.set_data_type(table=table, field='Lon', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-180, inclusive_min=True, max=180, inclusive_max=True)
output_schema.set_data_type(table=table, field='Total Demand to Warehouse', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
# endregion

# region customer_assignment
table = 'customer_assignment'
output_schema.set_data_type(table=table, field='Warehouse ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Customer ID', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=False, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Customer Demand', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Distance', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Warehouse Lat', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-90, inclusive_min=True, max=90, inclusive_max=True)
output_schema.set_data_type(table=table, field='Warehouse Lon', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-180, inclusive_min=True, max=180, inclusive_max=True)
output_schema.set_data_type(table=table, field='Customers Lat', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-90, inclusive_min=True, max=90, inclusive_max=True)
output_schema.set_data_type(table=table, field='Customers Lon', number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=-180, inclusive_min=True, max=180, inclusive_max=True)
output_schema.set_data_type(table=table, field='Transportation Cost', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
output_schema.set_data_type(table=table, field='Rates', number_allowed=True, strings_allowed=(),
                           must_be_int=True, min=0, inclusive_min=True, max=float('inf'), inclusive_max=False)
# endregion

# region status
table = 'status'
output_schema.set_data_type(table=table, field='Status', number_allowed=False, strings_allowed='*')
output_schema.set_data_type(table=table, field='Result', number_allowed=False, strings_allowed='*')
# endregion
# endregion
