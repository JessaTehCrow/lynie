generator_comp = (x for x in range(100) if x%2==0)
print(generator_comp)

list_comp = [x for x in range(100) if x%2==0]
print(list_comp)

dict_comp = {x:x%2==0 for x in range(100)}
print(dict_comp)