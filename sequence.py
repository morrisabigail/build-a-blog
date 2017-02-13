#find a sequence that increases with only erasing one number

def sequence(lst):
    count = 0
    if len(lst)== 1:
        print("true")
        return True
    for item in lst:
        if lst[item] > lst[item+1]:
            count +=1
            if item == lst[-1]:
                break
                print("break")
        if count > 1:
            print("false")
            return False
        else:
            print("true")
            return True


sequence([1,3,2,1])
