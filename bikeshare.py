import time
import pandas as pd
from os import system

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_DATA = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

# Setting development to True will disable all inputs for better testing purposes
development = False

def format_duration(total_seconds):
    """
    Coverts the amount of seconds into 4 int variables representing the days, hours, minutes and seconds
    
    Returns:
        (int) days - amount of days for the seconds from the argument
        (int) hours - rest of the amount of hours for the seconds from the argument
        (int) minutes - rest of the amount of minutes for the seconds from the argument
        (int) seconds - rest of the amount of seconds for the seconds from the argument
    """
    duration = pd.Timedelta(seconds=total_seconds)
    days = duration.days
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    return days, hours, minutes, seconds

def five_chunker(iterable, step=5):
    """
    Gives back "step"-amount of items from "iterable" starting at start_index to start_index+step
    """
    i = 0
    while i < len(iterable):
        data = iterable.iloc[i:i+5]
        yield data
        i += step

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    valid_city, valid_month, valid_day = False, False, False
    print('Hello! Let\'s explore some US bikeshare data!')

    # Setting variables here for debugging purposes and faster development
    if development:
        valid_city, valid_month, valid_day = True, True, True
        city = "washington"
        month = "june"
        day = "monday"
    # Setting variables here for debugging purposes and faster development

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    system('cls')
    while not valid_city:
        print("\n\nYou can now explore bikeshare data for the cities of Chicago, New York City or Washington!")
        city = input("Please enter the city you would like to explore data on: ")
        if city.lower() in CITY_DATA:
            valid_city = True
            print("\nExcellent, you chose {} as the city to explore.".format(city.title()))
            break
        else:
            print("\n")
            for city_option in CITY_DATA:
                if city.lower() in city_option.lower():
                    user_input = input("If you meant {}, please type in 'y' and press Enter: ".format(city_option.title()))
                    if user_input.lower() == 'y':
                        city = city_option
                        valid_city = True
                        print("\nExcellent, you chose {} as the city to explore.".format(city.title()))
                        break
        if not valid_city:
            print("\n--- Invalid City Input---")
            print("Sorry, but {} is not part of the data you are able to explore.".format(city.title()))
            print("Please try again with one of the valid options.")
            
    # TO DO: get user input for month (all, january, february, ... , june)
    system('cls')
    while not valid_month:
        print("\n\nYou can explore the data for the months from january up to june or 'all'!")
        month = input("Please enter the month you would like to explore data on: ")
        if month.lower() in MONTH_DATA:
            valid_month = True
            print("\nExcellent, you chose {} as the month(s) to explore.".format(month.title()))
            break
        else:
            print("\n")
            for month_option in MONTH_DATA:
                if month.lower() in month_option.lower():
                    user_input = input("If you meant {}, please type in 'y' and press Enter: ".format(month_option.title()))
                    if user_input.lower() == 'y':
                        month = month_option
                        valid_month = True
                        print("\nExcellent, you chose {} as the month(s) to explore.".format(month.title()))
                        break
        if not valid_month:
            print("\n--- Invalid Month Input---")
            print("Sorry, but {} is not part of the data you are able to explore.".format(month.title()))
            print("Please try again with one of the valid options.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    system('cls')
    while not valid_day:
        print("\n\nYou can explore the data for specific days of the week or 'all'!")
        day = input("Please enter the day you would like to explore data on: ")
        if day.lower() in DAY_DATA:
            valid_day = True
            print("\nExcellent, you chose {} as the day(s) to explore.".format(day.title()))
            break
        else:
            print("\n")
            for day_option in DAY_DATA:
                if day.lower() in day_option.lower():
                    user_input = input("If you meant {}, please type in 'y' and press Enter: ".format(day_option.title()))
                    if user_input.lower() == 'y':
                        day = day_option
                        valid_day = True
                        print("\nExcellent, you chose {} as the day(s) to explore.".format(day.title()))
                        break
        if not valid_day:
            print("\n--- Invalid Day Input---")
            print("Sorry, but {} is not part of the data you are able to explore.".format(day.title()))
            print("Please try again with one of the valid options.")

    system('cls')
    print("These are your selected options: \nCity: {}\nMonth: {}\nDay: {}\n".format(city.title(), month.title(), day.title()))
    print('-'*40)
    if not development:
        input("Press any Enter to continue!")
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time and End Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Adding new columns 'hour', 'month', 'day_of_week' to the series
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        df = df[df['month'] == MONTH_DATA.index(month) + 1]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    print("\n")

    chunk_generator = five_chunker(df)
    while True:
        input_show = input("Type 'yes' to see raw data for 5 lines. ")
        if input_show == "yes":
            rows = next(chunk_generator)
            print(rows.to_string(index=False))
        else:
            break
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_counts = df['month'].value_counts()
    print("The most popular month is: {}, Count: {}".format(MONTH_DATA[month_counts.idxmax() - 1].title(), month_counts.max()))

    # TO DO: display the most common day of week
    day_counts = df['day_of_week'].value_counts()
    print("The most popular day is: {}, Count: {}".format(day_counts.idxmax().title(), day_counts.max()))

    # TO DO: display the most common start hour
    hour_counts = df['hour'].value_counts()
    print("The most popular hour is: {}, Count: {}".format(hour_counts.idxmax(), hour_counts.max()))

    print("\n" + "#"*20 + " This took %s seconds. " % (time.time() - start_time) + "#"*20)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_counts = df['Start Station'].value_counts()
    print("The most popular start station is: {}, Count: {}".format(start_counts.idxmax(), start_counts.max()))

    # TO DO: display most commonly used end station
    end_counts = df['End Station'].value_counts()
    print("The most popular end station is: {}, Count: {}".format(end_counts.idxmax(), end_counts.max()))

    # TO DO: display most frequent combination of start station and end station trip
    combined_column = df['Start Station'] + "|" + df['End Station']
    start_end_counts = combined_column.value_counts()
    print("The most popular start and end station combination is: {} and {}, Count: {}".format(start_end_counts.idxmax().split("|")[0], start_end_counts.idxmax().split("|")[1], start_end_counts.max()))

    print("\n" + "#"*20 + " This took %s seconds. " % (time.time() - start_time) + "#"*20)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time = df['Trip Duration'].sum()
    travel_days, travel_hours, travel_minutes, travel_seconds = format_duration(travel_time)
    print("The total travel time is {} day(s), {} hour(s), {} minute(s) and {} second(s)".format(travel_days, travel_hours, travel_minutes, travel_seconds))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    mean_days, mean_hours, mean_minutes, mean_seconds = format_duration(mean_time)
    print("The mean travel time is {} day(s), {} hour(s), {} minute(s) and {} second(s)".format(mean_days, mean_hours, mean_minutes, mean_seconds))

    print("\n" + "#"*20 + " This took %s seconds. " % (time.time() - start_time) + "#"*20)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Listing the different User Types and the amount of bike rentals:")
    user_counts = df['User Type'].value_counts()
    for user_type, user_count in user_counts.items():
        print("User Type: {}, Amount: {}".format(user_type, user_count))

    # TO DO: Display counts of gender
    if "Gender" in df:
        print("\nListing the Genders and the amount of bike rentals:")
        gender_counts = df['Gender'].value_counts()
        for gender_type, gender_count in gender_counts.items():
            print("Gender: {}, Amount: {}".format(gender_type, gender_count))
    else:
        print("\nNo data on Genders available.")

    # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("\nListing data for Birth Years:")
        birth_counts = df['Birth Year'].value_counts()
        print("The earliest year of birth is: {}, Amount: {}".format(int(df['Birth Year'].min()), birth_counts.loc[df['Birth Year'].min()]))
        print("The most recent year of birth is: {}, Amount: {}".format(int(df['Birth Year'].max()), birth_counts.loc[df['Birth Year'].max()]))
        print("The most common year of birth is: {}, Amount: {}".format(int(birth_counts.idxmax()), birth_counts.count()))
    else:
        print("\nNo data on Birth Year available.")

    print("\n" + "#"*20 + " This took %s seconds. " % (time.time() - start_time) + "#"*20)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        if development:
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()