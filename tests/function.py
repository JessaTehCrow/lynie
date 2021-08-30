def some_func(arg1:int=5):
    return arg1 ** 5

print(some_func(5))

other_func = lambda arg1=5: arg1 ** 5

print(other_func(5))