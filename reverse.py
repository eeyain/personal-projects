def reverse(x):
    is_negative = False #save polarity of x
    fwd_int = abs(x)    #take as +ve value first. sign comes later
    digit_count = len(str(fwd_int))  #convert to str, then count how many chars
    if (x > (2**31 - 1) or x < -(2**31)):    #signed int check
        return 0
    elif (x < 0):
        is_negative = True

    reverse_int, i = 0, 0       #initialise variables to 0
    while (i < digit_count):    #e.g. if 4 digits then from 0 to 3
        # % 10 to get digit  
        reverse_int += (fwd_int % 10) * (10 ** (digit_count - i - 1))
        i = i + 1
        fwd_int = fwd_int // 10 #floor (int) divison
        
    if (is_negative):
        print(reverse_int * -1) #insert -ve sign if input was -ve
    else:
        print(reverse_int)
 
