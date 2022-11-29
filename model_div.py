def init(a, b):
    global x
    global y
    x = a
    y = b


def do_it(x, y):
    if y == 0:
        return "Division by zero"
    else:
        return x/y
