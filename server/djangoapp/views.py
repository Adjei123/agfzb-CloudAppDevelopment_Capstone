from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel, CarMake
# from .restapis import related methods
from.restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/bf04fca2-7896-4254-9996-ca1dcf1b7359/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        context["dealership_list"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request,dealer_id):
    context = {}

    if request.method == "GET":
        url = "https://us-east.functions.appdomain.cloud/api/v1/web/bf04fca2-7896-4254-9996-ca1dcf1b7359/dealership-package/get-review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)

        # Get Dealer name to pass to context
        dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/bf04fca2-7896-4254-9996-ca1dcf1b7359/dealership-package/get-dealership"
        dealer_name = get_dealer_by_id_from_cf(dealer_url, dealer_id).full_name
        
        # Concat all dealer's short name
        #dealer_reviews = ' '.join([rev.review for rev in reviews])
        #dealer_sentiments = ' '.join([rev.sentiment for rev in reviews])
        # Return a list of dealer short name
        context["review_list"] = reviews
        context["current_page"] = "dealer_details"
        context["dealer_id"] = dealer_id
        context["dealer_name"] = dealer_name
 
        #return HttpResponse(dealer_reviews + dealer_sentiments)
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# ...
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":

        # Get list of cars from dealership
        dealership_cars = CarModel.objects.filter(dealer_id=dealer_id)

        # Get dealership name
        dealer_url = "https://us-east.functions.appdomain.cloud/api/v1/web/bf04fca2-7896-4254-9996-ca1dcf1b7359/dealership-package/get-dealership"
        dealer_name = get_dealer_by_id_from_cf(dealer_url, dealer_id).full_name

        # Add dealer_name and cars to context to be used in template display
        context["dealer_name"] = dealer_name
        context["cars"] = dealership_cars
        context["dealer_id"] = dealer_id
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        post_url = "https://us-east.functions.appdomain.cloud/api/v1/web/bf04fca2-7896-4254-9996-ca1dcf1b7359/dealership-package/post-review"
        car_id = request.POST["car"]
        car = CarModel.objects.get(pk=car_id)
        review = {
        "id": dealer_id,
        "name": request.user.username,
        "dealership": dealer_id,
        "review": request.POST["content"],
        "purchase": "false",
        "purchase_date": request.POST["purchasedate"],
        "car_make": car.make.name,
        "car_model": car.name,
        "car_year": car.year
        }  
        if "purchasecheck" in request.POST:
            if request.POST["purchasecheck"] == 'on':
                review["purchase"] = True 

        json_payload = {}
        json_payload["review"] = review
        post_request(post_url, json_payload, dealer_id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)