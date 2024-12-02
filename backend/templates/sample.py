import time;
start_time = None
def checkin():
    global start_time
    start_time = time.time()
    return "Timer started"
def checkout():
    global start_time
    if start_time is None:
        return  "Timer not started"
    elapsed_time = time.time() - start_time
    start_time = None
    return elapsed_time
# print(checkin())
# time.sleep(10)
# print(checkout())