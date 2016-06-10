# This program flush dnb database, create a superuser: admin/admin, and test data.
# Require fake-factory and pytz: pip install fake-factory, pip install pytz
import os, sys, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dzbnb.settings")
django.setup()
from django.contrib.auth.models import User
from bnb.models import *
from faker import Faker # https://pypi.python.org/pypi/fake-factory
from random import randint, randrange, choice
from pytz import timezone

TIMEZONE = 'Asia/Phnom_Penh'
TOTAL_USERS_TO_ADD = 100
UNI_PASSWORD = '123456'
MAX_PROPERTIES_PER_USER = 3
fake = Faker()

try:
    User.objects.all().delete()
except:
    print('Must first run python manage.py flush')
else:
    try:
        print ('Creating Superuser.')
        User.objects.create_superuser(username='admin', password='admin', email='')
    except:
        print (sys.exc_info()[0])
    else:
        users_to_insert = []
        print ('Creating Users:')
        for i in range(0, TOTAL_USERS_TO_ADD-1): 
            u = User()
            u.password = UNI_PASSWORD
            u.first_name = fake.first_name()
            u.last_name = fake.last_name()
            u.email = fake.email()
            u.is_staff = fake.boolean(chance_of_getting_true=99)
            u.is_superuser = fake.boolean(chance_of_getting_true=1)
            u.is_active = fake.boolean(chance_of_getting_true=99)
            u.username = u.first_name + u.last_name
            u.date_joined = fake.date_time_between(start_date="-5y", end_date="-1m").replace(tzinfo=timezone(TIMEZONE))
            u.last_login = fake.date_time_between(start_date="-28d", end_date="now").replace(tzinfo=timezone(TIMEZONE))
            users_to_insert.append(u)
            print ('\r{}'.format(i+1), end='', flush=True)
        try:
            User.objects.bulk_create(users_to_insert)
        except:
            print (sys.exc_info()[0])
        else:
            print ()
            all_users = User.objects.all()
            bnbusers_to_insert = []
            i = 0
            print ('Creating BNBUsers:')
            for u in all_users:
                b = BNBUser()
                b.user = u
                b.login_count = randint(0,1000)
                bnbusers_to_insert.append(b)
                print('B', end='', flush=True)
                i += 1
                print ('\r{}'.format(i), end='', flush=True)
            try:
                BNBUser.objects.bulk_create(bnbusers_to_insert)
            except:
                print (sys.exc_info()[0])
            else:
                print ()
                all_bnbusers = BNBUser.objects.all()
                properties_to_insert = []
                print ('Creating Properties:')
                i = 0
                for b in all_bnbusers:
                    for _ in range(0, randint(0, MAX_PROPERTIES_PER_USER)):
                        p = Propertie()
                        p.owner = b
                        p.name = fake.sentence(nb_words=randint(3, 8), variable_nb_words=True)
                        p.hidden = fake.boolean(chance_of_getting_true=2)
                        p.size = randrange(0, 100)
                        p.price = randrange(150, 5000)
                        p.description = fake.paragraph(nb_sentences=randint(1, 5), variable_nb_sentences=True)
                        properties_to_insert.append(p)
                        i += 1
                        print ('\r{}'.format(i), end='', flush=True)
                try:
                    Propertie.objects.bulk_create(properties_to_insert)
                except:
                    print (sys.exc_info()[0])
                print ()
 
        all_properties = Propertie.objects.all()
        all_active_bnbusers = all_bnbusers.filter(user__is_staff=True).filter(user__is_active=True)
        all_active_properties = all_properties.filter(hidden=False)

        reservations_to_insert = []
        print ('Creating Reservations:')
        i = 0
        for u in all_active_bnbusers:
            if fake.boolean(chance_of_getting_true=50):
                r = Reservation()
                r.propertie = choice(all_active_properties)
                r.renter = u
                r.start_date = fake.date_time_between(start_date="-100d", end_date="-50d").replace(tzinfo=timezone(TIMEZONE))
                r.end_date = fake.date_time_between(start_date="-49d", end_date="-1d").replace(tzinfo=timezone(TIMEZONE))
                r.approved = fake.boolean(chance_of_getting_true=50)
                reservations_to_insert.append(r)
                i += 1
                print ('\r{}'.format(i), end='', flush=True)
        try:
            Reservation.objects.bulk_create(reservations_to_insert)
        except:
            print (sys.exc_info()[0])
        print ()

        reviews_to_insert = []
        i = 0
        print ('Creating Reviews:')
        for u in all_active_bnbusers:
            for j in range(0, randint(0, 5)):
                rv = Review()
                rv.reviewer = u
                rv.propertie = choice(all_active_properties)
                rv.hidden = fake.boolean(chance_of_getting_true=10)
                rv.rating = choice([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5])
                rv.comment = fake.paragraph(nb_sentences=randint(1, 5), variable_nb_sentences=True)
                rv.review_time = fake.date_time_between(start_date="-1y", end_date="-1m").replace(tzinfo=timezone(TIMEZONE))
                reviews_to_insert.append(rv)
                i += 1
                print ('\r{}'.format(i), end='', flush=True)
        try:
            Review.objects.bulk_create(reviews_to_insert)
        except:
            print (sys.exc_info()[0])
        print ()

        views_to_insert = []
        print ('Creating Views:')
        for i in range (0, len(all_bnbusers)*len(all_properties)):
            v = View()
            v.propertie = choice(all_properties)
            v.viewer = choice(all_bnbusers)
            v.view_time = fake.date_time_between(start_date="-1y", end_date="-1m").replace(tzinfo=timezone(TIMEZONE))
            views_to_insert.append(v)
            print ('\r{}'.format(i+1), end='', flush=True)
        try:
            View.objects.bulk_create(views_to_insert)
        except:
            print (sys.exc_info()[0])

print()
print('Results:')
tables = ['User', 'BNBUser', 'Propertie', 'Reservation', 'Review', 'View']
for table in tables:
    print('{}: {}'.format(table, eval(table).objects.count()))
