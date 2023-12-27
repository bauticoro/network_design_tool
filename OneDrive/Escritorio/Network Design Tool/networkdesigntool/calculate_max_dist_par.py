#
# This function identifies the pars with distance higher than max service and assigns it a 0 value in maximum_dist_par.csv. The rest have a 1 assigned.
#

from networkdesigntool import input_schema

def calculate_max_dist_par(dat):

    # max_dist_par will be the dictionary which holds the information about which routes are allowed while
    maximum_dist_par = dat.distance.copy()
    params = input_schema.create_full_parameters_dict(dat)

    #Renames the columns adecuated to the schema for high_service_dist_par
    maximum_dist_par['Warehouse ID']=maximum_dist_par['Origin']
    maximum_dist_par['Customer ID']=maximum_dist_par['Destination']
    maximum_dist_par = maximum_dist_par.drop(columns=['Origin'])
    maximum_dist_par = maximum_dist_par.drop(columns=['Destination'])

    #It creates a new column called "Binary Value". Depending on the value of the Distance, it assigns a binary value
    maximum_dist_par['Binary Value'] = maximum_dist_par['Distance'].apply(lambda x: 0 if x > params['Maximum Distance'] else 1)

    #It deletes distance value. It just jeeps Origin, Destination and Binary Value Columns
    maximum_dist_par = maximum_dist_par.drop(columns=['Distance'])


    dat.maximum_dist_par = maximum_dist_par

    return dat
