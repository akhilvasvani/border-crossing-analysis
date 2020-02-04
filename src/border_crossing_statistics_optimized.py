""" This script performs border crossing statistics via an optimized method
    of Nested Dictionaries. The output csv file is ordered by
    Date, Value, Measure, and Border."""

import csv

from utils import NestedDict, find_average, write_to_csv, parse_args


def main():
    """Using the specified border crossing entry data (input file),
       returns the desired statistics. """

    # Read in the border_crossing data
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.output is None:
        raise ImportError('Did not specify the correct output file!')

    with open(args.input, mode='r') as csv_file:

        result = NestedDict()
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:

            # These are the keys
            path = [row['Border'], row['Measure'], row['Date'], int(row['Value'])]

            # The integer values
            result[path] = 0

        final_list = find_average(result)

    write_to_csv(args.output, final_list)


if __name__ == '__main__':
    main()
