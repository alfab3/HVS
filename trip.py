#This is a function for a euler method to predict a trip when it may happen

import time


class TRIP:
    def trip_check(self):
        start = time.time()
        first_reading = mcp3428.take_single_recording(0)
        time.sleep(.01)
        end = time.time()
        second_reading = mcp3428.take_single_reording(0)
        rate = (second_reading - first_reading)/(end - start)
        if rate > 5:
            return True
        else:
            return False

