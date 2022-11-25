def biLineTopic(arr, low, high, x):
    # Check base case
    x = str(x).lower()
    if high >= low:
        mid = (high + low) // 2
        
        # If element is present at the middle itself
        if str(arr[mid].topic).lower() == x:
            indx = []
            indx.append(mid)
            cont = mid + 1
            while cont < len(arr) and str(arr[cont].topic).lower() == x:
                indx.append(cont)
                cont += 1
            while mid-1 > -1 and str(arr[mid-1].topic).lower() == x:
                indx.append(mid-1)
                mid -= 1
            return indx
  
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif str(arr[mid].topic).lower() > x:
            return biLineTopic(arr, low, mid - 1, x)
 
        # Else the element can only be present in right subarray
        else:
            return biLineTopic(arr, mid + 1, high, x)
 
    else:
        # Element is not present in the array
        return None