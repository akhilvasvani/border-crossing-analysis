# Border Crossing Analysis

## Table of Contents
1. [Problem](README.md#problem)
1. [Language and Libraries Used](README.md#language-and-libraries-used)
1. [How I solved this problem](README.md#how-i-solved-this-problem)
1. [Pros and Cons](README.md#pros-and-cons)
1. [How to run my Work?](README.md#how-to-run-my-work)
1. [References](README.md#references)

## Problem
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, equipment, passengers and pedestrians crossing into the United States by land.

**For this challenge, I will calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. In addition, I will find the running monthly average of total number of crossings for that type of crossing and border from the input dataset provided to me.**

## Language and Libraries Used
I used Python3 as my coding language to solve this problem. Sticking to the problem statement, I avoided the use of any pip installed libraries on Python and opted for the default included libraries. I used:

csv

argparse

operator 

datetime

itertools

math

## How I solved this problem
To solve this problem, I first read in the data as a ordered_dictionary and tried iterating through the csv file to seperate out the Border names, the dates, and the measures. Once then, I would try to establish a link betweeen the Border names, dates, and the measures via implementing several dictionary. Dictionaries are extremely useful because when looking up something inside a dictionary the time complexity is O(1). However, this did not work because iteravely updating a dictionary was tricky and it proved to be hard. 

Next I tried implementing a stack to keep track of the valves for each border, date, and measure, but once again I ran into the issue of how to know when to update the stack if I changed either of those three cateogories. In addition, I would have to make 6000+ different stacks if I implemented this structure (for each border, date, and measure). This did not lead anywhere. 

Hence, I arrived at my solution. I read in the csv file, and I sorted it (in a descending order) via Border, Date, and Measure and then I grouped the sorted list via these same 3 cateogories, so there would be a solid chunk of the same cateogies, but different values. This was essential because now all I had to do was aggregate these values and then calculate the average for each crossing!

Fun things I learned: iterating over Lists of Lists is (slightly) faster than iterating over a list of OrderedDictionaries! Itemgetter is faster than using a lambda function.


### Pros and Cons

Pros of my methodolgy:
* Easy code to read, nothing very messy or hard to understand
* If instead of aggregating the valves of the crossings and you wanted to aggregate via the date, it's easy to implement and not much to change

Cons:
* Unfortunately because I sorted the list (the data read in the csv_file), my time complexity became O(n log(n)), which is both the best and worst case. And at one time I have two nested for-loops, so my overall time complexity for my main function is O(n^{2} + n log(n)) = O(n^{2}), which if scaled up to a LOT more elements would take too long. Although I tried to implement other data structures to prevent this from happening, I could not get them working. Hence, I opted to have something working than nothing at all. In order to avoid this for future iterations, I would use the Pandas libraries, which would avoid the need for sorting (though we would still need to use the groupby function which I think is O(n) time complexity). My space complexity was simply O(n). 

### How to run my work?

So the first step, is to run the ```run.sh``` bash file, which will call my border_crossing_statistics.py script. However, I have added in extra parameters:

YOU MUST SPECIFY THE INPUT AND OUTPUT FILE AS WELL AS THE ARGUMENTS THEMSELVES. I REPEAT SPECIFY THE INPUT AND OUTPUT. For example,

this will work: ```python3 src/border_crossing_statistics.py --input input/Border_Crossing_Entry_Data.csv --output output/report.csv```

This will not work: ```python3 ./src/border_analytics.py ./input/Border_Crossing_Entry_data.csv ./output/report.csv```

I did this because there is now a clear distinction between input and output.

## References

Last, but not least, are the references whose helpful and thoughtful resources I read to help me solve this problem. While I did not use all of them, some were essential. Without them, I would not have been able to get this far so without further ado: 

[Reading and Writing CSV Files in Python](https://realpython.com/python-csv/)

[Python: OrderedDict](https://docs.python.org/2/library/collections.html#collections.OrderedDict)

[OrderedDict: Reordering, Delete, and Reinsert New OrderedDict](https://data-flair.training/blogs/python-ordereddict/)

[Python: Itertools](https://docs.python.org/3.5/library/itertools.html#itertools.groupby)

[How do I sort a list of dictionaries by a value of the dictionary?](https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary)

[How to sort a list of lists by a specific index of the inner list](https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list/4174955)

[Using Counter with list of lists](https://stackoverflow.com/questions/19211018/using-counter-with-list-of-lists)

[Python: Itemgetter](https://docs.python.org/3/library/operator.html#operator.itemgetter)

[How to iteratively append key-value pairs to a dictionary in Python?](https://stackoverflow.com/questions/31326297/how-to-iteratively-append-key-value-pairs-to-a-dictionary-in-python)

[dictionary update sequence element #0 has length 3; 2 is required](https://stackoverflow.com/questions/14302248/dictionary-update-sequence-element-0-has-length-3-2-is-required/14313394)

[In the Python dictionary, can 1 key hold more than 1 value?](https://www.quora.com/In-the-Python-dictionary-can-1-key-hold-more-than-1-value)

[https://www.quora.com/In-the-Python-dictionary-can-1-key-hold-more-than-1-value](https://www.quora.com/In-the-Python-dictionary-can-1-key-hold-more-than-1-value)

[Python creating a dictionary of lists](https://stackoverflow.com/questions/960733/python-creating-a-dictionary-of-lists)

[How to iterate through a list and sum members together](https://stackoverflow.com/questions/25149609/how-to-iterate-through-a-list-and-sum-members-together)

[python group on 2 keys in a list of lists and sum on 2 different values in each list](https://stackoverflow.com/questions/41071096/python-group-on-2-keys-in-a-list-of-lists-and-sum-on-2-different-values-in-each)

[compute mean in python for a generator](https://stackoverflow.com/questions/4963784/compute-mean-in-python-for-a-generator)

[Python - Itemgetter on Dates](https://stackoverflow.com/questions/21634678/python-itemgetter-on-dates)

[Python3: test if all values of a dictionary are equal - when value is unknown](https://stackoverflow.com/questions/45020701/python3-test-if-all-values-of-a-dictionary-are-equal-when-value-is-unknown?rq=1)
