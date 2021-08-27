def round(number):
    if number%1<0.5:
        return number-number%1
    return number+(1-number%1)

print(round(23873.73))