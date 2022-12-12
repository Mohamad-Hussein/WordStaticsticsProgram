#Name: Aire Bernard, Mohamad Hussein
#Group: L06 - 12 (Pairs)

import numpy as np
import matplotlib.pyplot as plt

country_data = np.genfromtxt('Country_Data.csv',delimiter=',',skip_header=True,dtype=str)#Had to change encoding because it returns each value as a byte
population_data = np.genfromtxt('Population_Data.csv',delimiter=',',skip_header=True,dtype=int)#Turns country entries into -1, will not need them as index will be used
threatened_data = np.genfromtxt('Threatened_Species.csv',delimiter=',',skip_header=True,dtype=int)

countries = [x[0].lower() for x in country_data] #Lowered the entries to match input with this list
regions = [x[1].lower() for x in country_data] #Kept duplicates to keep track of the index
sub_regions = [x[2].lower() for x in country_data]

#CLASSES
class Country():
    '''A class used to create the object of a country

        Attributes:
            index(int): Integer that keeps track of the placement of the country in the list.
    '''
    def __init__(self,index):
        self.index = index
        self.name = country_data[self.index][0]
        #list of populations throughout 2000-2020, did this reduce the amount of times I create this instance so I can access it throughout the functions
        self.pop_list = [i for i in population_data[self.index][1:]]
        self.region = country_data[self.index][1]
        self.subregion = country_data[self.index][2]
        self.size = country_data[self.index][3]
        self.years = [x for x in range(2000,2021)] #Stored in object to shorten code
        self.threatened_species_list = [i for i in threatened_data[self.index][1:]] #Stored in object to shorten code

    def print_all(self):
        '''Prints the information on a country like name, region, subregion and size.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        print('\nName: {}\nRegion: {}\nSub-region: {}\nSize: {} Sq Km'.format(self.name,self.region,self.subregion,self.size))

    def pop_change(self):
        '''Calculates the average population change in the country and graphs the populations throughout
        2000-2020 and graphs the change in population from year to year. Also prints out the average population 
        change of a country per year.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        change_population = []
        ind = 0
        #To find the change in population from year to year and store it in list
        for i in self.pop_list:
            if ind != 0: #Skipping first entry so no error message pops up from index out of range
                change_population.append(i - self.pop_list[ind-1])
            ind +=1
        average_pop_change = np.average(change_population)
        print('\nThe average population change in {} is {} per year.\n'.format(self.name,round(average_pop_change)))
        #Having the right label to represent if it is in millions or billions
        ylabel_pop = correct_units(self.pop_list,'Population')
        ylabel_pop_change = correct_units(change_population,'Population Change')
        #Population chart
        plt.figure(num=1,figsize=(15,15),dpi=80)
        plt.subplot(2,1,1)
        plt.plot(self.years,self.pop_list,'b--',label=ylabel_pop)
        plt.xlabel('Years')
        plt.ylabel(ylabel_pop)
        plt.legend(loc='upper right')
        plt.xticks(self.years)
        plt.title('The population in {} between 2000 and 2020'.format(self.name))
        #Change in population chart
        plt.subplot(2,1,2)
        plt.plot(self.years[1:],change_population,'r--',label=ylabel_pop_change)
        plt.xlabel('Years')
        plt.ylabel(ylabel_pop_change)
        plt.legend(loc='upper right')
        plt.xticks(self.years)
        plt.title('The change in population in {} between 2000 and 2020'.format(self.name))
        plt.show()

    def max_min_pop(self):
        '''Finds the most population a country has had and the least population between 2000 and 2020 and prints out those values.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        max_pop = max(self.pop_list)
        max_year = self.years[self.pop_list.index(max_pop)]
        min_pop = min(self.pop_list)
        min_year = self.years[self.pop_list.index(min_pop)]
        
        print('\nThe most population that {} had is {} in {}.'.format(self.name,max_pop,max_year))
        print('The least population that {} had is {} in {}.'.format(self.name,min_pop,min_year))
    
    def avg_thr_species(self): 
        '''Finds the average of the threatened species in a country and prints it. 
        Prints out the number of threatened species in a country and graphs it.
        
        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        species_list = self.threatened_species_list.copy() #to shorten it
        #Finds average of the threatened species in a country
        average = np.average(self.threatened_species_list)
        print('\nThe average number of threatened species is {}.\nIn total, there are {} endangered species in {}.'.format(round(average),sum(species_list),self.name))
        print('\nThreatened species in {}:\nPlants: {}\nFish: {}\nBirds: {}\nMammals: {}\n'.format(self.name,species_list[0],species_list[1],species_list[2],species_list[3]))
        types_list = ['Plants','Fish','Birds','Mammals']
        plt.figure(num=2,figsize=(8,8),dpi=80)
        plt.bar(types_list,species_list,color='r')
        plt.title(f'The number of threatened species in {self.name} compared to their types')
        plt.xlabel('Types of threatened species')
        plt.ylabel('The number of threatened species')
        plt.show()


class Region(): 
    '''A class used to create the object of both a region and subregion that contains functions that calculate desired 
    values

        Attributes:
            name(str): It is the name of the region and stores it in the object.
    '''
    def __init__(self,name):
        #This is to differentiate between a region and sub region, did this to recycle code for region
        if name in regions: 
            self.region_name = country_data[regions.index(name)][1] #I did it this way to make the first letter capital
            self.countries = [i[0] for i in country_data if i[1] == self.region_name] #All countries situated in the region chosen

        elif name in sub_regions:
            self.region_name = country_data[sub_regions.index(name)][2]
            self.countries = [i[0] for i in country_data if i[2] == self.region_name]
        
        self.total_species_list = []
        #Goes through all the countries in a region and finds the total threatened species of each country and stores it in list
        #Index is kept consistent with the countries in the region
        for i in self.countries:
            index = countries.index(i.lower())
            total_species = sum([x for x in threatened_data[index][1:]])
            self.total_species_list.append(total_species)
        
    def region_max_min_pop(self):
        '''Finds the highest and lowest population of all countries in the region chosen.
        Prints out the country and the value of that population, both for the highest and lowest.
        Bar graph is printed to represent the population of each country.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        pop_list = []
        #Goes through the countries and finds the most recent population number and adds to a list (index intact)
        for i in self.countries:
            index = countries.index(i.lower())#Lowered to match the list of countries that was lowered
            pop_list.append(population_data[index][-1])

        #Finds the max and min of that number and finds the country
        max_pop_region = max(pop_list)
        max_pop_country = self.countries[pop_list.index(max_pop_region)]
        min_pop_region = min(pop_list)
        min_pop_country = self.countries[pop_list.index(min_pop_region)]
        print('\nThe highest population in {} is {} with {}'.format(self.region_name,max_pop_country,max_pop_region))
        print('and the lowest population in {} is {} with {} (as of 2020).'.format(self.region_name,min_pop_country,min_pop_region))
        
        #Graphing
        ylabel_pop = correct_units(pop_list,'Population')
        plt.figure(num=3,figsize=(20,12),dpi=80)
        plt.bar(self.countries,pop_list,color='#87CEEB')
        plt.title(f'The population of each of the countries in {self.region_name}')
        plt.xticks(rotation=73)
        plt.xticks(self.countries)
        plt.xlabel(f'Countries in {self.region_name}')
        plt.ylabel(ylabel_pop)
        plt.show()


    def print_countries(self):
        '''Prints all the countries in a region and uses the print_neatly() function to print neatly.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        print(f'\nThe countries located in {self.region_name} are:\n')
        print_neatly(self.countries)
    
    def max_min_thr_species(self):
        '''Finds the country with the most and least threatened species in a region and prints 
        the country and the total of threatened species. Bar graph is printed to represent 
        information.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        #Finds the max of the total species list of countries in a region and find the country
        max_thr_species = max(self.total_species_list)
        max_country = self.countries[self.total_species_list.index(max_thr_species)]
        min_thr_species = min(self.total_species_list)
        min_country = self.countries[self.total_species_list.index(min_thr_species)]
        print('\nThe country in {} with the most threatened species is {} with {}'.format(self.region_name,max_country,max_thr_species))
        print('and the lowest is {} with {}.'.format(min_country,min_thr_species))

        #Graph
        plt.figure(num=4,figsize=(20,12),dpi=80)
        plt.bar(self.countries,self.total_species_list,color='#FF4500')
        plt.title(f'The total threatened species in each country in the region of {self.region_name}')
        plt.xticks(rotation=73)
        plt.xticks(self.countries)
        plt.xlabel('Countries')
        plt.ylabel('Number of Threatened Species')
        plt.show()
    
    def average_thr_species(self):
        '''Finds the average number of threatened species of each type of a whole region's countries
        and prints out the values and outputs a graph representing that metric.

        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        avg = np.average(self.total_species_list)
        plants_list = []
        fish_list = []
        birds_list = []
        mammals_list = []
        #Stores all values of thr species of each country in region, inside a list
        for i in self.countries: 
            index = countries.index(i.lower())
            plants_list.append(threatened_data[index][1])
            fish_list.append(threatened_data[index][2])
            birds_list.append(threatened_data[index][3])
            mammals_list.append(threatened_data[index][4])
        #Taking the average of each type of thr species and rounds it
        avg_plants = round(np.average(plants_list))
        avg_fish = round(np.average(fish_list))
        avg_birds = round(np.average(birds_list))
        avg_mammals = round(np.average(mammals_list))

        print(f'\nThe average number of threatened species throughout all of the countries in {self.region_name} is {avg:.0f}.')
        print('Average number of threatened species of all countries in {}:\nPlants: {}\nFish: {}\nBirds: {}\nMammals: {}\n'.format(self.region_name,avg_plants,avg_fish,avg_birds,avg_mammals))
        #X and Y of the bar graph
        types_list = ['Plants','Fish','Birds','Mammals']
        avg_thr_species_list = [avg_plants,avg_fish,avg_birds,avg_mammals]
        #Graphing
        plt.figure(num=5,figsize=(8,8),dpi=80)
        plt.bar(types_list,avg_thr_species_list,color='r')
        plt.title(f'The average number of threatened species of each type throughout all of {self.region_name}')
        plt.xlabel('Types of threatened species')
        plt.ylabel('The number of threatened species')
        plt.show()
    
    def max_min_growth(self):
        '''Finds the most growth in population for a country in a whole region in most recent times(last 5 years) 
        and prints it. Bar graph is shown to represent the information.
        
        Arguments: Self -- All the variables needed for this are stored in the object itself
        Return: None
        '''
        pop_change_list = []
        #Takes the average of growth of a country for its last 5 years
        for i in self.countries:
            index = countries.index(i.lower())
            change_population = []
            ind = 0
            domain = population_data[index][-5:]
            for i in domain:
                if ind != 0: #Skipping first entry so no error message pops up from index out of range
                    change_population.append(i - domain[ind-1])
                ind +=1
    
            pop_change_list.append(np.average(change_population))
        
        #Finds the highest and lowest entry and their respective countries
        max_growth = max(pop_change_list)
        max_country = self.countries[pop_change_list.index(max_growth)] #Finds index of number in the list and uses it in the countries of that region
        min_growth = min(pop_change_list)
        min_country = self.countries[pop_change_list.index(min_growth)]
        print('\nThe country with the biggest growth in population as of the most recent times (2015-2020) in {} is {} with {}'.format(self.region_name,max_country,round(max_growth)))
        print('and the lowest growth is {} with {}.'.format(min_country,round(min_growth)))

        #Graphing
        ylabel_pop = correct_units(pop_change_list,'Population Change')
        plt.figure(num=6,figsize=(20,12),dpi=80)
        plt.bar(self.countries,pop_change_list,color='#00FF00')
        plt.title(f'The population change of each of the countries in {self.region_name} between 2015-2020')
        plt.xticks(rotation=73)
        plt.xticks(self.countries)
        plt.xlabel(f'Countries in {self.region_name}')
        plt.ylabel(ylabel_pop)
        plt.show()


#FUNCTIONS
def correct_units(values_list,label_str):
    '''Gives the y axis title and y label of a graph the right units to not confuse the shortened y values
    
    Arguments: 
    values_list -- The y values of a graph to be interpreted
    label_str -- The text that is going to be on the y label of the graph

    Return: 
    The string with the right units for the values with the shortened notation
    '''
    chosen_str = label_str
    if max(values_list) >= 1000000000: #10 dig (billions)
        chosen_str += ' (billions)'
    elif max(values_list) >= 100000000: #9 dig
        chosen_str += ' (hundreds of millions)'
    elif max(values_list) >= 10000000: #8 dig
        chosen_str += ' (tens of millions)'
    elif max(values_list) >= 1000000: #7 dig
        chosen_str += ' (millions)'
    return chosen_str

def print_neatly(chosen_list):
    '''To print out a chosen list of entries in a neat and clean way of 5 x n format

    Arguments: chosen_list -- The list that is going to printed and organized

    Return: None
    '''
    num_iterations = 0
    for i in chosen_list:
        if num_iterations % 5 == 0: #To the list of countries neat
            print('\n',end='')
        if i == chosen_list[-1]: #If its the last country
            print('{}.'.format(i))
        else:
            print('{}, '.format(i),end='')
        num_iterations += 1

def list_choice(region_chosen):
    '''To list the choices of both regions and subregions to save space 
    
    Arguments: region_chosen -- the object chosen to make the choices
    
    Return: None
    '''
    second_option = True
    while second_option == True:
        user_input2 = input(f'''\nWhat do you want to know about the region {region_chosen.region_name}?
1. Lists of countries.
2. The country in {region_chosen.region_name} with the highest/lowest population as of 2020.
3. The country in {region_chosen.region_name} with the highest/lowest number of threatened species.
4. The average number of threatened species in {region_chosen.region_name}.
5. The country in {region_chosen.region_name} with biggest growth in population as of 2015-2020.\n6. Back\n\n''')

        if user_input2 == '1':
            region_chosen.print_countries()
        
        elif user_input2 == '2':
            region_chosen.region_max_min_pop()
        
        elif user_input2 == '3':
            region_chosen.max_min_thr_species()
        
        elif user_input2 == '4':
            region_chosen.average_thr_species()

        elif user_input2 == '5': #make new function for this option
            region_chosen.max_min_growth()
        
        elif user_input2 == '6':
            second_option = False
            break

        else:
            print('Input not correct. Type the number of your choosing from the list of options and press enter.\n')


#START OF THE  PROGRAM
print('''\nENDG 233 Final Project\nWelcome to the World Statistics program\n
Instructions:\n\n-Type in the country, region or subregion name that you want to know about.
-The name can be entered with or without capitals.\n-You can only type in the number when given a choice.\n-Type quit to stop the program.\n
If you want a list of choices (type in a number):\n1. Countries\n2. Regions\n3. Sub-regions\n''')
running = True

while running == True:
    user_input = input(f'\nWhat country/region/subregion do you want to know about? (type quit to end program)\n')

    #Country
    if user_input.lower() in countries:
        second_option = True
        country_index = countries.index(user_input.lower())
        country_chosen = Country(country_index)
        while second_option == True:

            user_input2 = input(f'''\nWhat do you want to know about {country_chosen.name}? (press the number you want to choose)\n
1. All the info on {country_chosen.name}.
2. Change in population over time.
3. The highest/lowest number of population between 2000 and 2020.
4. The threatened species in {country_chosen.name}.
5. Back\n''')
            #Choices
            if user_input2 == '1':
                country_chosen.print_all()
            
            elif user_input2 == '2':
                country_chosen.pop_change()
            
            elif user_input2 == '3':
                country_chosen.max_min_pop()

            elif user_input2 == '4':
                country_chosen.avg_thr_species()
            
            elif user_input2 == '5':
                second_option = False
                break

            else:
                print('Input not correct. Type the number of your choosing from the list of options and press enter.\n')

    #Region
    elif user_input.lower() in regions:
        region_chosen = Region(user_input.lower())
        list_choice(region_chosen)

    elif user_input.lower() in sub_regions:
        sub_region_chosen = Region(user_input.lower())
        list_choice(sub_region_chosen)
        
    #Print countries
    elif user_input == '1':
        print_neatly(countries)

    #Print regions
    elif user_input == '2':
        o = []
        for i in regions:
            if i not in o:
                o.append(i)
        print_neatly(o)

    #Print subregions
    elif user_input == '3':
        subregion_list = []
        for i in sub_regions:
            if i not in subregion_list:
                subregion_list.append(i)
        print_neatly(subregion_list)
        
    #To quit the program
    elif user_input.lower() == 'quit':
        running == False
        break
    else:
        print('\nInput not correct.')

print('\n\n\nThank you for using the program!\n')