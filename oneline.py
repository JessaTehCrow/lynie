def test(y):
    if y < 1000:
        return test(y*2)
    return y

print(test(5))