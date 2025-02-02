import unittest
import trainer.utils as utils
from datetime import datetime
from django.contrib.auth.models import Group, User

# Create your tests here.
class TestSchedule(unittest.TestCase):
    def test_schedule_no_bookings(self):
        trainer_schedule = [datetime(2024, 12, 25, 9, 0),
                                 datetime(2024, 12, 25, 18, 0)]
        bookings = []
        duration = 60
        check_time_shift = 15

        results = utils.booking_time_explore(trainer_schedule, bookings, duration, check_time_shift)
        expected = [datetime(2024, 12, 25,  9, 0), datetime(2024, 12, 25,  9, 15), datetime(2024, 12, 25,  9, 30), datetime(2024, 12, 25,  9, 45),
                    datetime(2024, 12, 25, 10, 0), datetime(2024, 12, 25, 10, 15), datetime(2024, 12, 25, 10, 30), datetime(2024, 12, 25, 10, 45),
                    datetime(2024, 12, 25, 11, 0), datetime(2024, 12, 25, 11, 15), datetime(2024, 12, 25, 11, 30), datetime(2024, 12, 25, 11, 45),
                    datetime(2024, 12, 25, 12, 0), datetime(2024, 12, 25, 12, 15), datetime(2024, 12, 25, 12, 30), datetime(2024, 12, 25, 12, 45),
                    datetime(2024, 12, 25, 13, 0), datetime(2024, 12, 25, 13, 15), datetime(2024, 12, 25, 13, 30), datetime(2024, 12, 25, 13, 45),
                    datetime(2024, 12, 25, 14, 0), datetime(2024, 12, 25, 14, 15), datetime(2024, 12, 25, 14, 30), datetime(2024, 12, 25, 14, 45),
                    datetime(2024, 12, 25, 15, 0), datetime(2024, 12, 25, 15, 15), datetime(2024, 12, 25, 15, 30), datetime(2024, 12, 25, 15, 45),
                    datetime(2024, 12, 25, 16, 0), datetime(2024, 12, 25, 16, 15), datetime(2024, 12, 25, 16, 30), datetime(2024, 12, 25, 16, 45),
                    datetime(2024, 12, 25, 17, 0)
                    ]
        self.assertListEqual(expected, results)

    def test_schedule_1_booking(self):
        # ------------------------------------------------------------------------------
        # booking in the middle of the working day
        trainer_schedule = [datetime(2025, 1, 11, 9, 0),
                                 datetime(2025, 1, 11, 18, 0)]
        bookings = [(datetime(2025, 1, 11, 11, 0),
                      datetime(2025, 1, 11, 12, 0)) ]
        duration = 60
        check_time_shift = 15
        results = utils.booking_time_explore(trainer_schedule, bookings, duration, check_time_shift)
        expected = [datetime(2025, 1, 11,  9, 0), datetime(2025, 1, 11,  9, 15), datetime(2025, 1, 11,  9, 30), datetime(2025, 1, 11,  9, 45),
                    datetime(2025, 1, 11, 10, 0),
                    datetime(2025, 1, 11, 12, 0), datetime(2025, 1, 11, 12, 15), datetime(2025, 1, 11, 12, 30), datetime(2025, 1, 11, 12, 45),
                    datetime(2025, 1, 11, 13, 0), datetime(2025, 1, 11, 13, 15), datetime(2025, 1, 11, 13, 30), datetime(2025, 1, 11, 13, 45),
                    datetime(2025, 1, 11, 14, 0), datetime(2025, 1, 11, 14, 15), datetime(2025, 1, 11, 14, 30), datetime(2025, 1, 11, 14, 45),
                    datetime(2025, 1, 11, 15, 0), datetime(2025, 1, 11, 15, 15), datetime(2025, 1, 11, 15, 30), datetime(2025, 1, 11, 15, 45),
                    datetime(2025, 1, 11, 16, 0), datetime(2025, 1, 11, 16, 15), datetime(2025, 1, 11, 16, 30), datetime(2025, 1, 11, 16, 45),
                    datetime(2025, 1, 11, 17, 0)
                    ]
        self.assertListEqual(expected, results)
        #-------------------------------------------------------------------------------
        # booking at the start of the working day
        trainer_schedule = [datetime(2025, 1, 11, 9, 0),
                                 datetime(2025, 1, 11, 18, 0)]
        bookings = [(datetime(2025, 1, 11, 9, 0),
                      datetime(2025, 1, 11, 10, 0)) ]
        duration = 60
        check_time_shift = 15
        results = utils.booking_time_explore(trainer_schedule, bookings, duration, check_time_shift)
        expected = [
                    datetime(2025, 1, 11, 10, 0), datetime(2025, 1, 11, 10, 15), datetime(2025, 1, 11, 10, 30), datetime(2025, 1, 11, 10, 45),
                    datetime(2025, 1, 11, 11, 0), datetime(2025, 1, 11,  11, 15), datetime(2025, 1, 11,  11, 30), datetime(2025, 1, 11,  11, 45),
                    datetime(2025, 1, 11, 12, 0), datetime(2025, 1, 11, 12, 15), datetime(2025, 1, 11, 12, 30), datetime(2025, 1, 11, 12, 45),
                    datetime(2025, 1, 11, 13, 0), datetime(2025, 1, 11, 13, 15), datetime(2025, 1, 11, 13, 30), datetime(2025, 1, 11, 13, 45),
                    datetime(2025, 1, 11, 14, 0), datetime(2025, 1, 11, 14, 15), datetime(2025, 1, 11, 14, 30), datetime(2025, 1, 11, 14, 45),
                    datetime(2025, 1, 11, 15, 0), datetime(2025, 1, 11, 15, 15), datetime(2025, 1, 11, 15, 30), datetime(2025, 1, 11, 15, 45),
                    datetime(2025, 1, 11, 16, 0), datetime(2025, 1, 11, 16, 15), datetime(2025, 1, 11, 16, 30), datetime(2025, 1, 11, 16, 45),
                    datetime(2025, 1, 11, 17, 0)
                    ]
        self.assertListEqual(expected, results)

        #------------------------------------------------------------------------------
        # booking at the end of the working day
        trainer_schedule = [datetime(2025, 1, 11, 9, 0),
                                 datetime(2025, 1, 11, 18, 0)]
        bookings = [(datetime(2025, 1, 11, 17, 0),
                      datetime(2025, 1, 11, 18, 0)) ]
        duration = 60
        check_time_shift = 15
        results = utils.booking_time_explore(trainer_schedule, bookings, duration, check_time_shift)
        expected = [
                    datetime(2025, 1, 11, 9, 0), datetime(2025, 1, 11, 9, 15), datetime(2025, 1, 11, 9, 30), datetime(2025, 1, 11, 9, 45),
                    datetime(2025, 1, 11, 10, 0), datetime(2025, 1, 11, 10, 15), datetime(2025, 1, 11, 10, 30), datetime(2025, 1, 11, 10, 45),
                    datetime(2025, 1, 11, 11, 0), datetime(2025, 1, 11,  11, 15), datetime(2025, 1, 11,  11, 30), datetime(2025, 1, 11,  11, 45),
                    datetime(2025, 1, 11, 12, 0), datetime(2025, 1, 11, 12, 15), datetime(2025, 1, 11, 12, 30), datetime(2025, 1, 11, 12, 45),
                    datetime(2025, 1, 11, 13, 0), datetime(2025, 1, 11, 13, 15), datetime(2025, 1, 11, 13, 30), datetime(2025, 1, 11, 13, 45),
                    datetime(2025, 1, 11, 14, 0), datetime(2025, 1, 11, 14, 15), datetime(2025, 1, 11, 14, 30), datetime(2025, 1, 11, 14, 45),
                    datetime(2025, 1, 11, 15, 0), datetime(2025, 1, 11, 15, 15), datetime(2025, 1, 11, 15, 30), datetime(2025, 1, 11, 15, 45),
                    datetime(2025, 1, 11, 16, 0)
                    ]
        self.assertListEqual(expected, results)
        #------------------------------------------------------------------------------
    def test_schedule_2_booking(self):
        # ------------------------------------------------------------------------------
        # 2 bookings at the edges of the working day
        trainer_schedule = [datetime(2025, 1, 11, 9, 0),
                            datetime(2025, 1, 11, 18, 0)]
        bookings = [(datetime(2025, 1, 11, 9, 0),
                     datetime(2025, 1, 11, 10, 0)),
                    (datetime(2025, 1, 11, 17, 0),
                     datetime(2025, 1, 11, 18, 0))
                    ]
        duration = 60
        check_time_shift = 15
        # don't set the 'check_time_shift' parameter
        results = utils.booking_time_explore(trainer_schedule, bookings, duration)
        expected = [
                    datetime(2025, 1, 11, 10, 0),datetime(2025, 1, 11, 10, 15),datetime(2025, 1, 11, 10, 30),datetime(2025, 1, 11, 10, 45),
                    datetime(2025, 1, 11, 11, 0), datetime(2025, 1, 11, 11, 15), datetime(2025, 1, 11, 11, 30), datetime(2025, 1, 11, 11, 45),
                    datetime(2025, 1, 11, 12, 0), datetime(2025, 1, 11, 12, 15), datetime(2025, 1, 11, 12, 30), datetime(2025, 1, 11, 12, 45),
                    datetime(2025, 1, 11, 13, 0), datetime(2025, 1, 11, 13, 15), datetime(2025, 1, 11, 13, 30), datetime(2025, 1, 11, 13, 45),
                    datetime(2025, 1, 11, 14, 0), datetime(2025, 1, 11, 14, 15), datetime(2025, 1, 11, 14, 30), datetime(2025, 1, 11, 14, 45),
                    datetime(2025, 1, 11, 15, 0), datetime(2025, 1, 11, 15, 15), datetime(2025, 1, 11, 15, 30), datetime(2025, 1, 11, 15, 45),
                    datetime(2025, 1, 11, 16, 0)
                    ]
        self.assertListEqual(expected, results)
        # ------------------------------------------------------------------------------
        trainer_schedule = [datetime(2025, 1, 11, 9, 0),
                            datetime(2025, 1, 11, 18, 0)]
        # 2 bookings in the middle of the working day, bookings are not ordered chronologically
        bookings = [(datetime(2025, 1, 11, 12, 0),
                     datetime(2025, 1, 11, 13, 0)),
                    (datetime(2025, 1, 11, 9, 0),
                     datetime(2025, 1, 11, 10, 30))
                    ]
        # duration 45 minutes
        duration = 45
        check_time_shift = 15
        results = utils.booking_time_explore(trainer_schedule, bookings, duration)
        expected = [
            datetime(2025, 1, 11, 10, 30), datetime(2025, 1, 11, 10, 45),
            datetime(2025, 1, 11, 11, 0), datetime(2025, 1, 11, 11, 15),
            datetime(2025, 1, 11, 13, 0), datetime(2025, 1, 11, 13, 15), datetime(2025, 1, 11, 13, 30), datetime(2025, 1, 11, 13, 45),
            datetime(2025, 1, 11, 14, 0), datetime(2025, 1, 11, 14, 15), datetime(2025, 1, 11, 14, 30), datetime(2025, 1, 11, 14, 45),
            datetime(2025, 1, 11, 15, 0), datetime(2025, 1, 11, 15, 15), datetime(2025, 1, 11, 15, 30), datetime(2025, 1, 11, 15, 45),
            datetime(2025, 1, 11, 16, 0), datetime(2025, 1, 11, 16, 15), datetime(2025, 1, 11, 16, 30), datetime(2025, 1, 11, 16, 45),
            datetime(2025, 1, 11, 17, 0), datetime(2025, 1, 11, 17, 15)
        ]
        self.assertListEqual(expected, results)


#-------------------------   Django tests   ------------------------------------
from django.test import TestCase, Client

class TrainerTest(TestCase):
    def test_show_all_trainers(self):
        client = Client()
        response = client.get('/trainer/')
        self.assertEqual(response.status_code, 200)

    def test_show_all_services(self):
        client = Client()
        response = client.get('/service/')
        self.assertEqual(response.status_code, 200)
        response = client.get('/service/?trainer_id=1')
        self.assertEqual(response.status_code,200)

    def test_trainer_add_service(self):
        # anonymous user
        client = Client()
        response = client.post('/service/', {'category': 1, 'price': 100, 'duration': 30, 'level':1})
        self.assertEqual(response.status_code, 403)

        # client
        Group.objects.create(name='client')
        user = User.objects.create_user(
                        username='user1',
                        password='1111',
                        email='user1@example.com',
                        first_name='user1',
                        last_name='password')
        user.groups.add(Group.objects.get(name='client'))
        user.save()
        client.login(username='user1', password='1111')
        response = client.post('/service/', {'category': 1, 'price': 100, 'duration': 30, 'level':1})
        self.assertEqual(response.status_code, 403)

        # trainer
        Group.objects.create(name='trainer')
        user = User.objects.create_user(
                        username='trainer1',
                        password='1111',
                        email='trainer1@example.com',
                        first_name='first',
                        last_name='trainer')
        user.groups.add(Group.objects.get(name='trainer'))
        user.save()
        client.login(username='trainer1', password='1111')
        response = client.post('/service/', {'category': 1, 'price': 100, 'duration': 30, 'level':1})
        self.assertEqual(response.status_code, 200)