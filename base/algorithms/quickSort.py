# Function to find the partition position
def partitionName(array, low, high):
    # choose the rightmost element as pivot use it as lower case to avoid compare problems (ASCII)
    pivot = array[high].name.lower()
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j].name.lower() <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
def quickSortName(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partitionName(array, low, high)
 
        # Recursive call on the left of pivot
        quickSortName(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSortName(array, pi + 1, high)

# Function to find the partition position
def partitionTopic(array, low, high):
    # choose the rightmost element as pivot use it as lower case to avoid compare problems (ASCII)
    pivot = str(array[high].topic).lower()
 
    # pointer for greater element
    i = low - 1
 
    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if str(array[j].topic).lower() <= pivot:
 
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1
 
            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])
 
    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
 
    # Return the position from where partition is done
    return i + 1
 
# function to perform quicksort
def quickSortTopic(array, low, high):
    if low < high:
 
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partitionTopic(array, low, high)
 
        # Recursive call on the left of pivot
        quickSortTopic(array, low, pi - 1)
 
        # Recursive call on the right of pivot
        quickSortTopic(array, pi + 1, high)

