# Do the same things as in border_crossing_statistics using SQL

# Packages
from utils import convert_date_to_sql, convert_date_back_to_original_format

import csv
import sqlalchemy as db
import argparse


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


def main():

    # Input and Output files Error-Handling
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.output is None:
        raise ImportError('Did not specify the correct output file!')

    engine = db.create_engine('sqlite://', echo=False)

    df = convert_date_to_sql(args.input)

    df.to_sql("bct", con=engine, if_exists='fail', index=False)

    # The first subquery gets the Border, Date, Measure, and Total Sum Value
    #
    # Write out to the output csv file: '/home/akhil/border-crossing-analysis/output/report_SQL_test_small.csv'
    with open(args.output, mode='w') as csv_outfile:

        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)

        # Column headers--Don't quote them
        outfile_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])

        for row in engine.execute("WITH crossings as ("
                                    "SELECT Border, Date, Measure, SUM(VALUE) as SumField "
                                    "FROM bct "
                                    "GROUP BY Border, Date, Measure "
                                    "ORDER BY Date DESC, SumField DESC, Measure DESC, Border DESC"
                                  ") "
                                  "SELECT Border, Date, Measure, SumField,"
                                  "ifnull((SELECT cast(round(avg(c2.SumField), 0) AS INTEGER) "
                                            "FROM crossings AS c2 "
                                            "WHERE c2.Border = c.Border "
                                                "AND c2.Measure = c.Measure "
                                                "AND c2.Date < c.Date),0) AS Average "
                                  "FROM crossings AS c "
                                    "ORDER BY Date DESC, SumField DESC, Border, Measure DESC;"):

            outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            # for each row in the final list, remove the list of list and create one list
            outfile_writer.writerow(row)

    convert_date_back_to_original_format(args.output)


if __name__ == "__main__":
    main()
