# CS6502 Programming for Bioscientists II
# Assignment 1
# Author: Conor Giles-Doran (121105743)
# 18/02/2022

import itertools  # 'itertools' python library imported for Q2 part b (generating n! permutations of size n).

### QUESTION ONE ###

# ptriangle(n)
# Prints the n-th line of Pascale's triangle (counting from 1).
def ptriangle(n):

    if n == 0:  # if zero is entered, return an error message that promps value > 0.
        return 'Error: counting rows from 1 - please enter value > 0.'
    if n == 1:  # if one is entered, just return [1] as this is the first row of pascal.
        return [1]
    else:
        # target_row will always start with a 1, so [1] is first element of row n.
        target_row = [1]

        # target_row will always end with a 1, so [1] will be the end point of row n.
        row_end = [1]

        # recursive call of ptriangle() to get value of the previous row.
        # the values of the (n-1)-th row are needed to get the values of row n.
        prev_row = ptriangle(n - 1)

        # for loop to iterate through values of the previous row.
        for i in range(len(prev_row) - 1):
            # within the previous row, one value + the next adjacent value provides each new value for the n-th row.
            nrow_val = prev_row[i] + prev_row[i + 1]
            # add the values calculated for the n-th row to the target_row list created above.
            target_row.append(nrow_val)
            # this list will already contain a 1, and now contains every value for row n except the end value.

        # add the end value [1] to the target_row list
        target_row += row_end

    # we now have a completed list of values for the n-th row of Pascal's triangle
    return target_row

# Examples #
# ptriangle(0)
# ptriangle(6)
# ptriangle(10)

# Recursive Explanation #
# As an example:
# When ptriangle(n-1) is first recursively called for ptriangle(6), it will be called for ptriangle(5).
# This in turn will recursively call ptriangle(4), which in turn calls ptriangle(3)...and so on until ptriangle(1).
# ptriangle(1) is the base case and will return [1] as per initial conditions of the function.
# As a result, ptriangle(2) can now proceed with [1] as the value of the previous row.
# As [1] is only of length 1, the for loop will be skipped and ptriangle(2) will have a [1] added on to give [1, 1].
# ptriangle(3) can then proceed and will enter the for loop with prev_row = [1,1].
# Therefore, ptriangle(3) = [starting 1 , 1 + 1, ending 1] = [1,2,1].
# This continues until ptriangle(5) is calculated as the previous row and provides the answer for ptriangle(6).

### QUESTION TWO ###

### Q2 PART 1 ###

# swap(n)
# simple swapping function for two elements of a list
# (from Lab 2 a) NotesOnTiming-EXTRA-CLASS-MATERIAL)
def swap(list, i, j):
    (list[i], list[j]) = (list[j], list[i])

# Alternative swap() function I created myself if above function not allowed to be used
#def swap(lis, index1, index2):
    #to_swap = lis[index1]
    #lis[index1] = lis[index2]
    #lis[index2] = to_swap

    #return lis

# Original InsertionSort(lis) function
# From Assignment 1 Exercise 2
def InsertionSort(lis):
    listemp = lis.copy()
    for i in range(1,len(listemp)):
        while (i >= 1 and (listemp[i-1] > listemp[i])):
            swap(listemp,i-1,i)
            i = i-1
    return listemp


# Example:
# InsertionSort([4,1,3,2])


# InsertionSortCount(lis)
# returns the number of comparisons (between list elements
# only) made by the algorithm InsertionSort on the input list.
def InsertionSortCount(lis):

    listemp = lis.copy()    # make a copy of the input list
    no_swap = 0             # initialize counter for number of comparisons without a swap
    swaps = 0               # initialize counter for number of comparisons with a swap

    # for loop to iterate through each element of list
    for i in range(1, len(listemp)):

        # conditions for sorting
        while (i >= 1 and (listemp[i - 1] > listemp[i])):

            # if a list element > the next list element, then swap these around
            swap(listemp, i - 1, i)
            # this is a swap, so add 1 to the swap count
            swaps += 1
            # reduce i by 1 to allow for correct list element iteration
            i = i - 1

        # otherwise if conditions are not met
        else:
            # and if i >= 1 and a list element LESS than the next list element
            if (i >= 1 and (listemp[i - 1] < listemp[i])):
                # then these elements are not to be swapped, but a comparison was still made
                # so add 1 to the no_swap counter
                no_swap += 1

    # the total number of comparisons will be:
    # the no. of comparisons with a swap + no. of comparisons without a swap
    comparisons = swaps + no_swap

    # return this total
    return comparisons

# Examples
# InsertionSortCount([1,2,3])
# InsertionSortCount([4,1,3,2])
# InsertionSortCount([4,1,3,2,1,3,4])

### Q2 PART 2 ###

# InsertionSortTime(n) function
# Prints the worst-case and average-case time for InsertionSort on lists of size n.
def InsertionSortTime(n):
    # 'itertools' python library should be imported for this function to operate.

    num_list = []  # set up basic list of size n.
    for i in range(1, n + 1):
        num_list.append(i)

    # using itertools.permutations function:
    # generate a list of all n! possible list permutations of size n.
    permuts = list(itertools.permutations(num_list))

    # set up an empty dictionary that will be used for counting comparison values.
    comp_dict = {}
    # for each of the n! permutations for a list of size n, e.g. if n = 3, n! = 6 possible list permutations.
    for permut in permuts:
        # add each permutation and its associated comparison count from the InsertionSortCount() function
        # to the comp_dict dictionary.
        comp_dict[permut] = InsertionSortCount(list(permut))
        # list() used here as itertools.permutations generates each permutation as a tuple,
        # whereas InsertionSortCount takes a list as input.

    # the worst permutation will be the maximum value of the comp_dict.
    worst_permut = max(comp_dict)
    # the actual worst count value.
    worst_count = comp_dict[worst_permut]

    # to get the total comparison count, add up all comparison count values from comp_dict.
    total_count = 0
    for count in comp_dict.values():
        total_count += count

    # average comparison count = total divided by n!
    avg_count = total_count / len(permuts)

    # print text output as detailed in question
    print('The worst-case time of InsertionSort on lists of size {} is {}'.format(n, worst_count))
    print('The average-case time of InsertionSort on lists of size {} is {}'.format(n, avg_count))

# Examples:
# InsertionSortTime(3)
# InsertionSortTime(4)
# InsertionSortTime(8)

### QUESTION THREE ###

# simple swap function used in Lab 1(a)
def swapshorthand(lst,i,j):
    lst[i],lst[j] = lst[j],lst[i]

# Original BubbleSort(lst) as seen in Lab 1(a)
def Bubblesort(lst):
    list_temp = lst.copy()
    for i in range(len(list_temp)-1,0,-1):
        for j in range(i):
            if list_temp[j] > list_temp[j+1]:
                swapshorthand(list_temp,j,j+1)
    return list_temp

# BubbleSortRec(lst)
# BubbleSort algorithm from above but which recursively performs the bubble-up phase.
def BubbleSortRec(lst):

    list_temp = lst.copy()  # make a copy of the input list

    # as with original, loop through each element of the input list from last element to first
    for i in range(len(list_temp) - 1, 0, -1):

        # if the list element is less than the previous element
        if list_temp[i] < list_temp[i - 1]:

            # (if more detailed step-by-step) text output required, uncomment below
            # print('Input List', list_temp, 'Comparison:', list_temp[i - 1], 'and', list_temp[i])

            # swap these elements using swapshorthand(lst,i,j) function
            swapshorthand(list_temp, i, i - 1)

            # instead of creating extra for loop to perform bubble-up phase
            # recursively call BubbleSortRec(lst) on the temporarily sorted list, within the if statement.
            list_temp = BubbleSortRec(list_temp)

    return list_temp

# Examples:
# BubbleSortRec([4,3,2,1])
# BubbleSortRec([4,3,1,1,1,1,1,2])
# BubbleSortRec([4,3,2,1,8,9,10,15,4])

# Recursive Explanation #
# Each time BubbleSortRec(lst) is called, the function will compare list elements two by two (pairs of elements).
# This will be performed without the need for a nested for loop (as seen in the original function).

# As an example - BubbleSortRec([4,3,2,1])
# list enters the main function as [4,3,2,1]
# It enters the for loop which starts at position 2 (value 1)
# 1 is first compared with 2 (the previous value) and it is less than 2 so it is swapped
# The list is now in an temporarily sorted state of [4,3,1,2].
# Still within the for loop and if statement, BubbleSortRec is then recursively called on this list.
# Again it starts at position 2, so 2 is compared to 1, but no swap is made so it does not enter the if statement.
# At position 1, 1 is compared to 3, which it is less than, so a swap is made.
# The list is now in a temporarily sorted state of [4,1,3,2]
# Again within the if statement, BubbleSortRec is recursively called on this list.
# This will end up producing the temporary list [4,1,2,3] and again BubbleSortRec(lst) is recursively called on this list.
# This will produce the temporary list [1,4,2,3] and then folliwng the same procedure, the list [1,2,4,3].
# Finally, the end result will be the complete sorted list as each list element will be less than the next adjacent
# element, meaning it will not enter the if statement and thus BubbleSortRec(lst) will not be called again.


