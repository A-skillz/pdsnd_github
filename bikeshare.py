import time
import pandas as pd
import numpy as np



CITY_DATA = { 'chicago': 'chicago.csv',

              'new york city': 'new_york_city.csv',

              'washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    """

    print('\n Hello! Let\'s explore some U.S bikeshare data!\n')

    # get user input for city (chicago, new york city, washington).

    while True:
        cities= ['chicago','new york city','washington']
        city= input("\n Which city would you like to analyse? (Chicago,New york city,Washington) \n").casefold()
        if city in cities:
            break

        else:
            print("\n Please enter a valid city name")

    # get user input for month (january, february, ... , june or none)

    while True:
        months= ['January','February','March','April','May','June','None']
        month = input("\n Which month would you like to consider? \n<Within January to June>? Type 'None' for no month filter\n").title()
        if month in months:
            break

        else:
            print("\n Please enter a valid month")


    # get user input for day of week (monday, tuesday, ... sunday or none)

    while True:
        days= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','None']
        day = input("\n Which day of the week would you like to consider? Type 'None' for no day filter \n").title()
        if day in days:
            break

        else:
            print("\n Please enter a valid day")


    print(f"\n  You chosen to view data for the city: {city.title()}\n\n      Month of {month.title()} : Day of {day.title()}")


    print(f"\n")
    print('='*60)

    return city, month, day


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "None" to apply no month filter
        (str) day - name of the day of week to filter by, or "None" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable

    if month != 'None':

        # use the index of the months list to get the corresponding int

        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1

        # filter by month to create the new dataframe

        df = df[df['month']==month]

    # filter by day of week if applicable

    if day != 'None':

        # filter by day of week to create the new dataframe

        df = df[df['day_of_week']==day]

    return df


def time_stats(df,month,day):

    """Displays statistics on the most frequent times of travel."""

    print(' Calculating Popular Times of Travel')

    print('='*60)

    start_time = time.time()

    # display the most common month

    if month =='None':
        pop_month= df['month'].mode()[0]
        months= ['January','February','March','April','May','June']
        pop_month= months[pop_month-1]

        print("\nThe most Popular month is",pop_month)

    # display the most common day of week

    if day =='None':
        pop_day= df['day_of_week'].mode()[0]

        print("\nThe most Popular day is",pop_day)


    # display the most common start hour

    df['Start Hour'] = df['Start Time'].dt.hour
    pop_hour=df['Start Hour'].mode()[0]

    print("\nThe popular Start Hour is {}:00 hrs".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))

def station_stats(df):

    """Displays statistics on the most popular stations and trip."""
    print(f"\n")
    print('='*60)
    print(' Calculating The Most Popular Stations and Trip')
    print('='*60)

    start_time = time.time()

    # display most commonly used start station

    pop_start_station= df['Start Station'].mode()[0]

    print("\nThe most commonly used Start Station is {}\n".format(pop_start_station))

    # display most commonly used end station

    pop_end_station= df['End Station'].mode()[0]

    print("The most commonly used End Station is {}\n".format(pop_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))

def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""

    print(f"\n")
    print('='*60)
    print(' Calculating Trip Duration')
    print('='*60)

    start_time = time.time()

    # display total travel time

    total_duration=df['Trip Duration'].sum()
    minute,second=divmod(total_duration,60)
    hour,minute=divmod(minute,60)

    print("\nThe total trip duration: {} hour(s) {} minute(s) {} second(s)\n".format(hour,minute,second))

    # display average travel time

    average_duration=round(df['Trip Duration'].mean())
    m,sec=divmod(average_duration,60)

    if m>60:
        h,m=divmod(m,60)

        print("The average trip duration is: {} hour(s) {} minute(s) {} second(s)\n".format(h,m,sec))

    else:
        print("The average trip duration is: {} minute(s) {} second(s)\n".format(m,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))


def user_stats(df,city):

    """Displays statistics on bikeshare users."""
    print(f"\n")
    print('='*60)
    print(' Calculating User Information')
    print('='*60)

    start_time = time.time()

    # Display counts of user types

    user_counts= df['User Type'].value_counts()

    print("\nThe user types are:\n ",user_counts)


    # Display counts of gender

    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts= df['Gender'].value_counts()

        print("\nThe counts of each gender are: \n",gender_counts)

    else:
        print('\n')
        print('='*60)
        print("There is no 'Gender' column in this city")
        print('='*60)

    # Display earliest, most recent, and most common year of birth

    if city.title() == 'Chicago' or city.title() == 'New York City':

        #("\ncalculate the most earliest birth year)

        earliest= int(df['Birth Year'].min())

        #("\ncalculate the most recent birth year)

        most_recent= int(df['Birth Year'].max())

       #("calculate The most common year of birth)

        common= int(df['Birth Year'].mode()[0])

        #print("Earliest year of birth: {}\n\nMost recent year of birth: {}\n\nMost common year of birth")

        print('\n')
        print('='*60)
        print("\nEarliest year of birth: {}\n\nMost recent year of birth: {}\n\nMost common year of birth: {}".format(earliest,
                         most_recent,common))
        print('='*60)

    else:
         print('\n')
         print('='*60)
         print("There is no 'earliest', 'most recent', and 'most common year of birth' column in this city")
         print('='*60)

    print("\nThis took %s seconds." % (time.time() - start_time))


def display_data(df):

    while True:
        response=['yes','no']
        choice= input("\nWould you like to view 5 Records of Bikeshare data? Type 'yes' or 'no'\n").lower()

        if choice in response:
            if choice=='yes':
                start=0
                end=5
                data = df.iloc[start:end,:9]

                print(data)

            break
        else:
            print("Please enter a valid response")

    if  choice=='yes':
            while True:
                choice_2= input("\nWould you like to view 5 more Records of Bikeshare data? Type 'yes' or 'no'\n").lower()

                if choice_2 in response:
                    if choice_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                    else:
                        break

                else:
                    print("Please enter a valid response")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart Bikeshare Program? Enter yes or no.\n')
        
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
