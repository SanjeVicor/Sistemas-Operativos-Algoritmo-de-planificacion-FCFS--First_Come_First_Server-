from decimal import *
def makeOperation(operation):
    getcontext().prec = 10
    #print('Solving : ', operation)
    while len(operation) != 1 :
        #print(operation)
        if "^" in operation:
            position = operation.index("^") 
            num1 = int(operation[position - 1])
            num2 = int(operation[position +1])
            #result = Decimal(pow(num1, num2))
            result = Decimal((num1**num2))
            operation[position] = result
            del operation[position - 1]
            del operation[position ]

        elif "%" in operation:
            position = operation.index("%") 
            num1 = int(operation[position - 1])
            num2 = int(operation[position + 1])
            #print(position)
            #print(num1)
            #print(num2)
            try:
                result =num1%num2
                operation[position] = result
                del operation[position - 1]
                del operation[position ]
            except :
                result = "Error durante la ejecucion : modulo por cero"  
                break

        elif "*" in operation:
            position = operation.index("*") 
            num1 = int(operation[position - 1])
            num2 = int(operation[position + 1])
            result = Decimal(num1 * num2)
            operation[position] = result
            del operation[position - 1]
            del operation[position ]

        elif "/" in operation:
            position = operation.index("/") 
            num1 = int(operation[position - 1])
            num2 = int(operation[position + 1])
            try:
                result = Decimal(num1 / num2)
                operation[position] = result
                del operation[position - 1]
                del operation[position ]
            except :
                result = "Error durante la ejecucion: division por cero"  
                break

        elif "-" in operation:
            position = operation.index("-")
            if position == 0  and len(operation) > 2:
                #print("-------------------")
                num1 = int(operation[position + 1]) * (-1)
                operator = operation[position + 2]
                num2 = int(operation[position + 3]) 

                if "+" in operator : 
                    result = Decimal(num1 + num2)
                elif "-" in operator : 
                    result = Decimal(num1 - num2)
                elif "*" in operator : 
                    result = Decimal(num1 * num2)
                elif "/" in operator : 
                    result = Decimal(num1 / num2)
                elif "%" in operator : 
                    result = Decimal(num1 % num2)
                elif "^" in operator : 
                    #result = Decimal(pow(num1, num2))
                    result = Decimal(num1**num2)
                
                operation[position] = result 
                del operation[1]
                del operation[1]
                del operation[1]
            elif  position == 0  and len(operation) == 2:
                num1= int(operation[position + 1]) * (-1)
                result = num1
                operation[position] = result 
                del operation[1]
            else : 
                num1 = int(operation[position - 1]) 
                num2 = int(operation[position + 1])
                result = Decimal(num1 - num2)
                operation[position] = result
                del operation[position - 1]
                del operation[position ]
        
        
        elif "+" in operation:
            position = operation.index("+") 
            num1 = int(operation[position - 1])
            num2 = int(operation[position + 1])
            result = Decimal(num1 + num2)
            operation[position] = result
            del operation[position - 1]
            del operation[position ]
            
        #print(operation)
            

    return result
