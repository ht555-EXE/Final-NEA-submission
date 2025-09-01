#number is passed in from main logic
def binaryConvert(number):
    binaryText = ""
    reverseBinaryList = []
    #denary number zero produces zero in binary, so zero is returned
    if number == 0:
        return 0
    #number is continually divided by two to generate binary bits 
    while number != 0:
        numberRemainder = number%2
        reverseBinaryList.append(numberRemainder)
        number = number//2
    #list is converted to string
    for i in range(len(reverseBinaryList)-1,-1, -1):
        binaryText = binaryText + str(reverseBinaryList[i])
    return binaryText
