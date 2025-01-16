from config import settings

log_amount = settings["cross_characters"]
log_counter = 0

def increment_counter():
    global log_counter
    log_counter += 1
    return log_counter

def reset_counter():
    global log_counter
    log_counter = 0
    return log_counter