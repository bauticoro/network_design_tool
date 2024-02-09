# In this function, we are visualizaing the output data-- the data after the optimization has run
from network_design_tool import input_schema
import pandas as pd
import plotly

def output_visual(dat, sln):

    """
    We adapt dat and sln to be structured in a easier way to be used
    """

    if dat.rates['Rate'].count() > 0:
        customer_assignment = pd.DataFrame(list(zip(
            sln.customer_assignment['Warehouse ID'],
            sln.customer_assignment['Customer ID'],
            sln.customer_assignment['Customer Demand'],
            sln.customer_assignment['Warehouse Lat'],
            sln.customer_assignment['Warehouse Lon'],
            sln.customer_assignment['Customers Lat'],
            sln.customer_assignment['Customers Lon'],
            sln.customer_assignment['Transportation Cost'],
            sln.customer_assignment['Rates']
        )), columns=['Warehouse ID', 'Customer ID', 'Customer Demand', 'Warehouse Lat', 'Warehouse Lon', 'Customers Lat', 'Customers Lon', 'Transportation Cost', 'Rates'])
    else:
        customer_assignment = pd.DataFrame(list(zip(
            sln.customer_assignment['Warehouse ID'],
            sln.customer_assignment['Customer ID'],
            sln.customer_assignment['Customer Demand'],
            sln.customer_assignment['Warehouse Lat'],
            sln.customer_assignment['Warehouse Lon'],
            sln.customer_assignment['Customers Lat'],
            sln.customer_assignment['Customers Lon']
        )), columns=['Warehouse ID', 'Customer ID', 'Customer Demand', 'Warehouse Lat', 'Warehouse Lon', 'Customers Lat', 'Customers Lon'])


    opened_warehouses = list(sln.opened_warehouses['Warehouse ID'])

    warehouses = dict(zip(
        dat.warehouses['Warehouse ID'],
        zip(
            dat.warehouses['Name'],
            dat.warehouses['City'],
            dat.warehouses['State'],
            dat.warehouses['Zipcode'],
            dat.warehouses['Lat'],
            dat.warehouses['Lon'],
            dat.warehouses['Production Capacity']
        )
    ))

    customers = dict(zip(
        dat.customers['Customer ID'],
        zip(
            dat.customers['Name'],
            dat.customers['City'],
            dat.customers['State'],
            dat.customers['Zipcode'],
            dat.customers['Lat'],
            dat.customers['Lon']
        )
    ))

    customer_demands = dict(
        zip(
            dat.customer_demand['Customer ID'],
            dat.customer_demand['Demand Value']
        )
    )

    params = input_schema.create_full_parameters_dict(dat)

    scenario_name = params['Scenario Name']
    model_name = "-"
    location = params['Location']


    """
    We process input data to be able to visualize it
    """

    warehouse_list = []
    for w in opened_warehouses:
            wh = {
                        'text':'Warehouse-'+warehouses[w][0],
                        'State':warehouses[w][2],
                        'ZipCode':warehouses[w][3],
                        'lat':warehouses[w][4],
                        'long':warehouses[w][5],
                        'cnt':10000000,
                        'size' : 30,
                        'color' : 'rgba(0, 100, 0)'
                        }
            warehouse_list.append(wh)


    customer_list =[]
    for c in customers.keys():
        cust = {
            'text':'Customer-'+customers[c][0],
            'State':customers[c][2],
            'ZipCode':customers[c][3],
            'lat':customers[c][4],
            'long':customers[c][5] ,
            'cnt':customer_demands[c],
            'size' : 3,
            'color' : 'rgb(255, 0, 0)'
        }
        customer_list.append(cust)

    """
    We define how do we want to visualize data
    """

    df = pd.DataFrame.from_records(warehouse_list)
    df['shape'] =  "triangle-down"
    df_cust = pd.DataFrame.from_records(customer_list)
    df_cust['shape'] =  "circle"
    df = pd.concat([df, df_cust], ignore_index=True)

    paths = []
    for i in range( len( customer_assignment) ):
            paths.append(
                dict(
                    type = 'scattergeo',
                    locationmode = 'country names',
                    lon = [ customer_assignment['Warehouse Lon'][i], customer_assignment['Customers Lon'][i] ],
                    lat = [ customer_assignment['Warehouse Lat'][i], customer_assignment['Customers Lat'][i] ],
                    mode = 'lines',
                    line = dict(
                        width = 1,
                        color = 'red',
                    ),
                    opacity = 0.8,
                )
            )


    locations = [ dict(
            type = 'scattergeo',
            locationmode = 'country names',
            lon = df['long'],
            lat = df['lat'],
            hoverinfo = 'text',
            text = df['text'],
            mode = 'markers',
            marker = dict(
                size=df['size'],
                color=df['color'],
                symbol = df['shape'],
                line = dict(
                    width=3,
                    color='rgba(68, 68, 68, 0)'
                ),
            ))]

    if location == "US":
        layout = dict(
                title = "Model Output: "+model_name,
                showlegend = False,
                geo = dict(
                    scope='usa',
                    projection=dict( type='albers usa' ),
                    showland = True,
                    landcolor = 'rgb(243, 243, 243)',
                    countrycolor = 'rgb(204, 204, 204)',
                ),
            )

    if location == "Asia":
        layout = dict(
                title = "Model Output: "+model_name,
                showlegend = False,
                geo = dict(
                    scope='asia',
                    projection=dict( type='mercator' ),
                    showland = True,
                    landcolor = 'rgb(243, 243, 243)',
                    countrycolor = 'rgb(204, 204, 204)',
                ),
            )
    if location == "South America":
        layout = dict(
                title = "Model Output: "+model_name,
                showlegend = False,
                geo = dict(
                    scope='south america',
                    projection=dict( type='mercator' ),
                    showland = True,
                    landcolor = 'rgb(243, 243, 243)',
                    countrycolor = 'rgb(204, 204, 204)',
                ),
            )

    if location == "Europe":
        layout = dict(
            title = "Model Output: "+model_name,
            showlegend = False,
            geo = dict(
                scope='europe',
                projection=dict( type='mercator' ),
                showland = True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(204, 204, 204)',
            ),
        )


    """
    We plot data
    """
    plotly.offline.plot({"data":locations+paths, "layout":layout},filename=scenario_name+'_output.html')
