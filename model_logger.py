from datetime import datetime as dt

def Logger(a, b, operation, result):
    path = 'log.csv'
    time_sign = dt.now().strftime('%D %H:%M')
    f = open(path, 'a')
    f.write(f'{time_sign}--> {a} {operation} {b} = {result}\n')
    f.close()
