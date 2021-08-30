#Nested function
def nested_function(arg1):
    def squared(arg):
        return arg**2
    return squared(arg1)

print(nested_function(5))

#Nested loop
matrix = []
for y in range(5):
    matrix.append([])
    for x in range(5):
        matrix[y].append(x)

print(matrix)

#Nested if
var1 = 10

if var1 <= 100:
    if var1 == 20:
        print(var1**2)
    elif var1 > 20:
        print(var1)
    else:
        print(var1//2)
else:
    print("Var1 is greater than 100")