def concatenate(**kwargs):
    result = ""
    # Iterating over the Python kwargs dictionary
    for arg in kwargs.values():
        result += arg
    return result




def my_sum(*integers):
    result = 0
    for x in integers:
        result += x
    return result


if __name__ == '__main__':
    print(concatenate(a="Real", b="Python", c="Is", d="Great", e="!"))
    print(my_sum(1, 2, 3))