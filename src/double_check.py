# Necessary packages
import csv
import os
import pandas as pd


def main():
    # Splits up the absolute path of current working directory
    (head, tail) = os.path.split(os.getcwd())

    # Read in the border_crossing data
    data = pd.read_csv(os.path.join(head, 'input/Border_Crossing_Entry_Data.csv'))
    print(data[['Date', 'Value']])

# Port Name
# State
# Port Code
# Border
# Date
# Measure
# Value
# Location

if __name__ == '__main__':
    main()


    def get_value(value_stack):
        # border = 'US-Canada Border', date = '03/01/2019 12:00:00 AM', measure = 'Trains'

        total_value = sum (value_stack)
        average = round (total_value / len (value_stack))
        # print(total_value, average)
        return total_value, average
        # return sum(value_stack), int(round(sum(value_stack)//len(value_stack)))


    def find_the_values(new_list, borders, dates, measures):  # row
        """ Find the values from each row """
        # count, value_total = 0, 0
        temp = []
        value_stack = list ()
        for i in range (1, len (new_list)):  # csv_reader:
            row = new_list[i]
            # if (row[3] in borders and row[4] in dates) and row[5] in measures:
            #     if int(row[6]) != 0:
            #         count += 1
            #     value_total += int(row[6])
            #     # temp.append([row[3], row[4], row[5], row[6]])
            #     print(row[3], row[4], row[5], value_total)
            # # print(row[3], row[4], row[5], row[6], count)
            # else:
            #     value_total = 0
            #     count = 0

            if row['Border'] == 'US-Canada Border' and (
                    row['Date'] == '03/01/2019 12:00:00 AM' and row['Measure'] == 'Trains'):
                if int (row['Value']) != 0:
                    value_stack.append (int (row['Value']))

                    total_value, average = get_value (value_stack)
                    print (total_value, average)
                # print(row[6])
            # for border in borders:
            #     for date in dates:
            #         for measure in measures:
            #         if row[3] == border and (row[4] == date and row[5] == measure):
            #             print(row[3], row[4], row[5], row[6])
            # get_value(row)
            # count += 1
            # if count > 1:
            #     print(row[3], row[4], row[5], row[6], count)
            # new_list.append([row[3], row[4], row[5], row[6], count])
            # else:
            #     count = 0

        # date_and_measure = {k:v if k == row[4] and v == row[5]}
        # measure_and_value = {row[5]: row[6]}
        # value_and_counts = {}

        # TRASH:
        # for key, rows in groupby(new_list, key=lambda x: x[3:6]): # (x[3], x[4], x[5])
        #     print(key, sum(int(r[6]) for r in rows if r[6].isdigit() and int(r[6]) != 0))

    # Read the csv_file into an ordered dictionary
    # csv_reader = csv.DictReader(csv_file)
    # new_list = sorted(csv_reader, key=itemgetter('Border', 'Date', 'Measure'), reverse=True)
    # for key, rows in itertools.groupby(new_list, key=lambda x: (x['Border'], x['Date'], x['Measure'])):
    #     rows = tuple(rows)
    #     print(key, rows)

    # BRUTE FORCE solution:
    # get the list of unique dates, measures, borders. whatever. (iterate once through the list)
    # iterate through the list again to look for the specific types

    # For each row, we have a saved an ordered_dictionary with the keys as the column names
    # We iterate through each row, keeping the date the same, but sort by the measure
    # We should record the following information:
    # the border, the data + time, the VEHiCLE Type, and count the value

    # Create a dictionary that associates the Border with the specific data
    # if row[3] not in border_dict.keys():
    #     border_dict[row[3]] = row[4]
    # if row[4] in border_dict.values():
    #     print('Bad')
    #

# print(borders)
# print(len(dates))