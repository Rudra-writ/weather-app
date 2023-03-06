from statistics import mean
numbers = []
while True:

        entry = input("Enter a number: ")
        if entry == 'done':
            try:
                print("Sum: {0}, Count: {1}, average: {2}  ".format(sum(numbers), len(numbers), mean(numbers)))
            except:
                print("please enter atleast one value")
            break
        else:
            try:
                entry = float(entry)
                numbers.append(entry)
           
            except:
                print("Invalid Input")
                continue


    

