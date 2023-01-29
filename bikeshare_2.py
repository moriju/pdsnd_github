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
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington? Choose: ").lower()
    while city not in ["chicago", "new york city", "washington"]:
        city = input("Please choose Chicago, New York City or Washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month? Please choose: All, January, February, March, April, May, June: ").lower()
    while month not in ["all","january", "february", "march", "april", "may", "june"]:
        month = input("Please choose ALL, January, February, March, April, May, June: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day? Please choose: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ").lower()
    while day not in ["all","monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        day = input("Please choose: All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load file to df
    df = pd.read_csv(CITY_DATA[city])
    #date convertion
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)
    # display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]
    print('Most Popular Start Day Of Week:', popular_dow)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\nMost Popular Start Station:\n', start_station)


    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nMost Popular End Station:\n', end_station)


    # display most frequent combination of start station and end station trip
    df['Combined Station'] = df['Start Station'] + ' / ' + df['End Station']
    most_frequent_station_from_to =  df['Combined Station'].mode()[0]
    print ('\nMost frequent combination of start station and end station trip:\n', most_frequent_station_from_to)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("\nTotal travel time (hours): ", df['Trip Duration'].sum()//3600)

    # display mean travel time
    print("\nMean travel time (minutes): ", df['Trip Duration'].mean()//60)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nDisplay counts of user types:\n", df['User Type'].value_counts())

    # Display counts of gender
    try:
        print("\nCounts of user gender:\n", df['Gender'].value_counts())
    except KeyError:
        print("\nNo Gender data for Washington, sorry")

    # Display earliest, most recent, and most common year of birth

    try:
       birth_year = df['Birth Year']
       print("\nEarliest year of birth: ", int(birth_year.min()))
       print("\nMost recent year of birth: ", int(birth_year.max()))
       print("\nMost common year of birth: ", int(birth_year.value_counts().idxmax()))
    except KeyError:
        print("\nNo Birth Year for Washington, sorry")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#script prompts the user if they want to see 5 lines of raw data
def raw_data (df):
    print("\nPress enter to see row data, press no to skip\n")
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
