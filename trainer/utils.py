from datetime import datetime, timedelta

def booking_time_explore(trainer_schedule, bookings, check_time_step, duration):
    # Input parameters:
    # trainer_schedule: list [start_datetime, end_datetime]
    # bookings: list of tuples [(booking1_start_datetime, booking1_end_datetime),
    #                           (booking2_start_datetime, booking2_end_datetime), ...] - ordered chronologically
    # check_time_step: integer, in minutes
    # duration: integer, in minutes
    #
    # Function returns: free_timeslots_list - [free_timeslot1_start_datetime, free_timeslot2_start_datetime, ...]
    #    ordered chronologically
    # -------------------------------------------------------------------------------------------------------------
    free_timeslots_list = []
    start_time, end_time = trainer_schedule
    time_to_add = start_time

    while time_to_add + timedelta(minutes=duration) <= end_time:
        this_time_is_free = True
        for booking in bookings:
            if (time_to_add + timedelta(minutes=duration) > booking[0]) and (time_to_add < booking[1]):
                this_time_is_free = False
                break
        if this_time_is_free:
            free_timeslots_list.append(time_to_add)

        time_to_add += timedelta(minutes=check_time_step)

    return free_timeslots_list

#-------------------------------------------------------------------------------------------------------------------
test_trainer_schedule = [datetime(2025,1,11, 9, 0),
                        datetime(2025,1,11, 18, 0)]
test_bookings = [(datetime(2025,1,11, 11, 0),
                        datetime(2025,1,11, 12, 0)),
                 (datetime(2025,1,11, 12, 30),
                  datetime(2025,1,11,13,0)),
                 (datetime(2025,1,11, 17, 0),
                  datetime(2025,1,11, 17, 30))]
test_check_time_shift = 15
test_duration = 30

test_timeslots = booking_time_explore(test_trainer_schedule, test_bookings, test_check_time_shift, test_duration)
for slot in test_timeslots:
    print(slot.strftime("%Y-%m-%d %H:%M"))

print('With empty list of bookings:')
test_bookings = []
test_timeslots = booking_time_explore(test_trainer_schedule, test_bookings, test_check_time_shift, test_duration)
for slot in test_timeslots:
    print(slot.strftime("%Y-%m-%d %H:%M"))