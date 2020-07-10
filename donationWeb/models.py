from django.db import models
import datetime
from django.contrib.auth.models import User, auth
from datetime import datetime



# Create your models here.


class excursions(models.Model):
    id = models.AutoField(primary_key=True)
    excursions_name = models.CharField(max_length=70)
    excursions_image = models.ImageField(upload_to='excursions_pics')
    EX_TYPES = [
        ("adventure", "adventure"),
        ("activity", "activity"),
        ("relax", "relax"),
        ("city discovery", "city discovery")
    ]
    excursions_type = models.CharField(max_length=100, choices=EX_TYPES)
    excursions_place = models.CharField(max_length=255)
    excursions_description = models.TextField()
    amount_per_person = models.FloatField()
    excursions_ratings = models.FloatField()
    excursions_minimum_people = models.IntegerField()
    excursions_maximum_people = models.IntegerField()
    
class availability(models.Model):
    all_excursions = excursions.objects.all().order_by("id")
    all_choices = []

    for ex in all_excursions:
        id_name_pair = (str(ex.id), ex.excursions_name)
        all_choices.append(id_name_pair)

    all_choices_tuple = tuple(all_choices)

    select_excursion = models.CharField(max_length=255, choices=all_choices_tuple)

    availability_date = models.DateField()
    departure_time = models.TimeField()
    departure_point = models.CharField(max_length=255)
    
    return_date = models.DateField()
    return_time = models.TimeField()
    return_point = models.CharField(max_length=255)

    trip_completed = models.BooleanField(default=False)



class user_confirmation(models.Model):
    id = models.IntegerField(primary_key=True)
    code_hash = models.CharField(max_length=32)
    is_verified = models.BooleanField()

class profile_pics(models.Model):
    id = models.IntegerField(primary_key=True)
    user_img = models.ImageField(upload_to='profilePics')


class booking_details(models.Model):
    id = models.AutoField(primary_key=True)
    available_row_id = models.IntegerField()
    total_members = models.IntegerField()
    booked_by = models.IntegerField()
    total_amount = models.FloatField()
    isCompleted = models.BooleanField(default=False)
    current_date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))


class credit_cards(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.IntegerField()
    exp_date = models.DateField()
    cvv_num = models.CharField(max_length=3)
    card_number = models.CharField(max_length=20)
    total_credit = models.FloatField(default=5000)


class ex_reviews(models.Model):
    id = models.AutoField(primary_key=True)
    author_id = models.IntegerField()
    author_name = models.CharField(max_length=50)
    author_picture = models.CharField(max_length=150)
    review_star = models.IntegerField()
    review_msg = models.TextField()
    event_id = models.IntegerField()
    date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))

class whole_person_info:
    def __init__(self, id):
        self.person = User.objects.get(id=id)
        self.id = id
        self.full_name = self.person.first_name
        self.email = self.person.username
        self.img = self.person.last_name
        self.dob = self.email

        # credit_card_info = credit_cards.objects.get(owner_id=id)

        self.credit_status = credit_cards.objects.filter(owner_id=id).exists()

        if self.credit_status:
            self.cd = credit_cards.objects.get(owner_id=id)
            self.card_number = self.cd.card_number
            self.cvv_num = self.cd.cvv_num
            self.exp_date = self.cd.exp_date
            self.total_credit = self.cd.total_credit

        self.isBooked = booking_details.objects.filter(booked_by=id).exists()

        if self.isBooked:
            self.bd = booking_details.objects.filter(booked_by=id)
            self.all_bd = []

            for i in self.bd:
                thisDict = {}
                thisDict['total_amount'] = i.total_amount
                thisDict['total_members'] = i.total_members
                current_row_id = i.available_row_id
                getAvailableDates = availability.objects.get(id=current_row_id)
                getEvent = excursions.objects.get(id=getAvailableDates.select_excursion)

                thisDict['deptDate'] = getAvailableDates.availability_date
                thisDict['deptTime'] = getAvailableDates.departure_time
                thisDict['deptPoint'] = getAvailableDates.departure_point
                thisDict['retDate'] = getAvailableDates.return_date
                thisDict['rettTime'] = getAvailableDates.return_time
                thisDict['rettPoint'] = getAvailableDates.return_point
                thisDict['isCompleted'] = getAvailableDates.trip_completed
                thisDict['event_name'] = getEvent.excursions_name
                thisDict['event_id'] = getEvent.id
                thisDict['amount_per_person'] = getEvent.amount_per_person


                

                self.all_bd.append(thisDict)
                
        # for i in self.all_bd:
        #     for j in i:
        #         print(j, "->", i[j])
            



  


# class more_info(models.Model):
#     id = models.AutoField(primary_key=True)
#     image = models.ImageField(upload_to='profilePics')
#     dob = models.DateField()
#     friendPoints = models.IntegerField(default=0)
#     likes = models.IntegerField(default=0)
#     friends = models.IntegerField(default=0)
#     all_friends = models.CharField(max_length=5000, default="0")
#     amount_raised = models.IntegerField(default=0, editable=False)
#     like_persons = models.CharField(max_length=5000, default="0")
#     event_created = models.IntegerField(default=0, editable=False)
#     isOnline = models.BooleanField(default=0)
#     is_credit_card_added = models.BooleanField(default=0)

# class credit_card(models.Model):
#     card_id = models.AutoField(primary_key=True)
#     owner_id = models.IntegerField()
#     owner_name = models.CharField(max_length=30)
#     owner_surname = models.CharField(max_length=30)
#     exp_date = models.DateField()
#     cvv_number = models.IntegerField()
#     optional_card_number = models.IntegerField()

# class notifications(models.Model):
#     id = models.AutoField(primary_key=True)
#     sender_id = models.IntegerField()
#     sender_image = models.CharField(max_length=300)
#     receiver_id = models.IntegerField()
#     msg = models.CharField(max_length=600)
#     date = models.DateField()
#     time = models.TimeField()
#     isRead = models.BooleanField(default=0)

# class friend_list(models.Model):
#     id = models.AutoField(primary_key=True)
#     sender = models.IntegerField()
#     sender_image = models.CharField(max_length=300, default="None")
#     msg = models.CharField(max_length=800, default="None")
#     acceptor = models.IntegerField()
#     isAccepted = models.BooleanField(default=0) 
#     isRead = models.BooleanField(default=0)

# class credit_cards(models.Model):
#     id = models.AutoField(primary_key=True)
#     owner_id = models.IntegerField()
#     owner_name = models.CharField(max_length=60)
#     owner_surname = models.CharField(max_length=60)
#     exp_date = models.DateField()
#     cvv_num = models.CharField(max_length=3)
#     card_number = models.CharField(max_length=13)
#     total_credit = models.IntegerField(default=5000)

# class events(models.Model):
#     id = models.AutoField(primary_key=True)
#     image = models.ImageField(upload_to='events')
#     host_id = models.IntegerField()
#     name = models.CharField(max_length=255)
#     description = models.TextField(max_length=None)
#     starting_date = models.DateField()
#     due_date = models.DateField()
#     current_amount = models.IntegerField(default=0)
#     total_participants = models.IntegerField(default=0)
#     target_amount = models.IntegerField()
#     remaining_amount = models.IntegerField(default=0)
#     isCompleted = models.BooleanField(default=0)
#     is_amount_collected_by_host = models.BooleanField(default=0)

# class donation_details(models.Model):
#     id = models.AutoField(primary_key=True)
#     event_id = models.IntegerField()
#     donor_id = models.IntegerField()
#     credit_card_id = models.IntegerField()
#     donation_date = models.DateField()
#     donation_amount = models.IntegerField()

# class donation_all_details:
#     def __init__(self, donation_date, donation_amount):
#         self.donation_date = donation_date
#         self.donation_amount = donation_amount

#     def gether_event_details(self, event_id):
#         self.event = events.objects.get(id=event_id)
#         self.event_name = self.event.name
#         self.host = User.objects.get(id=self.event.host_id)
#         self.host_name = self.host.first_name




# class event_whole_info:
#     def __init__(self, id):
#         self.id = id

#     def all_values(self):
#         self.event = events.objects.get(id=self.id)
#         self.getting_event_info()
#         self.getting_host_info(self.event.host_id)

#     def getting_event_info(self):
#         self.name = self.event.name
#         self.image = self.event.image
#         self.description = self.event.description
#         self.starting_date = self.event.starting_date
#         self.due_date = self.event.due_date
#         self.current_amount = self.event.current_amount
#         self.total_participants = self.event.total_participants
#         self.target_amount = self.event.target_amount
#         self.remaining_amount = self.event.remaining_amount
#         self.isCompleted = self.event.isCompleted
#         self.is_amount_collected_by_host = self.event.is_amount_collected_by_host

#     def getting_host_info(self, host_id):
#         self.host = User.objects.get(id=host_id)
#         self.host_id = host_id
#         self.host_name = self.host.first_name
#         self.host_img = self.host.last_name

# class user_whole_info:
#     def __init__(self, id, name, email, image, likes, friends, all_friends, events=None, amount_collected=None, join_date=None, isOnline=None, like_persons=None):
#         self.id = id
#         self.name = name
#         self.email = email
#         self.image = image
#         self.likes = likes
#         self.friends = friends
#         self.events = events
#         self.amount_collected = amount_collected
#         if join_date is not None:
#             self.join_date = join_date.strftime("%d %b, %Y")
#         self.all_friends = all_friends
#         self.isOnline = isOnline
#         self.like_persons = like_persons
#         self.is_already_sent = False
#         self.make_friend_list()
#         self.make_liker_list()

#     def make_friend_list(self):
#         self.all_friends = self.all_friends.split(",")
#         self.all_friends = list(map(int, self.all_friends))
    
#     def make_liker_list(self):
#         if self.like_persons is not None:
#             self.like_persons = self.like_persons.split(",")
#             self.like_persons = list(map(int, self.like_persons))
        
#     def isRequestSent(self, other_id):
#         way_1 = friend_list.objects.filter(sender=self.id, acceptor=other_id, isAccepted=0).count()
#         way_2 = friend_list.objects.filter(sender=other_id, acceptor=self.id, isAccepted=0).count()
#         if not (way_1==0 and way_2==0):
#             self.is_already_sent = True

#     def print_all_data(self):
#         print(self.id, self.name, self.email, self.image, self.likes, self.friends, self.all_friends)


