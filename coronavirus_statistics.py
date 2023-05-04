# Project for ENS Introduction to Python Programming course 2023
# Part 2: Analysing the data
# Reminder: original data is in form [country, number of cases, number of deaths, region, population, latitude, longitude]  

#import packages
import numpy as np

def read_data():
    '''
    A function to open and transform the covid-19 data from Part I into a numpy array
    '''
    lines = open("coronavirus_data.csv").readlines()
    output = []
    for line in lines:
        line_as_list = line.strip("\n").split(",")
        output.append(line_as_list)
    output = np.array(output)
    return(output)
    
        
def region_data():
    '''
    A function that takes covid-19 data from part I, and gives a 2D Numpy array with rows: [region, # cases, # deaths, region population]
    '''
    # Skip the coordinates
    data = read_data()[:,0:5]
    # Save all the region unique values
    regions = np.unique(data[:,3])
    region_data = []
    # Cycle through regions, use a selector matrix to pick correct entries, and take sums
    for region in regions:
        selected = data[data[:,3] == region]
        sum_value = np.array([region, selected[:,1].astype(int).sum(), selected[:,2].astype(int).sum(), selected[:,4].astype(int).sum()])
        region_data.append(sum_value)
    region_data = np.array(region_data)
    return(region_data)

# Set the definite value to be a numpy array of relevant countries
def country_data(countries = read_data()[:,0].tolist()):
    '''
    A function that takes covid-19 data from part I, and gives a 2D Numpy array for an (optional, default all) list of countries
    with each row being [Country, # cases / pop, # deaths / pop, pop]
    '''
    # Skip the coordinates
    data = read_data()[:,0:5]
    country_data = []
    # Loop through selected countries, creating relevant variables, and adding the rows
    for country in countries:
        selected = data[data[:,0] == country][0]
        cases = selected[1].astype(int)
        deaths = selected[2].astype(int)
        pop = selected[4].astype(int)
        output = [country, cases/pop, deaths/pop, pop]
        country_data.append(output)
    country_data = np.array(country_data)
    return(country_data)

# Reminder: original data is in form [country, number of cases, number of deaths, region, population, latitude, longitude]  
def top_country_data(k: int, n = 0):
    '''
    A function that takes covid-19 data from part I, and gives a 2D Numpy array for the k countries with the highest (# deaths / pop)
    values with population above n (optional, default n = 0). The resulting rows are: [country, # death/pop, lat, lon]
    '''
    data = read_data()[:,(0,2,4,6,7)]   # Choosing only the relevant values [country, deaths, pop, lat, lon]
    data = data[data[:,2].astype(int) > n] # Subsetting data to be above n in population
    if data.shape[0] < k: # Checking that there are enough observations left
        print(f"Parameter n = {n} too high to get k = {k} countries.")
        return
    output = []
    for country in data: # We create the required rows by country
        death_div_pop = (country[1].astype(int) / country[2].astype(int)).astype(float)
        output_row = [country[0], death_div_pop, country[3], country[4]]
        output.append(output_row)
    output = np.array(output)
    output = output[output[:,1].astype(float).argsort()[::-1]] # Sorting the countries by the value of # death/pop, and adding an inverse command to end
    output = output[0:k,:] # Choosing only the k highest countries
    return(output)