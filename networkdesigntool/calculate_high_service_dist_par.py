#
# This function identifies the pars with distance higher than high service distance and assigns it a 0 value in high_service_dist_par.csv. The rest have a 1 assigned.
#

from networkdesigntool import input_schema

def calculate_high_service_dist_par(dat):

    # max_dist_par will be the dictionary which holds the information about which routes are allowed while
    high_service_dist_par = dat.distance.copy()
    params = input_schema.create_full_parameters_dict(dat)

    #Renames the columns adecuated to the schema for high_service_dist_par
    high_service_dist_par['Warehouse ID']=high_service_dist_par['Origin']
    high_service_dist_par['Customer ID']=high_service_dist_par['Destination']
    high_service_dist_par = high_service_dist_par.drop(columns=['Origin'])
    high_service_dist_par = high_service_dist_par.drop(columns=['Destination'])

    #It creates a new column called "Binary Value". Depending on the value of the Distance, it assigns a binary value
    high_service_dist_par['Binary Value'] = high_service_dist_par['Distance'].apply(lambda x: 0 if x > params['High Service Distance'] else 1)

    #It deletes distance value. It just jeeps Origin, Destination and Binary Value Columns
    high_service_dist_par = high_service_dist_par.drop(columns=['Distance'])

    dat.high_service_dist_par = high_service_dist_par

    return dat
