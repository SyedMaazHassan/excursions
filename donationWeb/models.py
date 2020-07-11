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

    def __str__(self):
        return self.excursions_name

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

    def __str__(self):
        this_name = excursions.objects.get(id=self.select_excursion)
        return this_name.excursions_name+" ("+str(self.availability_date)+")"


class user_confirmation(models.Model):
    id = models.IntegerField(primary_key=True)
    code_hash = models.CharField(max_length=32)
    is_verified = models.BooleanField()

    def __str__(self):
        thisUSER = User.objects.get(id=self.id)
        return thisUSER.username



class profile_pics(models.Model):
    id = models.IntegerField(primary_key=True)
    user_img = models.ImageField(upload_to='profilePics')

    def __str__(self):
        thisUSER = User.objects.get(id=self.id)
        return thisUSER.username


class booking_details(models.Model):
    id = models.AutoField(primary_key=True)
    available_row_id = models.IntegerField()
    total_members = models.IntegerField()
    booked_by = models.IntegerField()
    total_amount = models.FloatField()
    isCompleted = models.BooleanField(default=False)
    current_date = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))

    def __str__(self):
        thisUSER = User.objects.get(id=self.booked_by)
        availableFocus = availability.objects.get(id = self.available_row_id)
        excursionFocus = excursions.objects.get(id=availableFocus.select_excursion)
        return excursionFocus.excursions_name+"  -  "+thisUSER.username+"  -  "+str(self.current_date)+"  -  "+str(self.total_members)+" seats"+"  -  Amount = "+str(self.total_amount)




class credit_cards(models.Model):
    id = models.AutoField(primary_key=True)
    owner_id = models.IntegerField()
    exp_date = models.DateField()
    cvv_num = models.CharField(max_length=3)
    card_number = models.CharField(max_length=20)
    total_credit = models.FloatField(default=5000)

    def __str__(self):
        thisUSER = User.objects.get(id=self.id)
        return thisUSER.username



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




