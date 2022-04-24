import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['january', 'february', 'march', 'april', 'may', 'june','all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday','all']


def get_filters():

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city  = input("Enter the name of the city that you would like to view the stats for : ").lower().strip()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input("This city does not exist in the database! Enter another city name : ").lower().strip()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter the month for which you would like to view the stats. Enter 'all' to view all months : ").lower().strip()
    while month not in months:
        month = input("This month does not exist in the database! Enter another month or enter 'all' to view all months : ").lower().strip()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter the day of the week that you would like to view the stats for : ").lower().strip()
    while day not in days:
        day = input("This day does not exist! Enter another day or enter 'all' to view all days :").lower().strip()

    print('-'*40)
    return city, month, day


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower().strip()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])


    #create new columns
    df['month'] = df['Start Time'].dt.month #month
    df['day_of_week'] = df['Start Time'].dt.dayofweek #day of the week
    df['start_hour'] = df['Start Time'].dt.hour #start hour
    df['start_end_station'] = df["Start Station"] + ' - ' + df["End Station"] #combined start and end station combination
    df['trip_duration_minutes'] = df['Trip Duration']/60 #trip duration in minutes

    # filter by month if applicable
    if month != 'all':
        month_str = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month_str]

    # filter by day of week if applicable
    if day != 'all':
        day_str = days.index(day)
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day_str]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month of travel is : ' + months[(df.loc[:,"month"].mode()[0])-1].title())

    # display the most common day of week
    print('The most common day of travel is : ' + days[(df.loc[:,"day_of_week"].mode()[0])].title())

    # display the most common start hour
    print('The most common start hour is : ' + str(df.loc[:,"start_hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is : ' + (df.loc[:,"Start Station"].mode()[0]).title())

     # display most commonly used end station
    print('The most commonly used end station is : ' + (df.loc[:,"End Station"].mode()[0]).title())

    # display most frequent combination of start station and end station trip
    print('The most commonly used end station is : ' + (df.loc[:,"start_end_station"].mode()[0]).title())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time in minutes is ' + str(df['trip_duration_minutes'].sum()))


    # display mean travel time
    print('mean traveltime per trip in minutes is ' + str(df['trip_duration_minutes'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of user types : \n')
    # Display counts of user types
    print(df['User Type'].value_counts())

        # Display counts of gender
    if city != 'washington':
        print('\nCounts of gender : \n')
        print(df['Gender'].value_counts())

    # Display earliest year of birth
    if city != 'washington':
        print('\nThe earliest year of birth is : ' + str(df['Birth Year'].min()))

    # Display most recent year of birth
    if city != 'washington':
        print('\nThe most recent year of birth is : ' + str(df['Birth Year'].max()))

    # Display most common year of birth
    if city != 'washington':
        print('\nThe most common year of birth is : ' + str(df['Birth Year'].mode()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_selected_data(df):

    #set row limits
    counter = 0
    upper_lim = 4

    while True:

        if counter == 0:
            see_data_flg = input(" Do you want to see the first 5 rows of the selected data? Type 'yes' to see or 'no' to exit ").lower().strip()
        else:
            see_data_flg = input(" Do you want to see the next 5 rows of the selected data? Type 'yes' to see or 'no' to exit ").lower().strip()

        if see_data_flg == 'yes':
            while counter <= upper_lim:
                print(df.iloc[[counter]])
                counter = counter + 1

        upper_lim = upper_lim + 5

        if see_data_flg == 'no':
            break

        if see_data_flg not in ['yes','no']:
            print('Invalid Input : please enter yes to see the data or no to exit')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)

        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_selected_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
