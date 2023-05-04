# Project for ENS Introduction to Python Programming course 2023
# Part 3: Visualizing the data
# Reminder: -original data is in form [country, number of cases, number of deaths, region, population, latitude, longitude] 
#           -top_country_data is in form [country, #death / pop, lat, lon]
#           -country_data is in form [Country, # cases / pop, # deaths / pop, pop]
#           -region_data is in the form [region, # cases, # deaths, region population]

#import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import coronavirus_statistics as cs
import cartopy.crs as ccrs

# Create functions
def regions_piechart(region = str, show = False):
    '''
    Makes a piechart for a given region: 1 fraction is # covid deaths the other is # infected but recovered 
    '''
    data = cs.region_data()
    # Choose only relevant region
    data = data[data[:,0] == region]
    fracs = np.array([data[0][2].astype(float), (data[0][1].astype(float)-data[0][2].astype(float))]).astype(float)
    labels = "Deaths", "Recovered"
    fig = plt.figure(figsize=(6,6))
    plt.pie(fracs, labels = labels, autopct="%1.3f")
    plt.title(f"Covid-19 deaths and recoveries in {region}")
    plt.savefig("regions_piechart.png")
    if show:
        plt.show()
    plt.clf()

def countries_barchart(countries = cs.read_data()[:,0].tolist(), show = False):
    data = cs.country_data(countries = countries)
    # Data wrangling, setting to 1m cases, and rounding a bit
    labels = data[:,0]
    data[:,1] = np.around(data[:,1].astype(float)*1000000,3)
    data[:,2] = np.around(data[:,2].astype(float)*1000000,3)
    # Charts for cases per 1m citizens
    x_pos = np.linspace(1,len(data), num = len(data))
    plt.subplot(1,2,1)
    plt.title("Covid-19 cases per 1m")
    plt.bar(x = x_pos, height = data[:,1].astype(float), width = 0.4, color = "y")
    plt.xticks(x_pos, labels, fontsize = 8)
    # Some tricks needed to get a nice dataset-adaptive y-axis 
    plt.yticks(np.linspace(0,round(data[:,1].astype(float).max(),-4),5))
    # Charts for deaths per 1m citizens
    plt.subplot(1,2,2)
    plt.title("Covid-19 deaths per 1m")
    plt.bar(x = x_pos, height = data[:,2].astype(float), width = 0.4, color = "r")
    plt.subplots_adjust(wspace=0.4)
    plt.xticks(x_pos, labels, fontsize = 8)
    # Some tricks needed to get a nice dataset-adaptive y-axis 
    plt.yticks(np.linspace(0,round(data[:,2].astype(float).max(),-2),5))
    plt.savefig("countries_barchart_cases_deaths.png")
    if show:
        plt.show()   
    plt.clf()       

def highest_mortality(k: int, n = 0, show = False):
    '''
    For all countries with pop <= n get gets countries with the highest number of deaths per 1m, and draws barcharts
    '''
    data = cs.top_country_data(k = k,n = n)
    # Change var to be multiplied by 1m
    data[:,1] = data[:,1].astype(float)*1000000
    # Plotting
    plt.title("Most Covid19 deaths per 1m citizens")
    labels = data[:,0]
    # Setting up appropriate number of bars
    x_pos = np.linspace(1,len(data), num = len(data))
    cases_1m_bar = plt.bar(x = x_pos, height = data[:,1].astype(float), width = 0.4, color = "r")
    plt.xticks(x_pos, labels, fontsize = 8)
    # Some tricks needed to get a nice dataset-adaptive y-axis 
    plt.yticks(np.linspace(0,round(data[:,1].astype(float).max(),-1),5))
    plt.savefig("countries_barchart_highest_mortality.png")
    if show:
        plt.show()  
    plt.clf() 
        
def map(k: int, show = False):
    '''
    Maps the capitals for the k countries with the most Covid-19 deaths per capita. Circle sizes vary on mortality.
    '''
    data = cs.top_country_data(k = k)   
    # Taking a projection that seems ok from the website    
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.stock_img()    
    # First lon then lat, multiplying with a scale factor (trial & error) to get nice marker sizes
    for country in data:
        deaths_per_cap = np.around(country[1].astype(float)*300,0).astype(int)
        lat = country[2].astype(float)
        lon = country[3].astype(float)
        plt.plot(lon, lat, color='red', marker='o', linewidth = 0, transform=ccrs.Geodetic(),
            markersize = deaths_per_cap)
    plt.savefig("map_highest_mortality.png")
    if show:
        plt.show()
    plt.clf()
    
def main():
    study_y_n = input(f"Do you want to study coronavirus data?")    
    if study_y_n != "Yes":
        print(f"Either you don't want to study the data, or I don't understand you. Goodbye!")
        return()
    while True:
        which_graph = int(input(f"Indicate by a number which of the graphs you want to study (1,2,3,4)"))
        if which_graph == 1:
            choice_reg = input(f"Indicate which world region / continent you want to study")
            regions_piechart(choice_reg, show = True)
        elif which_graph == 2:
            choice_country = input(f"Indicate which countries you want to study, separated by commas and without spaces").split(",")
            countries_barchart(choice_country, show = True)
        elif which_graph == 3:
            choice_k = int(input(f"Indicate the number of highest-mortality countries you want to study"))
            choice_n = int(input(f"Indicate the threshold population value, set to 0 if you want to consider all countries"))
            highest_mortality(choice_k ,choice_n, show = True)
        elif which_graph == 4:
            choice_k = int(input(f"Indicate the number of highest-mortality countries you want to study"))
            map(choice_k)
        stop_flag = bool(input(f"Press enter to continue, and any other key to stop"))
        if stop_flag:
            break
    return()

if __name__ == "__main__":
   main()       
