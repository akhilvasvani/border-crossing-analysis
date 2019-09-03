# Packages to import
import math
import pandas as pd


def my_round(i):
    """ Helper function for rounding.

    Keyword:
    (float) i : number to be inputted

    Returns:
    (int) f: number rounded up or down based on mathematical rounding rules
    """
    f = math.floor(i)
    return f if i - f < 0.5 else f+1


def output_list(master_list):
    """
    Helper function that removes the extra brackets when outputting a list of lists into a csv file.
    Stackoverflow link: https://stackoverflow.com/questions/31587784/python-list-write-to-csv-without-the-square-brackets

    Keywords:
    masterList (list): input list of lists

    Returns:
    list: output list
    """

    output = []
    for item in master_list:

        # check if item is a list
        if isinstance(item, list):

            # Append each item inside the list of list
            for i in output_list(item):
                output.append(i)

        # Otherwise just append the item (if not inside list of list)
        else:
            output.append(item)

    # return a single list without the nested lists
    return output


def count_the_months(another_list):

    """ Helper function designed to count the number of months.

    Keywords:
    (list) another_list: input list of all the dates (some are repeating)

    Returns: length of set of dates or dictionary if dates per each measure are different
    """

    # Create a dates set and a measure dictionary
    dates_set = set()
    measure_dict = dict()

    for row in another_list:

        # If the date is not in the set, then add it
        if row[1] not in dates_set:
            dates_set.add(row[1])

        # If the measure is in the dictionary, increase the count
        if row[2] in measure_dict:
            measure_dict[row[2]] += 1
        else:
            # Otherwise add it to the dictionary
            measure_dict[row[2]] = 1

    # Remove the column name Measure
    del(measure_dict['Measure'])

    # Check for an empty dictionary first if that's possible
    expected_value = next(iter(measure_dict.values()))
    all_equal = all(value == expected_value for value in measure_dict.values())

    return len(dates_set) if all_equal else measure_dict


def check_all_there(the_list):
    """ Helper function to make sure all of the elements are there.

    Keywords:
    (list) the_list: input list of everything

    Returns:
    (bool) True: if everything inside the list
    """

    # For each row in the list
    for row in the_list:

        # For each index in the row
        for i, item in enumerate(row):

            # If the row is empty, raise error
            if not row[i]:
                raise ValueError('Ehh, empty list, sir!')
            else:
                return True


def calculate_average_crossing_per_month_and_measure(num_of_months, list_with_agg_values):
    """ Helper function used to calculate the average crossings per month and per measure.

    Keywords:
    num_of_months (dict or list): the number of months based on the frequency of each measure

    list_with_agg_values (list): the list with Border, Date, Measure, and aggregated values

    Returns:
    list_with_avg (list): the list with the average crossing values per month and per measure
    """

    list_with_avg = []

    # Going through the list of aggregated valves backwards
    # the list was sorted with the most recent date up first, so hence we are adding from the
    # the bottom up and not top down direction
    for i in range(len(list_with_agg_values) - 1, 0, -1):
        each_row = list_with_agg_values[i]

        # Now check whether the number of the months per measure is the same or not:
        # If it's not, we going to calculate the average for each measure's frequency
        if isinstance(num_of_months, dict):
            for key, value in num_of_months.items():
                if each_row[2] == key:
                    if i % value == 0:
                        accumulation, counter = 0, 0
                        each_row = each_row + [0]
                    else:
                        # Add up each of the previous months' values
                        each_row_before = list_with_agg_values[i + 1]
                        accumulation += each_row_before[3]

                        # Similarly add for each month to the counter
                        counter += 1

                        # For each row, get the average value of crossing based for each measure and border
                        each_row = each_row + [my_round(accumulation / counter)]

                    # And keep track in the list
                    list_with_avg.append(each_row)
        else:
            # Otherwise, if the frequency is the same for all of the measures
            if i % (num_of_months - 1) == 0:
                accumulation, counter = 0, 0
                each_row = each_row + [0]
            else:
                # Add up each of the previous months' values
                each_row_before = list_with_agg_values[i + 1]
                accumulation += each_row_before[3]

                # Similarly add for each month to the counter
                counter += 1

                # For each row, get the average value of crossing based for each measure and border
                each_row = each_row + [my_round(accumulation / counter)]

            # And keep track in the list
            list_with_avg.append(each_row)

    return list_with_avg


def convert_date_to_sql(filename):
    """ Converts the date to the SQLite Datetime format"""

    # Read in the date
    df = pd.read_csv(filename, sep=',')

    # Because SQLite is particular about the Datetime format, I have to switch the format
    df['Date'] = pd.to_datetime (df.Date)
    df['Date'] = df['Date'].dt.strftime ('%Y-%m-%d %H:%M:%S %p')

    return df


def convert_date_back_to_original_format(filename):
    """ Converts Date back to the original format"""

    # '/home/akhil/border-crossing-analysis/output/report_SQL_test_small.csv'

    df = pd.read_csv(filename, sep=',')

    # Because SQLite is particular about the Datetime format, I have to switch the format
    df['Date'] = pd.to_datetime (df.Date)
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y %H:%M:%S %p')
    df.to_csv(path_or_buf=filename, index=False)


