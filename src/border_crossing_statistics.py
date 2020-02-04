""" This script performs border crossing statistics via an optimized keeping a running
    cumulative average of each measure. The output csv file is ordered by
    Date, Value, Measure, and Border."""

# Necessary packages
import csv

from operator import itemgetter
from datetime import datetime
from itertools import groupby

# import helper functions from util file
from utils import count_the_months, check_all_there, parse_args
from utils import calculate_average_crossing_per_month_and_measure, write_to_csv


def main():
    """Using the specified border crossing entry data (input file),
        returns the desired statistics. """

    # Input and Output files Error-Handling
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.output is None:
        raise ImportError('Did not specify the correct output file!')

    # Read in the border_crossing data
    with open(args.input, mode='r') as csv_file:

        # Read the CSV data into a list of lists
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Sort the list by Border, Date, and Measure in descending order
        sorted_list = sorted(csv_reader, key=itemgetter(3, 5))

        # Make sure the sorted_list rows are not empty
        if check_all_there(sorted_list):
            pass

        # Let's group the sorted list via the keys--border names, dates,
        # and measures, so that there are rows with the same border name, date,
        # measure, but different values! In each row, check if the
        # 6th index (this is our value) is a number and is not 0! If true, then
        # add those values together and create a new list, which holds this aggregated
        # summation of values for each border name, date, and measure
        list_with_agg_values = [key +
                                [sum([int(r[6]) for r in rows if r[6].isdigit()
                                      and int(r[6]) != 0])]
                                for key, rows in groupby(sorted_list,
                                                         key=lambda x: x[3:6])]

        # x number of months -- could be a dictionary or int
        num_of_months = count_the_months(list_with_agg_values)

        # calculate the average crossing per month and per measure
        list_with_avg = calculate_average_crossing_per_month_and_measure(num_of_months,
                                                                         list_with_agg_values)

        # Sort the list by Date, Value, Measure, Border in descending order
        sorted_list_with_vbm = sorted(list_with_avg, key=itemgetter(3, 2, 0),
                                      reverse=True)
        final_sorted_list = sorted(sorted_list_with_vbm,
                                   key=lambda x: datetime.strptime(x[1],
                                                                   '%d/%m/%Y %H:%M:%S %p'),
                                   reverse=True)
    write_to_csv(args.output, final_sorted_list)


if __name__ == '__main__':
    main()
