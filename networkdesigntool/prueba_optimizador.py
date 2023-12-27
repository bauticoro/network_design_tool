from pulp import *
import time
import pandas as pd
from networkdesigntool import input_schema


def prueba_optimizador (dat):

    #Adapt dat input information from csvs in order to be able to be used in the optimization model
    high_service_dist_par = dict(zip(zip(dat.high_service_dist_par['Warehouse ID'],dat.high_service_dist_par['Customer ID']),dat.high_service_dist_par['Binary Value']))
    rates = dict(zip(zip(dat.rates['Origin'],dat.rates['Destination']),dat.rates['Rate']))
    maximum_dist_par = dict(zip(zip(dat.maximum_dist_par['Warehouse ID'],dat.maximum_dist_par['Customer ID']),dat.maximum_dist_par['Binary Value']))
    warehouses = dict(zip(dat.warehouses['Warehouse ID'],zip(dat.warehouses['Name'],dat.warehouses['State'],dat.warehouses['Zipcode'],dat.warehouses['Lat'],dat.warehouses['Lon'],dat.warehouses['Production Capacity'])))
    customers = dict(zip(dat.customers['Customer ID'],zip(dat.customers['Name'],dat.customers['State'],dat.customers['Zipcode'],dat.customers['Lat'],dat.customers['Lon'])))
    customer_demands = dict(zip(dat.customer_demand['Customer ID'],dat.customer_demand['Demand Value']))
    distance = dict(zip(zip(dat.distance['Origin'],dat.distance['Destination']),dat.distance['Distance']))

    #Adapt dat parameters in order to be able to be used in the optimization model
    params = input_schema.create_full_parameters_dict(dat)

    scenario_name = params['Scenario Name']
    capacity_constraint_active = params['Capacity Constraint Type']
    warehouse_capacity = params['Every warehouse Capacity (If constraint is active)']
    receive_from_only_one = params['Recieve from Only One']
    high_service_distance_constraint_active = params['High Service Distance-Demand Constraint']
    high_service_dist = params['High Service Distance']
    high_service_demand = params['High Service Demand (If constraint active)']
    avg_service_distance_constraint_active = params['Avg Service Distance Constraint']
    avg_service_dist = params['Minimum Average Distance']
    maximum_distance_constraint_active = params['Max Distance Constraint']
    maximum_dist = params['Maximum Distance']
    total_cost_constraint_active = params['Total Cost Constraint']
    total_cost = params['Maximum Cost']
    number_of_whs_constraint_active = params['Total Number of Warehouses']
    number_of_whs = params['Maximum Number of Warehouses']
    include_distance_bands = params['Include Distance Bands']
    distance_band = [params['Distance band 1'],params['Distance band 2'],params['Distance band 3'],params['Distance band 4']]
    input_map = params['Input Map']
    output_map = params['Output Map']



    return 1
