log_amount = 0
log_counter = 0

def set_counter(number: int):
    global log_amount
    log_amount = number
    return log_amount

def increment_counter():
    global log_counter
    log_counter += 1
    return log_counter

def reset_counter():
    global log_counter
    log_counter = 0
    return log_counter