import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Imports related to Watson Natural Language Understanding (NLU)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, SentimentOptions


# To make HTTP GET requests

def get_request(url, **kwargs,):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs)

    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Method to get dealers from a cloud function
# Calls get_request() with specified arguments
# Parses JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result      
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"], 
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], 
                zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_id_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    if json_result:
        # Get the row list in JSON as dealers
        dealer=json_result[0]     

        dealer_obj = CarDealer(
            address=dealer["address"], 
            city=dealer["city"], 
            full_name=dealer["full_name"],
            id=dealer["id"], 
            lat=dealer["lat"], 
            long=dealer["long"],
            short_name=dealer["short_name"],
            st=dealer["st"], 
            zip=dealer["zip"])

    return dealer_obj

# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_by_st_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, st=st)
    if json_result:
        # Get the row list in JSON as dealers
        dealers=json_result      
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"], 
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], 
                zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function


def get_dealer_reviews_from_cf(url, id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,id=id)
    if json_result:
        # Get the row list in JSON as dealers
        reviews=json_result['data']['docs']
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                id=review_doc["id"], 
                name=review_doc["name"], 
                dealership=review_doc["dealership"],
                review=review_doc["review"], 
                purchase=review_doc["purchase"], 
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_model"], 
                car_year=review_doc["car_year"],
                sentiment="positive")
            review_obj.sentiment = analyze_review_sentiments(review_doc["review"])
            results.append(review_obj)

    return results







# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text): 

    url = "https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/c2a00002-1451-4c64-ae8e-fc15145434f9" 
    api_key = "nf2VNgFU39a2bzLyiHvvWfHL4Qqe3gFc92VoJ3ncLK5R" 
    authenticator = IAMAuthenticator(api_key) 
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator) 
    nlu.set_service_url(url) 
    nlu.set_disable_ssl_verification(True)
    try:
        response = nlu.analyze( 
            text=text ,
            features=Features(sentiment=SentimentOptions(targets=[text]))
        ).get_result() 
        label=json.dumps(response, indent=2) 
        label = response['sentiment']['document']['label'] 
    except: 
        label = "neutral"

    return label