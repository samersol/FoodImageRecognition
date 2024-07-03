
from bs4 import BeautifulSoup
import requests
import json
from PIL import Image
import numpy as np
from keras.models import load_model
model = load_model('Food30.h5')
import random


labels = {0: 'Fish', 1: 'Hot dog', 2: 'Potato Fries', 3: 'Spaghetti', 4: 'Steak', 5: 'apple_pie', 6: 'baklava',
          7: 'boiled_eggs', 8: 'bread', 9: 'cake', 10: 'cheesecake', 11: 'chicken', 12: 'donuts', 13: 'eggs', 14: 'falafel', 15: 'hamburger', 16: 'hummus',
          17: 'ice_cream', 18: 'lasagna', 19: 'macrons', 20: 'pancakes', 21: 'pizza', 22: 'rice', 23: 'salad', 24: 'salmon', 25: 'sambosk', 26: 'shrimp', 27: 'soup',
          28: 'suchi', 29: 'waffel'}


def processing_image(img):
    img = Image.open(img).resize((224, 224))
    img = np.array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)
    label = np.argmax(pred, axis=1)[0]
    FoodName = labels[label]
    return FoodName


def provide_advice(goal, calories):
    # Based on the user's goal and calories, provide advice
    if goal == "lose":
        if calories > 150:
            advice = "This food is high in calories. Consider choosing a healthier option."
        else:
            advice = "This food is within your calorie limit. Good job!"
    elif goal == "gain":
        if calories < 200:
            advice = "This food is low in calories. Consider adding more nutritious options to your diet."
        else:
            advice = "This food is a good choice for gaining weight. Enjoy!"
    if goal == "maintain":
        if calories > 200:
            advice = "This food is high in calories. Not bad from time to time."
        else:
            advice = "This food is suitable for your goal . but trying aiming for big meal for the rest of the day!"

    return advice


def fetch_calories2(FoodName):



    # Set up the API endpoint
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    # Set up the headers with your application ID and key
    headers = {
        "x-app-id": "e0a784df",
        "x-app-key": "6d5789bb144c38fb972ab588c751d92d",
        "Content-Type": "application/json"
    }

    # Set up the payload with the food name
    payload = {
        "query": FoodName,
        "timezone": "US/Eastern"
    }

    # Send a POST request to the API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Parse the response
    data = response.json()
    # Extract the calories value
    calories = data['foods'][0]['nf_calories']
    return calories
    # Format the food name for the search query

    # # Send a GET request to Google
    # response = requests.get("https://www.google.com/search?q=" + search_query)

    # # Parse the HTML content of the response using BeautifulSoup
    # soup = BeautifulSoup(response.content, "html.parser")

    # # Find the element containing the calories information
    # calories_element = soup.find("div", class_="Z0LcW an_fna")

    # if calories_element:
    #     # Extract the calories value
    #     calories = calories_element.text.split(" ")[0]
    #     return calories
    # else:
    #     return "Calories not found"
