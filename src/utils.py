"""Script contain helper functions for border crossing analysis. """

# Packages to import
import math
import pandas as pd
import pathlib
import errno
import csv
import os
import argparse

from operator import itemgetter
from datetime import datetime
from itertools import chain


def my_round(my_number):
    """Rounds a number based on the rule: if a number is 4 or less
        then round down, otherwise round up.

    Args:
        my_number: the float number as input

    Returns:
        f: an integer rounded up or down based on the round rule.
    """
    f = math.floor(my_number)
    return f if my_number - f < 0.5 else f+1


def parse_args():
    """Parses arguments passed in the shell to be used in the main function.

    Returns:
        args -- arguments
    """
    parser = argparse.ArgumentParser(description='Look for Border Crossing Statistics')
    parser.add_argument('--input', help="enter the input filename", type=str)
    parser.add_argument('--output', help="enter the output filename", type=str)
    args = parser.parse_args()
    return args


"""Functions used for Original (Brute Force) Script"""


def output_list(master_list):
    """Removes the extra brackets when outputting a list of lists
       into a csv file.

    Args:
        masterList: input list of lists

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
    """Counts the number of months.

    Args:
        another_list: input list of all the dates (some are repeating)

    Return:
        length of set of dates or dictionary if dates per each measure are different
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
    """Checks if all of the elements are not None or
       if there is an empty list.

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
    """Calculates the average crossings per month and per measure.

    Args:
        num_of_months: the number of months based on the
                       frequency of each measure, saved as
                       a dict or a list.

        list_with_agg_values: the list with Border, Date, Measure,
                              and aggregated values.

    Returns:
        list_with_avg (list): the list with the average crossing values
                              per month and per measure
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


def write_to_csv(name_of_output_file, final_list):
    """ Writes the file out to csv file row by row.

    Args:
        name_of_output_file: name of the output file
        final_list: the list which holds all the border data information

    Raises:
        OSError: If the file does in fact exist
        FileNotFoundError: If the file is not found
    """

    try:
        filepath = name_of_output_file
    except OSError:
        if pathlib.Path(name_of_output_file).resolve(strict=True):
            pass
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    name_of_output_file)

    # Write out to the output csv file
    with open(filepath, mode='w') as csv_outfile:
        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_NONE)

        # Column headers--Don't quote them
        outfile_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])

        outfile_writer = csv.writer(csv_outfile, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)

        # for each row in the final list, remove the list of list
        # and create one list
        for row in final_list:
            outfile_writer.writerow(row)


"""Functions used for SQL Script"""


def convert_date_to_sql(filename):
    """ Converts the date to the SQLite Datetime format"""

    # Read in the date
    df = pd.read_csv(filename, sep=',')

    # Because SQLite is particular about the Datetime format,
    # I have to switch the format
    df['Date'] = pd.to_datetime(df.Date)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d %I:%M:%S %p')

    return df


def convert_date_back_to_original_format(filename):
    """ Converts Date back to the original format"""

    df = pd.read_csv(filename, sep=',')

    # Because SQLite is particular about the Datetime format,
    # I have to switch back to the original format
    df['Date'] = pd.to_datetime(df.Date)
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y %I:%M:%S %p')
    df.to_csv(path_or_buf=filename, index=False)


"""Functions {and Class} used for Optimized Script"""


class NestedDict(dict):
    """
    Class for managing nested dictionary structures. Normally, it works
    like a builtin dictionary. However, if it gets a list as an argument,
    it will iterate through that list assuming all elements of that list
    as a key for the subdirectory chain.

    NestedDict implements module level functions and makes managing nested
    dictionary structure easier.

    Instead of having a complicated way to manage extending or
    overwriting, NestedDict has a lock property (not decorated!) which
    allows or prohibits all alterations on the particular NestedDict
    instance. Warning! If you do not pass a list (even if it has only one
    element) to __setitem__, the superclass' method will be used which
    sets the item regardless of lock state!

    If you want more sophisticated behavior than full access/prohibition,
    you can still use module level functions.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = False

    def __getitem__(self, *args):
        if isinstance(args[0], list):
            return getitem(self, args[0])
        return super().__getitem__(*args)

    def __setitem__(self, *args):
        if isinstance(args[0], list):
            lock = self.get_lock(args[0])
            if not lock:
                return setitem(self, args[0], args[1],
                               overwrite=not lock, restruct=not lock,
                               dict_type=type(self))
            else:
                return False
        else:
            super().__setitem__(*args)
            return True

    def get_lock(self, path):
        """
        Returns the state of lock on the given path. In fact it walks on
        the path as long as possible, and returns the state of the last
        lock it can get.
        """
        lock = self.lock
        level = 1
        while level <= len(path):
            try:
                lock = getitem(self, path[:level]).lock
            except (KeyError, AttributeError):
                break
            level += 1
        return lock

    def func_if_unlocked(self, *args):
        """
        The default func_if_unlocked function for self.merge() method
        which checks for lock on a path and returns True if path is
        unlocked.
        """
        path = args[0]
        return not self.get_lock(path)

    def lock_close(self, recursively=True):
        """
        Locks locks.
        """
        self.lock = True
        if recursively:
            for p in self.paths(of_values=False):
                self.__getitem__(p).lock = True

    def lock_open(self, recursively=True):
        """
        Unlocks locks.
        """
        self.lock = False
        if recursively:
            for p in self.paths(of_values=False):
                self.__getitem__(p).lock = False

    def merge(self, *dictobjs, restruct=True):
        """
        Same as module level function merge. It needs less arguments
        though since it uses self.func_if_unlocked() method to manage
        extend and overwrite permissions.
        """
        merge(self, *dictobjs,
              func_if_extend=self.func_if_unlocked,
              func_if_overwrite=self.func_if_unlocked,
              restruct=restruct,
              dict_type=type(self))

    def paths(self, of_values=True):
        """
        Same as module level function paths.
        """
        return paths(self, of_values=of_values)


def getitem(dictobj, path):
    """
    Returns the element of a nested dictionary structure which is on the
    given path.
    """
    _validate_path(path)
    if len(path) == 1:
        return dictobj[path[0]]
    else:
        return getitem(dictobj[path[0]], path[1:])


def setitem(dictobj, path, value, overwrite=True, restruct=True,
        dict_type=dict):
    """
    Sets a dictionary item on a given path to a given value.
      - Returns True if value on path has been set.
      - Returns False if there was a value on the given path which was not
        overwritten by the function.
      - Returns None if there was a value on the given path which was
        identical to value.

    If restruct=True then when a value blocks the path, that value get
    cleared by an empty dictionary to make way forward.
    """
    _validate_path(path)

    try:
        one_step = dictobj[path[0]]
    except KeyError:
        if len(path) == 1:
            dictobj[path[0]] = value
            return True
        else:
            dictobj[path[0]] = dict_type()
            one_step = dictobj[path[0]]
    else:
        if len(path) == 1 and one_step == value:
            return None
        elif len(path) == 1 and overwrite is False:
            return False
        elif len(path) == 1 and overwrite is True:
            dictobj[path[0]] = value
            return True
        else:
            if not isinstance(one_step, dict):
                if overwrite is True and restruct is True: ##TEST
                    dictobj[path[0]] = dict_type()
                    one_step = dictobj[path[0]]
                else:
                    return False
    return setitem(one_step, path[1:], value, overwrite=overwrite,
                restruct=restruct, dict_type=dict_type)


def paths(dictobj, of_values=True, past_keys=[]):
    """
    Generator to iterate through branches. Used by merge function, but
    can be useful for other object management stuffs.

    By default it returns paths of values. However, if of_values=False
    then it returns the paths of all subdirectories.
    """
    for key in dictobj.keys():
        path = past_keys + [key]
        if not isinstance(dictobj[key], dict):
            if of_values is True:
                yield path
        else:
            if of_values is False:
                yield path
            yield from paths(dictobj[key], of_values=of_values,
                             past_keys=path)


def merge(*dictobjs,
          func_if_extend=True,
          func_if_overwrite=True,
          restruct=True,
          dict_type=dict,
          return_new=False):
    """
    Merges one dictionary with one or more another.

    By default it mutates the first dictobj. However, if return_new=True
    then it returns a new dictionary object typed recursively to
    dict_type. If you want no retypeing, use copy.deepcopy(), and pass the
    copied dictionary as first argument.

    To make mergeing more flexible, you are able to control how extension
    overwriting should be done (both are allowed by default). By setting
    func_if_overwrite to False, overwriting becomes disabled. By setting
    func_if_extend to False, extension becomes disabled and you can only
    update existing values if overwriting is enabled. If both are
    disabled, no alteration will be made, so this scenario makes no sense,
    but allowed.

    Moreover you can pass functions to the two mentioned arguments which
    will be called with the path (list of keys), dictobj1, dictobj2
    arguments and expected to return True or False.
    """
    if return_new is True:
        d = retype(dictobjs[0], dict_type)
    elif return_new is False:
        d = dictobjs[0]

    for dictobj in dictobjs[1:]:
        for p in paths(dictobj):
            try:
                getitem(d, p)
            except KeyError:
                    if hasattr(func_if_extend, '__call__'):
                        ex = func_if_extend(p, d, dictobj)
                    else:
                        ex = func_if_extend
                    if ex:
                        setitem(d, p, getitem(dictobj, p),
                                dict_type=dict_type)
            else:
                if getitem(d, p) != getitem(dictobj, p):
                    if hasattr(func_if_overwrite, '__call__'):
                        ow = func_if_overwrite(p, d, dictobj)
                    else:
                        ow = func_if_overwrite
                    restruct_ = restruct and ow
                    setitem(d, p, getitem(dictobj, p),
                            overwrite=ow,
                            restruct=restruct_,
                            dict_type=dict_type)
    return d


def retype(dictobj, dict_type):
    """
    Recursively modifies the type of a dictionary object and returns a new
    dictionary of type dict_type. You can also use this function instead
    of copy.deepcopy() for dictionaries.
    """
    def walker(dictobj):
        for k in dictobj.keys():
            if isinstance(dictobj[k], dict):
                yield (k, dict_type(walker(dictobj[k])))
            else:
                yield (k, dictobj[k])
    d = dict_type(walker(dictobj))
    return d


def _validate_path(path):
    if not isinstance(path, list):
        raise TypeError('path argument have to be a list')
    if not path:
        raise Exception('path argument have to be a nonempty list')


def sum_values(measure_value):
    """Sums all the measure values

    Args:
        measure_value: Dictionary which holds the Date and Time as a key,
                       and the value the current number of crossings and 0
    Returns:
        the sum of all the measure values for that dictionary
    """
    for key, value in measure_value.items():
        measure_value[key] = sum(value)

    return measure_value


def cumulative_average(values_list):
    """" Gathers the cumulative average for each measure.
         So if the values list has more than one value,
         then there will be two numbers, the total sum at
         that step as well as the cumulative average.

    Args:
        values_list: list of values of the specific measure

    Return:
        list: if there are not multiple values, then return
              the singular value and 0, otherwise return
              the value at each step of the cumulative average.
    """

    if len(values_list) == 1:
        for value in values_list:
            return [tuple((value, 0))]

    new_list = [0] * len(values_list)

    new_p, counter = 0, 0
    for i in range(len(values_list)-1, -1, -1):
        new_list[i] = new_p
        new_p += values_list[i]

        if counter >= 1:
            new_list[i] = my_round(new_list[i]/counter)

        counter += 1

    return list(zip(values_list, new_list))


def find_the_bloody_key(total_list, result_key, measure_key, measure_values):
    """From the list of all the measure values, gets the values at each step.
       For instance, at step 0, Cars passing in Canada-US border is 6,800. At
       step 1, Cars passing in Canada-US border is 7,000--so the average is 14,800.

       Args:
           total_list: list of all measure values (number, and cumulative average)
           result_key: name of border
           measure_key: date and time entry
           measure_values: value of measure

       Returns:
            new_total_list: list of everything
                            (<Border>, <Date>, <Measure>, <Value>, <Average>)
                            nicely put together

        Raises:
            IndexError: if total_list is emtpy
            ValueError: if total list has less than one pair of measure value and
                        cumulative sum.
       """

    if not total_list:
        raise IndexError("Error! The list of cumulative average is empty.")

    new_total_list = []
    i = 0
    for key in measure_values.keys():

        # If the list has 1 value!
        if len(list(chain(*total_list))) == 2 and total_list[0][0] in measure_values.values():

            # saves in this order: <Border>, <Date>, <Measure>, <Value>, <Average>
            return [result_key, key, measure_key, total_list[0][0], total_list[0][1]]

        # if the list has more than 1 value
        elif len(list(chain(*total_list))) > 2:
            if total_list[i][0] in measure_values.values() and i < len(list(chain(*total_list))):
                new_total_list.append([result_key, key, measure_key, total_list[i][0], total_list[i][1]])
                i += 1

        else:
            raise ValueError("Error: total_list does not has less than one pair of values.")

    return new_total_list


def find_average(result):
    """Iterate through the various keys and values,
       until we find the specific one of interest. Find the cumulative average.
       Place that in the final list, and sort it by the Date, Value, Measure, and
       Border.

       Args:
           result: list of all the data

        Returns:
            final_sorted_list: list of sorted items

    """

    all_list = []

    for result_key, result_value in result.items():
        for measure_key, measure_value in result_value.items():

            measure_values = sum_values(measure_value)

            new_table = [v for v in (measure_values.values())]
            total_list = cumulative_average(new_table)

            row = find_the_bloody_key(total_list, result_key, measure_key, measure_values)

            if len(row) == 5:
                all_list.append(row)
            else:
                all_list += row

    # Sort the list by Date, Value, Measure, Border in descending order
    sorted_list_with_val_border_measure = sorted(all_list, key=itemgetter(3, 2, 0),
                                                 reverse=True)
    final_sorted_list = sorted(sorted_list_with_val_border_measure,
                               key=lambda x: datetime.strptime(x[1],
                                                               '%d/%m/%Y %H:%M:%S %p'),
                               reverse=True)

    return final_sorted_list
