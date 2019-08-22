# Necessary packages
import csv
import argparse

from operator import itemgetter
from datetime import datetime
from itertools import groupby


def parse_args():
    """
    Helper function that takes in the arguments passed in the shell to be used in the main script.

    Returns:
        args -- arguments
    """
    parser = argparse.ArgumentParser(description='Look for Border Crossing Statistics')
    parser.add_argument('--input', help="enter the input filename", type=str)
    parser.add_argument('--output', help="enter the output filename", type=str)
    args = parser.parse_args()
    return args


def output_list(masterlist):
    """
    Helper function that removes the extra brackets when outputting a list of lists into a csv file.
    Stackoverflow link: https://stackoverflow.com/questions/31587784/python-list-write-to-csv-without-the-square-brackets

    Keywords:
    masterList (list): input list of lists

    Returns:
    list: output list
    """
    #
    output = []
    for item in masterlist:

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

    Returns: length of set of dates
    """

    # Create a dates set
    dates_set = set()

    for row in another_list:
        if row[4] not in dates_set:
            dates_set.add(row[4])

    return len(dates_set)


def check_all_there(the_list):
    """ Helper function to make sure all is there"""
    for row in the_list:
        for i in range(len(row)):
            if not row[i]:
                raise ValueError('Ehh, empty list, sir!')
            else:
                return True


def main():
    """ Main function that takes in the input file of border crossing entry data and returns the statistics. """

    # Input and Output files from the shell script
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.output is None:
        raise ImportError('Did not specify the correct output file!')

    # Read in the border_crossing data
    with open(args.input, mode='r') as csv_file:

        # Read the CSV data into a list of lists
        # https://stackoverflow.com/questions/15990456/list-of-lists-vs-dictionary
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Sort the list by Border, Date, and Measure in descending order
        sorted_list = sorted(csv_reader, key=itemgetter(3, 5))

        # Make sure the sorted_list rows are not empty
        if check_all_there(sorted_list):
            pass

        # Let's group the sorted list via the keys--border names, dates, and measures, so
        # that we have a bunch of rows with the same border name, date, measure, but different values!
        # In each row, check if the 6th index (this is our value) is a number and is not 0!
        # If this is true, then add that those values together and create a new list
        # which holds this aggregated summation of values for each border name, date, and measure
        list_with_agg_values = [key + [sum([int(r[6]) for r in rows if r[6].isdigit() and int(r[6]) != 0])]
                                for key, rows in groupby(sorted_list, key=lambda x: x[3:6])]

        # x number of months
        num_of_months = count_the_months(sorted_list)

        list_with_avg = []
        # Going through the list of aggregated valves backwards
        # (constructed so that we are adding in the top down direction and bottom up)
        for i in range(len(list_with_agg_values)-1, 0, -1):
            each_row = list_with_agg_values[i]
            # Every x number of months we switch measures so restart the accumulator and counter
            if i % (num_of_months-1) == 0:
                accumulation, counter = 0, 0

            # Add up each value for each month between 1996 - 2019 + 2 extra months
            accumulation += each_row[3]

            # Similarly add for each month to the counter
            counter += 1

            # For each row, get the average value of crossing based for each measure and border
            each_row = each_row + [round(accumulation/counter)]

            # And keep track in the list
            list_with_avg.append(each_row)

        # Sort the list by Date, Value, Measure, Border in descending order
        sorted_list_with_val_border_measure = sorted(list_with_avg, key=itemgetter(3, 2, 0), reverse=True)
        final_sorted_list = sorted(sorted_list_with_val_border_measure,
                                   key=lambda x: datetime.strptime(x[1], '%d/%m/%Y %H:%M:%S %p'), reverse=True)

    # Write out to the output csv file
    with open(args.output, mode='w') as csv_outfile:
        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Column headers
        outfile_writer.writerow(['Border,Date,Measure,Value,Average'])

        # for each row in the final list, remove the list of list and create one list
        for row in final_sorted_list:
            outfile_writer.writerow(output_list(row))


if __name__ == '__main__':
    main()
