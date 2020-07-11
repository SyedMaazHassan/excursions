from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib as hl

from random import randint

# Create your views here.



def index(request):
    all_users = User.objects.all()
    for i in all_users:
        print(i.username)

    all_ex = excursions.objects.all()[:3]

    for i in all_ex:
        i.excursions_description = i.excursions_description[:250]

    context = {}

    context['all_ex'] = all_ex

    return render(request, "index.html", context)


def all_excursions(request):
    context = {}
    all_ex = excursions.objects.all()

    if request.method == "GET":

        filter_type = request.GET['typeFilter'] if 'typeFilter' in request.GET else None
        filter_place = request.GET['placeFilter'] if 'placeFilter' in request.GET else None
        filter_date = request.GET['dateFilter'] if 'dateFilter' in request.GET and request.GET['dateFilter']!=""     else None

        print("filter_type =>", filter_type)
        print("filter_place =>", filter_place)
        print("filter_date =>", filter_date)

        if filter_type is not None:
            all_ex = all_ex.filter(excursions_type=filter_type)

            context['filter_type'] = filter_type

        if filter_place is not None:
            all_ex = all_ex.filter(excursions_place=filter_place)

            context['filter_place'] = filter_place

        if filter_date is not None:
            all_ex = list(all_ex)

            available_ex = list(availability.objects.all().filter(availability_date=filter_date).values_list("select_excursion", flat=True))

            for i in range(0, len(available_ex)):
                available_ex[i] = int(available_ex[i])


            context['filter_date'] = filter_date

            for i in range(0, len(all_ex)):
                if all_ex[i].id not in available_ex:
                    all_ex[i] = None


    for i in all_ex:
        if i is not None:
            i.excursions_description = i.excursions_description[:250]

    all_ex_without_none = []

    for i in all_ex:
        if i is not None:
            all_ex_without_none.append(i)

    context['all_ex'] = all_ex_without_none

       # select all available types
    all_excursions_types = list(excursions.objects.values_list("excursions_type", flat=True))

    # select all available places
    all_excursions_places = list(excursions.objects.values_list("excursions_place", flat=True))

    # removing dublicates values
    all_excursions_types = remove_dublicate(all_excursions_types)
    all_excursions_places = remove_dublicate(all_excursions_places)

    context['available_places'] = all_excursions_places
    context['available_types'] = all_excursions_types




    return render(request, "all_events.html", context)


def remove_dublicate(myList):
    return list(dict.fromkeys(myList))


def particular_ex(request, id):
    context = {}
    particular_event = excursions.objects.get(id=id)
    context['event'] = particular_event

    available_dates = availability.objects.all().filter(select_excursion=str(id), trip_completed=False)

    today_date = datetime.today().strftime('%Y-%m-%d')
    empty_list = []


    for i in available_dates:
        if i.availability_date.strftime('%Y-%m-%d') > today_date:
            empty_list.append(i)



    available_dates = empty_list



    context['available_dates'] = available_dates

    if request.user.is_authenticated:
        context['USER'] = whole_person_info(request.user.id)
        if booking_details.objects.filter(booked_by=request.user.id).exists():
            booked_ex = list(booking_details.objects.filter(booked_by=request.user.id, isCompleted=False).values_list("available_row_id", flat=True))
            print(booked_ex)
            context['BOOKED_EX'] = booked_ex
        else:
            context['BOOKED_EX'] = []


    if request.method == 'POST':
        if 'number_of_people' in request.POST and 'available_row_id' in request.POST and 'total_amount' in request.POST:

            booked_by = request.user.id
            available_row_id = request.POST['available_row_id']
            total_amount = float(request.POST['total_amount'])
            total_members = request.POST['number_of_people']
            total_user_credit = float(request.POST['total_user_credit'])

            if total_user_credit >= total_amount:


                get_main_available_row = availability.objects.get(id=available_row_id)

                get_main_event = excursions.objects.get(id=get_main_available_row.select_excursion)

                send_ex_email(request.user.first_name, get_main_event.excursions_name, get_main_available_row.availability_date, total_members)


                new_booking = booking_details(available_row_id=available_row_id, total_members=total_members, booked_by=booked_by, total_amount=total_amount)
                new_booking.save()

                get_credit_card = credit_cards.objects.get(owner_id=request.user.id)
                get_credit_card.total_credit = get_credit_card.total_credit - total_amount
                get_credit_card.save()



                messages.info(request, "Congratulations! this excursion has been booked.")
            else:
                messages.info(request, "You don't have enough credit to book this excursion!")

        else:
            person_id = request.user.id
            person_name = request.user.first_name
            person_pic = request.user.last_name
            review_msg = request.POST['myReview']
            event_id = request.POST['eventID']
            rating_stars = request.POST['ratings']

            new_rating = ex_reviews(author_id=person_id, author_name=person_name, author_picture=person_pic, review_star=rating_stars, review_msg=review_msg, event_id=event_id)
            new_rating.save()


    isReviewExists = ex_reviews.objects.filter(event_id=id).exists()

    if isReviewExists:
        all_reviews = ex_reviews.objects.filter(event_id=id)
        context['reviews'] = all_reviews


    return render(request, "events.html", context)






def profile(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            card_num = request.POST['card_num']
            exp_date = request.POST['exp_date']
            cvv_num = request.POST['cvv_num']

            new_credit_card = credit_cards(owner_id=request.user.id, exp_date=exp_date, cvv_num=cvv_num, card_number=card_num)
            new_credit_card.save()

            if 'next' in request.POST:
                return redirect(request.POST['next'])

        context['USER'] = whole_person_info(request.user.id)



        return render(request, "member.html", context)
    else:
        return redirect("index")


def logout(request):
    try:
        user_more_info = more_info.objects.get(id=request.user.id)
        user_more_info.isOnline = 0
        user_more_info.save()
        auth.logout(request)
        return redirect("index")
    except:
        auth.logout(request)
        return redirect("index")

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return redirect("login")
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        dob = request.POST['dob']
        pic = request.FILES['image']
        context = {
            "name":name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
            "dob":dob,
            "pic":pic
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email"
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, email=dob, first_name=name, password=pass1, last_name=pic)
            user.save()

            user = auth.authenticate(username=email, password=pass1)
            auth.login(request, user)

            save_img = profile_pics(id=request.user.id, user_img=pic)
            save_img.save()

            send_security_code(request.user.id, request.user.first_name, request.user.username)

            return redirect("authentication")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)



    return render(request, "signup.html")


def authentication(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            myCode = request.POST['s_code']
            hash_converted = convert_code(myCode)

            thisUserCode = user_confirmation.objects.get(id=request.user.id)

            if thisUserCode.code_hash == hash_converted:
                thisUserCode.is_verified = True
                thisUserCode.save()
                return redirect("index")
            else:
                messages.info(request, "Entered code is wrong!")

        return render(request, "authentication.html")
    else:
        return redirect("signup")

def send_security_code(u_id, u_name, u_email):
    # generate code
    security_code = generate_code()

    # save in database

    if user_confirmation.objects.filter(id=u_id).exists():
        finding.code_hash = security_code[1]
        finding.is_verified = False
        finding.save()
    else:
        add_confirmation = user_confirmation(id=u_id, code_hash=security_code[1], is_verified=False)
        add_confirmation.save()

    # send email
    send_html_email(u_name, u_email, security_code[0])


def generate_code():
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    for i in range(0, 6):
        index = randint(0, len(CHAR)-1)
        code += CHAR[index]
    code_hash = hl.md5(code.encode())
    code_hash = code_hash.hexdigest()
    both = (code, code_hash)
    print(both)
    return both

def convert_code(c):
    Hash = hl.md5(c.encode())
    Hash = Hash.hexdigest()
    return Hash

def send_html_email(user_name, user_email, myCode):
    # me == my email address
    # you == recipient's email address
    sender = "***************"
    receiever = user_email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Authentication Code"
    msg['From'] = sender
    msg['To'] = user_email

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hello!\nThanks for register on Excursion.pk\n"
    html = """\
    <html>
      <head></head>
      <body>
        <p><b>Hello {}!</b><br><br>
           Thanks for register on Excursion.pk
           <br>
           Code: <b>{}</b><br>
           Enter the given authentication code in registration form</p>
      </body>
    </html>
    """.format(user_name, myCode)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part o f a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, '************')
    mail.sendmail(sender, user_email, msg.as_string())
    mail.quit()




def send_ex_email(user_name, excursion_name, excursion_booking_date, total_members_booked):
    # me == my email address
    # you == recipient's email address
    sender = "*************"
    user_email = "*************"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Booking confirmation"
    msg['From'] = sender
    msg['To'] = user_email

    # Create the body of the message (a plain-text and an HTML version).
    text = "New booking of Excursion has been received\n"
    html = """\
    <html>
      <head></head>
      <body>
        <p>
           New booking of Excursion has been received
           <br>
           <b><u>Details</u></b><br>
           <b>Username:</b> {}<br>
           <b>User Email:</b> {}<br>
           <b>Excursion Name:</b> {}<br>
           <b>Booking date:</b> {}<br>
           <b>Total members:</b> {}<br>


      </body>
    </html>
    """.format(user_name, user_email, excursion_name, excursion_booking_date, total_members_booked)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part o f a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, '*************')
    mail.sendmail(sender, user_email, msg.as_string())
    mail.quit()
