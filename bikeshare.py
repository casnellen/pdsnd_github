import time
import pandas as pd
import numpy as np



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    print("Which city would you like to look at?")
    city = str(input()).lower()
    
    # Test that the user input is in the appropriate responses.
    while city not in ["chicago", "new york city", "washington"]:
        print("We don't have information on that city. Please choose from the following: Chicago, New York City, Washington")
        city = str(input()).lower()
     

    # Get user input for month (all, january, february, ... , june).
    print("Which month would you like to look at?")
    month = str(input()).lower()
    # Test that the user input is in the appropriate responses.
    while month not in ["all","january","february","march","april","may","june"]:
        print("Invalid month. Please choose a specific month or for all of them choose 'all'")
        month = str(input()).lower()
     

    # Get user input for day of week (all, monday, tuesday, ... sunday).
    print("Which day of the week would you like to look at?")
    day = str(input()).lower()
    # Test that the user input is in the appropriate responses.
    while day not in ["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
        print("Invalid day. Please choose a specific day of the weel or for all of them choose 'all'")
        day = str(input()).lower()

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
    # Provides a dictionary of available cities and their associated files.
    CITY_FILES = {"new york city": "new_york_city.csv", "chicago":"chicago.csv", "washington":"washington.csv"}
    
    # Transform csv into pandas dataframe.
    city_df = pd.read_csv(CITY_FILES[city])
    # Convert times into a tijme object.
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    city_df['End Time'] = pd.to_datetime(city_df['End Time'])
    # Get month and day of week from the start time.
    city_df['month'] = city_df['Start Time'].dt.month
    city_df['day_of_week'] = city_df['Start Time'].dt.weekday_name
    
    # Filter data based on month filter.
    if month != 'all':
        months =  ["january","february","march","april","may","june"]
        month = months.index(month) + 1
        city_df = city_df[city_df['month'] == month]
    
    # Filter data based on day filter.
    if day != 'all':
        city_df = city_df[city_df['day_of_week'] == day.title()]

    return city_df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    pop_month  = df["month"].mode()[0]
    months =  ["January","February","March","April","May","June"]
    print("The most common month is: " + months[(pop_month-1)])


    # Display the most common day of week.
    pop_dow  = df["day_of_week"].mode()[0]
    print("The most common day of the week is: " + str(pop_dow))

    # Display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    pop_hour  = df["hour"].mode()[0]
    print("The most common start hour is: " + str(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # Display most commonly used start station.
    pop_start_station  = df["Start Station"].mode()[0]
    print("The most common start station is: " + str(pop_start_station))


    # Display most commonly used end station.
    pop_end_station  = df["End Station"].mode()[0]
    print("The most common end station is: " + str(pop_end_station))


    # Display most frequent combination of start station and end station trip.
    df["Trip"] = df[['Start Station', 'End Station']].agg(' to '.join, axis=1)
    pop_trip  = df["Trip"].mode()[0]
    print("The most common trip is: " + str(pop_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # Calculate travel time for each race.
    df["Travel Time"] = (df["End Time"] - df["Start Time"])
    
    # Display total travel time.
    total_travel = df["Travel Time"].sum()
    print("Total travel time is: ", total_travel)

    # Display mean travel time.
    total_travel = df["Travel Time"].mean()
    print("Mean travel time is: ", total_travel)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types.
    user_counts = df.groupby(["User Type"], as_index=False).count()
    print("Counts of users are: ")
    for user in user_counts["User Type"]:
        print("\t" + str(user) + ": " + str(user_counts[user_counts["User Type"] == user]["Start Time"].values[0]))
    
    # Display counts of gender.
    if "Gender" in df.columns:
        gender_counts = df.groupby(["Gender"], as_index=False).count()
        print("\r\nCounts of genders are: ")
        for gender in gender_counts["Gender"]:
            print("\t" + str(gender) + ": " + str(gender_counts[gender_counts["Gender"] == gender]["Start Time"].values[0]))
    else: 
        print("There is no gender information in this file")
    
    # Display earliest, most recent, and most common year of birth.
    if "Birth Year" in df.columns:
        min_birthyear = df["Birth Year"].min()
        max_birthyear = df["Birth Year"].max()
        most_birthyear = df["Birth Year"].mode()[0]

        print("\r\nBirth year breakdown is: ")
        print("\tEarliest birth year: ", int(min_birthyear))
        print("\tMost recent birth year: ", int(max_birthyear))
        print("\tMost common birth year: ", int(most_birthyear))
    else: 
        print("There is no birth year information")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """Gathers user input and calculates different stats based on the data from the filters."""
    while True:
        # Get user filters.
        city, month, day = get_filters()
        # Load the data.
        df = load_data(city, month, day)
        # Calculate and print time stats.
        time_stats(df)
        # Calculate and print station stats.
        station_stats(df)
        # Calculate and print trip stats.
        trip_duration_stats(df)
        # Calculate and print user stats.
        user_stats(df)
        
        # Ask the user is they want to see the raw data.
        display = input('\nWould you like to display the raw data? Enter yes or no.\n')
        if display.lower() == 'yes':
            idx = 0 
            # Keep displaying 5 rows of the data until the user says no.
            while display == "yes":
                subset = df.iloc[idx:(idx+5)]
                print(subset)
                idx = idx+5
                display = input('\nWould you like to display the next 5 rows of data? Enter yes or no.\n')
                
            
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
