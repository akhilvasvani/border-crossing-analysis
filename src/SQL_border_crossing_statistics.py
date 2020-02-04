"""This script performs the same operation as in border_crossing_statistics, except
 it uses SQL."""

import csv
import sqlalchemy as db

from utils import convert_date_to_sql, convert_date_back_to_original_format, \
    parse_args


def main():
    """Using the specified border crossing entry data (input file),
       returns the desired statistics. """

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
    # From that subquery, we are going to select the measure and where the
    # (current) date is > than the previous, and create a average cumulative sum
    # -- we make sure to round if there is nothing (hence, starts the average)

    # Write out to the output csv file:
    with open(args.output, mode='w') as csv_outfile:

        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_NONE)

        # Column headers--Don't quote them
        outfile_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])

        for row in engine.execute("WITH crossings as ("
                                    "SELECT Border, Date, Measure, SUM(VALUE) "
                                  "as SumField "
                                    "FROM bct "
                                    "GROUP BY Border, Date, Measure "
                                    "ORDER BY Date DESC, SumField DESC, "
                                  "Measure DESC, Border DESC"
                                  ") "
                                  "SELECT Border, Date, Measure, SumField,"
                                  "ifnull((SELECT cast(round(avg(c2.SumField),"
                                  " 0) AS INTEGER) "
                                            "FROM crossings AS c2 "
                                            "WHERE c2.Border = c.Border "
                                                "AND c2.Measure = c.Measure "
                                                "AND c2.Date < c.Date),0) AS Average "
                                  "FROM crossings AS c "
                                    "ORDER BY Date DESC, SumField DESC, Border,"
                                  " Measure DESC;"):

            outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)

            # for each row in the final list, remove the list of list and create one list
            outfile_writer.writerow(row)

    convert_date_back_to_original_format(args.output)


if __name__ == "__main__":
    main()
