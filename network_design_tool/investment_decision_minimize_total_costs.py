# Model_4. This model minimizes the total cost

from pulp import *
import time
import pandas as pd
from network_design_tool import input_schema
from network_design_tool import output_schema

def investment_decision_minimize_total_costs(dat):


    #Adapt dat input information from csvs in order to be able to be used in the optimization model
    high_service_dist_par = dict(zip(zip(dat.high_service_dist_par['Warehouse ID'],dat.high_service_dist_par['Customer ID']),dat.high_service_dist_par['Binary Value']))
    rates = dict(zip(zip(dat.rates['Origin'],dat.rates['Destination']),dat.rates['Rate']))
    maximum_dist_par = dict(zip(zip(dat.maximum_dist_par['Warehouse ID'],dat.maximum_dist_par['Customer ID']),dat.maximum_dist_par['Binary Value']))
    warehouses = dict(zip(dat.warehouses['Warehouse ID'],zip(dat.warehouses['Name'],dat.warehouses['City'],dat.warehouses['State'],dat.warehouses['Zipcode'],dat.warehouses['Lat'],dat.warehouses['Lon'],dat.warehouses['Production Capacity'],dat.warehouses['Default Active'])))
    customers = dict(zip(dat.customers['Customer ID'],zip(dat.customers['Name'],dat.customers['City'],dat.customers['State'],dat.customers['Zipcode'],dat.customers['Lat'],dat.customers['Lon'])))
    customer_demands = dict(zip(zip(dat.customer_demand['Customer ID'],dat.customer_demand['Time Period']),dat.customer_demand['Demand Value']))
    distance = dict(zip(zip(dat.distance['Origin'],dat.distance['Destination']),dat.distance['Distance']))
    operation_type = dict(zip(dat.operation['Operation ID'],zip(dat.operation['Operation Type Name'],dat.operation['Production Capacity'],dat.operation['Operation Cost'])))

    #Adapt dat parameters in order to be able to be used in the optimization model
    params = input_schema.create_full_parameters_dict(dat)

    scenario_name = params['Scenario Name']
    type_of_cost = params['Type of Cost']

    capacity_constraint_active = params['Capacity Constraint Type']
    warehouse_capacity = params['Every warehouse Capacity (If constraint is active)']
    receive_from_only_one = params['Recieve from Only One']
    high_service_distance_constraint_active = params['High Service Distance-Demand Constraint']
    high_service_dist = params['High Service Distance']
    high_service_demand = params['High Service Demand (If constraint active)']
    avg_service_distance_constraint_active = params['Avg Service Distance Constraint']
    avg_service_dist = params['Maximum Average Distance']
    maximum_distance_constraint_active = params['Max Distance Constraint']
    maximum_dist = params['Maximum Distance']
    total_cost_constraint_active = params['Total Cost Constraint']
    maximum_total_cost = params['Maximum Cost']
    number_of_whs_constraint_active = params['Total Number of Warehouses']
    number_of_whs = params['Maximum Number of Warehouses']
    fixed_warehouses_constraint = params['Fixed Warehouses']
    number_of_time_periods = params['Number of Time Periods']
    include_distance_bands = params['Include Distance Bands']
    distance_band = [params['Distance band 1'],params['Distance band 2'],params['Distance band 3'],params['Distance band 4']]
    input_map = params['Input Map']
    output_map = params['Output Map']

    time_periods = list(range(1, number_of_time_periods + 1))

    """
    Optimization is initialized
    """
    start_time=time.time()

    # Create the 'prob' variable to contain the problem data
    minimize_total_costs = LpProblem ( "minimize_total_costs", LpMinimize)

    """
    Decision variables are setted
    """
    # Another dicionary called 'facility_vars' is created to contain the decision variables Xi - the decision of a facility at city i to be opened or not
    facility_vars = LpVariable.dicts("Open/Close", [(w,o) for w in warehouses for o in operation_type],0,1,LpInteger)
    # flow_vars are continuous variables representing the proportion of demand of a customer 'c' satisifed by a warehouse 'w'
    flow_vars = LpVariable.dicts("Flow", [(w,c,t) for w in warehouses for c in customers for t in time_periods], lowBound=0)
    # assign vars are binary variables representing the open routes between warehouses and customers (Will only be used if supply from only one is active)
    if receive_from_only_one == "True":
        assign_vars = LpVariable.dicts("Assign", [(w,c) for w in warehouses for c in customers],0,1,LpInteger)

    """
    Objective variable is defined
    """
    # The objective function is added to 'prob' first
    if type_of_cost == "Rate per Unit":
        total_cost = lpSum([rates[w,c] * flow_vars[w,c,t] + operation_type[o][2] * facility_vars[w,o] for w in warehouses for c in customers for o in operation_type for t in time_periods])
    elif type_of_cost == "Rate per Route":
        total_cost = lpSum([rates[w,c] + operation_type[o][2] * facility_vars[w,o] for w in warehouses for c in customers for o in operation_type for t in time_periods])


    """
    Restrictions are stablished
    
    The structure of a Pulp LP constraint is: LpConstraint(e, sense, name, rhs)
    Parameters:	
    e – an instance of LpExpression
    sense – one of LpConstraintEQ, LpConstraintGE, LpConstraintLE (LpConstraintEQ means equal, LpConstraintGE means greater or equal, LpConstraintGE means less or equal)
    name – identifying string
    rhs – numerical value of constraint right hand side
    """

    # Ensures that all of a customer's demand is satisfied.
    for c in customers:
        for t in time_periods:
            minimize_total_costs += LpConstraint(
                                            e = lpSum([flow_vars[w,c,t] for w in warehouses]),
                                            sense = LpConstraintEQ,
                                            name = str(t) + "_" + str(c) + "_Served",
                                            rhs = customer_demands[c,t])

    # Ensures that only one warehouse with a specific operation type can be built in each location
    for w in warehouses:
        minimize_total_costs += LpConstraint(
                                        e = lpSum(facility_vars[w,o] for o in operation_type),
                                        sense=LpConstraintLE,
                                        name=str(w)+"_Fixed",
                                        rhs = 1)

    # Ensures that the number of warehouses constructed is the stablished at #number_of_whs
    if number_of_whs_constraint_active == "True":
        minimize_total_costs += LpConstraint(
                                        e=lpSum([facility_vars[w,o] for w in warehouses for o in operation_type]),
                                        sense=LpConstraintEQ,
                                        name="_inTotal",
                                        rhs=number_of_whs)

    # Ensures that the demand served by a warehouse doesn't exceed its capacity
    if capacity_constraint_active == "Every Warehouse the same Capacity" or capacity_constraint_active == "Capacity Specific for each Warehouse" or capacity_constraint_active == "Capacity Determined by Operation Type":
        for w in warehouses:
            for t in time_periods:
                if capacity_constraint_active == "Capacity Specific for each Warehouse":
                    warehouse_capacity = warehouses[w][6]
                elif capacity_constraint_active == "Capacity Determined by Operation Type":
                    minimize_total_costs += LpConstraint(
                                            e = lpSum([flow_vars[w, c, t] for c in customers]) - lpSum((operation_type[o][1] * facility_vars[w,o]) for o in operation_type),
                                            sense = LpConstraintLE,
                                            name =str(w) + "_" + str(t) + "_Capacity",
                                            rhs = 0)
                else:
                    minimize_total_costs += LpConstraint(
                                                e = lpSum([flow_vars[w, c] for c in customers]) - warehouse_capacity * lpSum(facility_vars[w,o] for o in operation_type),
                                                sense = LpConstraintLE,
                                                name = str(w) + "_Capacity",
                                                rhs = 0)

    # Ensures that average service distance is within the given value
    if avg_service_distance_constraint_active == "True":
        minimize_total_costs += LpConstraint(
                                        e = lpSum([distance[w,c] * flow_vars[w,c,t] for w in warehouses for c in customers for t in time_periods]) - avg_service_dist * lpSum([customer_demands[c,t] for c in customers for t in time_periods]),
                                        sense=LpConstraintLE,
                                        name="_Avg_Served",
                                        rhs= 0)

    # Ensures that a customer cannot be served from a warehouse which is farther than maximum distance value
    if maximum_distance_constraint_active == "True":
        for w in warehouses:
            for c in customers:
                for t in time_periods:
                    minimize_total_costs += LpConstraint(
                                            e = flow_vars[w,c,t],
                                            sense=LpConstraintLE,
                                            name=str(w) + "_" + str(c) + "_" + str(t) + "_Max_Served",
                                            rhs=maximum_dist_par[w, c] * customer_demands[c,t])

    # Ensures that the cost of delivering goods is less or equal than the objective stablished at #total_cost
    if total_cost_constraint_active == "True":
        minimize_total_costs += LpConstraint(
                                        e=lpSum([rates[w,c] * flow_vars[w,c,t] for w in warehouses for c in customers for t in time_periods]),
                                        sense=LpConstraintLE,
                                        name="Total_Cost",
                                        rhs=maximum_total_cost)

    # Ensures that a certain demand is within the service distance
    if high_service_distance_constraint_active == "True":
        for t in time_periods:
            minimize_total_costs += LpConstraint(
                                            e = lpSum([high_service_dist_par[w,c] * flow_vars[w,c,t] for w in warehouses for c in customers]),
                                            sense = LpConstraintGE,
                                            name = "_HighService_Served",
                                            rhs = high_service_demand)

    # If the column "Default Active" has value True, we ensure that the facility is open
    if fixed_warehouses_constraint == "True":
        for w in warehouses:
            if warehouses[w][7] == "True":
                fixed_value = 1
            else:
                fixed_value = 0

            minimize_total_costs += LpConstraint(e = lpSum(facility_vars[w,o] for o in operation_type),
                                sense=LpConstraintGE,
                                name=str(w)+"_DefaultOpen",
                                rhs = fixed_value)

    # Ensures that a warehouse must be built for there to exist flow between a warehouse and a customer
    if receive_from_only_one == "False":
        for w in warehouses:
            for c in customers:
                for t in time_periods:
                    minimize_total_costs += LpConstraint(
                                                e = lpSum(flow_vars[w, c, t] - lpSum(facility_vars[w,o] for o in operation_type) * customer_demands[c,t]),
                                                sense=LpConstraintLE,
                                                name=str(t) + "_"  + str(w) + "_" + str(c) + "_Route",
                                                rhs=0
                                                )

    if receive_from_only_one == "True":
        # Ensures that only one flow is assigned to each assign_vars
        for c in customers:
            minimize_total_costs += LpConstraint(
                                            e = lpSum([assign_vars[w, c] for w in warehouses]),
                                            sense=LpConstraintEQ,
                                            name=str(c) + "Only_One",
                                            rhs=1
                                            )

        # Ensures that a warehouse must be built for there to exist flow between a warehouse and a customer
            for w in warehouses:
                minimize_total_costs += LpConstraint(
                                            e = lpSum(assign_vars[w, c] - facility_vars[w,o] for o in operation_type),
                                            sense=LpConstraintLE,
                                            name=str(w) + "_" + str(c) + "_Route",
                                            rhs=0
                                            )

                minimize_total_costs += LpConstraint(
                                            e = lpSum(flow_vars[w,c,t] - assign_vars[w, c] * customer_demands[c,t] for t in time_periods),
                                            sense=LpConstraintLE,
                                            name=str(w) + "_" + str(c) + "_Flow&Assign",
                                            rhs=0
                                            )

    """
    Objective of the optimization is setted 
    """
    # Setting problem objective
    minimize_total_costs.setObjective(total_cost)

   # We will ensure that every output is delivered to the same output folder
    output_folder = 'data/output'

    # If output folder doesn't exist, we create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # The problem data is written to an .lp file
    lp_file_path = os.path.join(output_folder, "minimize_total_costs.lp")
    minimize_total_costs.writeLP(lp_file_path)

    # The problem is solved using PuLP's choice of Solver
    _solver = pulp.PULP_CBC_CMD(keepFiles=False,gapRel=0.00,timeLimit=120, msg=True)
    minimize_total_costs.solve(solver=_solver)

    if LpStatus[minimize_total_costs.status] == "Infeasible":
        sln = output_schema.PanDat()
        sln.status = LpStatus[minimize_total_costs.status], value(minimize_total_costs.objective)
        print("Optimization Status",LpStatus[minimize_total_costs.status])
        return sln

    end_time = time.time()

    """
    Results of the model are calculated 
    """
    # Total demand is calculated
    total_demand = []

    for t in time_periods:
        period_demand = sum(customer_demands[c,t] for c in customers)
        total_demand.append(period_demand)


    # Demand satisfied by each warehouse is calculated and appended to a dictionary
    total_demand_to_warehouse = {(w, t): sum(flow_vars[w, c, t].varValue for c in customers)
                                 for w in warehouses
                                 for t in time_periods
                                 if any(flow_vars[w, c, t].varValue > 0 for c in customers)}


    """
    if dat.distance['Distance'].count() > 0:
        # Total demand distance is calculated, taking in account how many packages are delivered in each route
        total_demand_distance = sum(distance[w,c] * flow_vars[w,c].varValue for c in customers for w in warehouses)

        # Average distance for each delivery is calculated
        actual_avg_service_dist = total_demand_distance / total_demand
    """
    # Model running time is calculated
    time_diff = end_time - start_time

    """
    Data is preparated to be written in .csv file
    """
    #
    # Opened Warehouses data is preparated
    #
    opened_warehouses = []

    for (w,o) in facility_vars.keys():
        for t in time_periods:
            if(facility_vars[w,o].varValue > 0):
                wh = {'Warehouse ID': w,
                'City': warehouses[w][0],
                'State': warehouses[w][2],
                'Zipcode': warehouses[w][3],
                'Warehouse Latitude': warehouses[w][4],
                'Warehouse Longitude': warehouses[w][5],
                'Time Period': t,
                'Total Demand to Warehouse': value(total_demand_to_warehouse[w,t]),
                'Operation Type': operation_type[o][0]
                }
                opened_warehouses.append(wh)

    # Converting the list to dataframe
    df_wh = pd.DataFrame.from_records(opened_warehouses)

    # Including just the important information in the outcome .csv
    df_wh = df_wh[['Warehouse ID', 'City', 'State', 'Zipcode', 'Total Demand to Warehouse', 'Operation Type','Time Period']]

    #
    # Customers data is preparated
    #
    customers_assignment = []

    for (w,c,t) in flow_vars.keys():
        if flow_vars[(w,c,t)].varValue > 0:
            cust = {
                'Warehouse ID': str(warehouses[w][1]) + ',' + str(warehouses[w][2]),
                'Customer ID': str(customers[c][1]) + ',' + str(customers[c][2]),
                'Customer Demand': flow_vars[(w,c,t)].varValue,
                'Warehouse Lat' : warehouses[w][4],
                'Warehouse Lon' : warehouses[w][5],
                'Customers Lat' : customers[c][4],
                'Customers Lon': customers[c][5],
                'Time Period': t,
                'Rates' : rates[w,c]
            }

            if type_of_cost == "Rate per Unit":
                cust['Transportation Cost'] = flow_vars[(w,c,t)].varValue * rates[w,c]
            elif type_of_cost == "Rate per Route":
                cust['Transportation Cost'] = rates[w,c]

            if dat.distance['Distance'].count() > 0:
                cust['Distance'] = distance[w,c]

            customers_assignment.append(cust)


    # Converting the list to dataframe
    df_cu = pd.DataFrame.from_records(customers_assignment)

    # Preparing the data to be returned
    df_cu_copy = df_cu.copy()

    # Including just the important information in the outcome .csv
    if dat.distance['Distance'].count() > 0:
        df_cu = df_cu[['Warehouse ID', 'Customer ID', 'Distance', 'Customer Demand','Transportation Cost', 'Time Period']]
    else:
        df_cu = df_cu[['Warehouse ID', 'Customer ID', 'Customer Demand','Transportation Cost', 'Time Period']]



    """
    Prepare data to be returned
    """

    df_wh_sln = df_wh.astype({'Warehouse ID': 'Float64','Operation Type': str})
    df_cu_copy = df_cu_copy.astype({'Warehouse ID': str, 'Customer ID': str, 'Customer Demand': 'Float64', 'Warehouse Lat': 'Float64', 'Warehouse Lon': 'Float64', 'Customers Lat': 'Float64', 'Customers Lon': 'Float64', 'Transportation Cost': 'Float64', 'Rates': 'Float64', 'Time Period': 'Float64'})
    if dat.distance['Distance'].count() > 0:
        df_cu_copy = df_cu_copy.astype({'Distance': 'Float64'})

    sln = output_schema.PanDat()

    sln.opened_warehouses = df_wh_sln[['Warehouse ID','Operation Type']]
    if dat.distance['Distance'].count() > 0:
        sln.customer_assignment = df_cu_copy[['Warehouse ID', 'Customer ID', 'Customer Demand', 'Distance', 'Warehouse Lat', 'Warehouse Lon', 'Customers Lat', 'Customers Lon', 'Transportation Cost', 'Rates','Time Period']]
    else:
        sln.customer_assignment = df_cu_copy[['Warehouse ID', 'Customer ID', 'Customer Demand', 'Warehouse Lat', 'Warehouse Lon', 'Customers Lat', 'Customers Lon', 'Transportation Cost', 'Rates', 'Time Period']]

    # With this line we assign a value to status. This is used at the unit test to understand the status of the engine and the result of the objective function
    sln.status = LpStatus[minimize_total_costs.status], value(minimize_total_costs.objective)

    """
    Outcome of the model is printed 
    """
    #Header is printed
    print("\nMinimize Total Costs Model")

    # The status of the solution is printed to the screen
    print ("Status:", LpStatus[minimize_total_costs.status])
    #file.write('\nstatus:'+ LpStatus[minimize_total_costs.status])
    print("Optimization Status",LpStatus[minimize_total_costs.status])

    # Results are printed to the screen
    #print("Total Demand", total_demand)
    """
    if dat.distance['Distance'].count() > 0:
        print("Total Demand Distance",total_demand_distance)
        print("Average service distance: {0:.1f} ".format(actual_avg_service_dist),"km")
    if dat.high_service_dist_par['Binary Value'].count() > 0 or high_service_distance_constraint_active == "True":
        print("% of Demand within ",high_service_dist,"km: ",round(high_service_demand*100/total_demand,2),"%")

    # Main objective is printed
    print("Objective(Total Cost): ", value(minimize_total_costs.objective))

    # If include_distance_bands is True,  demand within each distance bands is printed
    if include_distance_bands == "True" and dat.distance['Distance'].count() > 0:
        percent_demand_distance_band_1 = sum(df_cu[df_cu['Distance']<distance_band[0]]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_2 = sum(df_cu[df_cu['Distance']<distance_band[1]]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_3 = sum(df_cu[df_cu['Distance']<distance_band[2]]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_4 = sum(df_cu[df_cu['Distance']<distance_band[3]]['Customer Demand'])*100/total_demand
        print("\nPercent Demand served within {} miles : {:.1f}" .format(distance_band[0], percent_demand_distance_band_1))
        print("Percent Demand served within {} miles : {:.1f}" .format(distance_band[1], percent_demand_distance_band_2))
        print("Percent Demand served within {} miles : {:.1f}" .format(distance_band[2], percent_demand_distance_band_3))
        print("Percent Demand served within {} miles : {:.1f}" .format(distance_band[3], percent_demand_distance_band_4))

    # Model running time is printed
    print("\nRun Time of model in seconds {:.1f}" .format(time_diff))
    """
    """
    Outcome of the model is written in .txt file
    
    #Header is written
    file.write('\n\nMinimize Total Distance Model')

    # Results are written
    file.write("\nTotal Demand:"+ str(total_demand))
    file.write("\nTotal Cost: "+ str(total_cost))
    file.write("Total Demand Distance"+ str(total_demand_distance))
    file.write("\nAverage service distance: "+str(actual_avg_service_dist)+"km")
    file.write("\n% of Demand within "+str(high_service_dist)+"km: "+str(round(high_service_demand*100/total_demand,2))+"%")

    # Main objective is written
    file.write("\nObjective(Total Distance): "+ str(value(minimize_total_costs.objective)))

    # If include_distance_bands is True, demand within each distance bands is written
    if include_distance_bands == True:
        percent_demand_distance_band_1 = sum(df_cu[df_cu['Distance']<distance_band_1]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_2 = sum(df_cu[df_cu['Distance']<distance_band_2]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_3 = sum(df_cu[df_cu['Distance']<distance_band_3]['Customer Demand'])*100/total_demand
        percent_demand_distance_band_4 = sum(df_cu[df_cu['Distance']<distance_band_4]['Customer Demand'])*100/total_demand
        file.write("\nPercent Demand served within {} miles : {:.1f}" .format(distance_band[0], percent_demand_distance_band_1))
        file.write("\nPercent Demand served within {} miles : {:.1f}" .format(distance_band[1], percent_demand_distance_band_2))
        file.write("\nPercent Demand served within {} miles : {:.1f}" .format(distance_band[2], percent_demand_distance_band_3))
        file.write("\nPercent Demand served within {} miles : {:.1f}" .format(distance_band[3], percent_demand_distance_band_4))

    # Model running time is written
    file.write("\nRun Time of model in seconds {:.1f}" .format(time_diff))
    """
    """
    Data is written in .csv file
    """

    # Ruta completa del archivo de Excel en la carpeta de salida
    excel_file_path = output_folder + '/' + scenario_name + '_detailed.xlsx'

    # CSV is created
    writer = pd.ExcelWriter(excel_file_path)

    # Writing warehouses data
    df_wh.to_excel(writer, 'Opened Warehouses', index=False)

    # Writing customers data
    df_cu.to_excel(writer, 'Customers Assignment', index=False)

    # CSV is closed
    writer.close()

    """
    Output data is returned
    """
    return sln
