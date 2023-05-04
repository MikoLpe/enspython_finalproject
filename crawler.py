# Project for ENS Introduction to Python Programming course 2023
# Part 1: Gathering data

#import packages
import numpy as np
import requests
from bs4 import BeautifulSoup

def cases_deaths():
    '''
    Crawls covid data on cases and deaths by country from worldometers.info, and parses them into a numpy array
    '''
    # Download and parse data
    page = requests.get("https://bit.ly/3din7Bs")
    soup = BeautifulSoup(page.content,"html.parser")
    stats = []
    countries = []
    # We make a list of lists by breaking the collection at every 4th object
    i = 1
    for tag in soup.select("tr td"):
        # Deal with the specific Japanese case and remove commas
        cell = tag.get_text().replace(",","") if tag.get_text() != "Japan (+Diamond Princess)" else "Japan"        
        stats.append(cell)
        if i % 4 == 0:
            countries.append(stats)
            stats = []
        i += 1
    countries = np.array(countries)
    # Delete the second to last row with the MS ZAANDAM (axis = 0 is horizontal)
    countries = countries[countries[:,0] != "MS ZAANDAM"]
    countries = np.delete(countries, -2, 0)
    #sort in ascending order
    countries = countries[countries[:,0].argsort()]
    return(countries)

def population():
    '''
    Crawls population data by country from worldometers.info and makes a numpy array
    '''
    # Download and parse data
    page = requests.get("https://bit.ly/3lWkVDO")
    soup = BeautifulSoup(page.content,"html.parser")
    populations = []
    countries = []
    # We make a list of populations, taking advantage of them being the only bolded ones
    for tag in soup.select("tr > td[style='font-weight: bold;']"):
        # remove commas, <td style="font-weight: bold;  ">1,439,323,776</td>
        populations.append(tag.get_text().replace(",",""))
    # We make a list of countries, taking advantage of them being the only ones with "a"
    for tag in soup.select("td > a"):
        countries.append(tag.get_text())
    # We then combine them:
    output = []
    for i in range(0,len(countries)):
        output_item = []
        output_item.append(countries[i])
        output_item.append(int(populations[i]))
        output.append(output_item)
    output = np.array(output)
    # Sort
    output = output[output[:,0].argsort()]
    return(output)

def capital_coordinates():
    '''
    Takes city data from provided csv-file, selects capital city coordinates for all countries
    '''
    output = []
    file = open("worldcities.csv", encoding = "utf-8").readlines()
    for line in file:
        content = line.split(",")
        item = []
        # Doing some data cleaning: standardizing country names
        content[4] = "Micronesia" if content[4] == "Micronesia Federated States Of" else content[4]
        content[4] = "Congo" if content[4] == "Congo (Brazzaville)" else content[4]
        content[4] = "DR Congo" if content[4] == "Congo (Kinshasa)" else content[4]
        content[4] = "Czech Republic (Czechia)" if content[4] == "Czechia" else content[4]
        content[4] = "Côte d'Ivoire" if content[4] == "Côte D’Ivoire" else content[4]
        content[4] = "Antigua and Barbuda" if content[4] == "Antigua And Barbuda" else content[4]
        content[4] = "Bosnia and Herzegovina" if content[4] == "Bosnia And Herzegovina" else content[4]
        content[4] = "Bahamas" if content[4] == "Bahamas The" else content[4]
        content[4] = "Myanmar" if content[4] == "Burma" else content[4]
        content[4] = "North Macedonia" if content[4] == "Macedonia" else content[4]
        content[4] = "Saint Kitts & Nevis" if content[4] == "Saint Kitts And Nevis" else content[4]
        content[4] = "Sao Tome & Principe" if content[4] == "Sao Tome And Principe" else content[4]
        content[4] = "St. Vincent & Grenadines" if content[4] == "Saint Vincent And The Grenadines" else content[4]
        content[4] = "State of Palestine" if content[4] == "West Bank" else content[4]
        content[4] = "Trinidad and Tobago" if content[4] == "Trinidad And Tobago" else content[4]
        content[4] = "Eswatini" if content[4] == "Swaziland" else content[4]
        # Choosing only those who report a primary capital, and only taking one value per country
        check_double = sum([content[4] in city for city in output])
        # Including the special case of Ottawa (federal capital of Canada)
        if (content[0] == "Ottawa" and content[4] == "Canada") or (content[8] == "primary" and check_double == 0) or (content[4] == "Curaçao"):
            item = [content[4],content[1],float(content[2]),float(content[3])]
            output.append(item)
    # Make into array
    output = np.array(output)
    # Sort
    output = output[output[:,0].argsort()]
    return(output)

def main():
    '''
    Combines worldometers.info data on covid and populations alongside given information on city locations into numpy array
    of one row per country - with some exceptions since we end up with 193 obs
    '''
    cases = cases_deaths() # 229 obs, 4 fields: country, number of cases, number of deaths, region.
    pop = population() # 235 obs, 2 fields: country, population
    coord = capital_coordinates() # 197 obs, 4 fields: country, city, lat lon
    output = np.array([0,1,2,3,4,5,6,7]) # We use the sorted structure and run through indices in the shortest list
    i, j, k, = 0,0,0
    with open("coronavirus_data.csv", "w") as file:
        while k < len(coord) and j < len(pop) and i < len(cases):
            coord_country = coord[k, 0]
            pop_country = pop[j, 0]
            cases_country = cases[i, 0]
            # Check for all cases except full equality, move pointer if needed
            if coord_country < pop_country or coord_country < cases_country:
                k += 1
            elif pop_country < coord_country or pop_country < cases_country:
                j += 1
            elif cases_country < coord_country or cases_country < pop_country:
                i += 1
            else:
                # Concatenate arrays with country names dropped out, write to file
                row = np.concatenate((cases[i,:],pop[j,1:],coord[k,1:]))
                file.write(f"{','.join(row)}\n")
                # Move up the index for k - could be i or j, is ultimately arbitrary since the names are same
                k += 1
    
# We try out code and write to file
if __name__ == "__main__":
    main()
    
