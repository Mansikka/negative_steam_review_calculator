from steam_reviews import ReviewLoader
import json
import os




def get_reviews(app_id:int):
    reviews = ReviewLoader().load_from_api(app_id)
    reviews.save_json()

def read_data(data_source:str):
    f = open(data_source)
    data:dict = json.load(f)
    f.close()
    return data

def to_hours(minutes:float):
    minutes = float(minutes)
    hours = minutes/60
    return round(hours, 2)

def percentage(value, total):
    retval = float(value)/total
    retval = round(retval * 100)
    return retval


# Starfield: 1716740
#SETUP
app_id = 1716740 #Your app here
data_source = f'reviews_{app_id}.json'
accept_free = False

#Fetch reviews if no pre-existing data exists
if not os.path.exists(data_source):
    get_reviews(app_id)
#Get the reviews
data = read_data(data_source)
reviews:list[dict] = data.get('reviews', [])

average_playtime = 0
negative_reviews = 0

negative_reviews_playtime = 0
negative_reviews_with_playtime= 0
negative_reviews_with_playtime_more_than_100 = 0
negative_reviews_with_no_playtime = 0

total_playtime_after_negative = 0
total_playtime_after_negative_more_than_100 = 0
total_playtime_after_negative_more_than_50 = 0
total_playtime_after_negative_less_than_10 = 0
average_playtime_after_negative = 0

lowest = 0
highest = 0

for review in reviews:
    voted_up = review.get('voted_up')
    received_for_free = review.get('received_for_free')
    if not voted_up and not received_for_free:
        negative_reviews +=1
        author:dict = review.get('author')
        playtime_forever:int = author.get('playtime_forever', 0)
        playtime_at_review:int = author.get('playtime_at_review', 0)
        playtime_after_review:int = playtime_forever - playtime_at_review
        negative_reviews_playtime += playtime_at_review
        total_playtime_after_negative += playtime_after_review
        average_playtime += playtime_forever
        if playtime_after_review > 0:
            negative_reviews_with_playtime += 1
            if lowest == 0 or playtime_after_review < lowest:
                lowest = playtime_after_review
            if playtime_after_review > highest:
                highest = playtime_after_review
            if to_hours(playtime_after_review) > 100:
                total_playtime_after_negative_more_than_100 += 1
            elif to_hours(playtime_after_review) > 50:
                total_playtime_after_negative_more_than_50 += 1
            elif to_hours(playtime_after_review) < 10:
                total_playtime_after_negative_less_than_10 += 1
        else:
            negative_reviews_with_no_playtime += 1
        
        if to_hours(playtime_at_review) > 100:
            negative_reviews_with_playtime_more_than_100 += 1


average_playtime_after_negative = float(total_playtime_after_negative) / negative_reviews


print('Negative reviews with playtime after view:', negative_reviews_with_playtime, '/', negative_reviews,  f'= {percentage(negative_reviews_with_playtime, negative_reviews)}%')
print('Total playtime after review:', to_hours(total_playtime_after_negative), 'hours')
print('Reviews with more than 100 hours at review:', negative_reviews_with_playtime_more_than_100,  f', {percentage(negative_reviews_with_playtime_more_than_100, negative_reviews)}% of all negatives')
print('Reviews with more than 100 hours after review:', total_playtime_after_negative_more_than_100,  f', {percentage(total_playtime_after_negative_more_than_100, negative_reviews)}% of all negatives')
print('Reviews with more than 50 hours after review:', total_playtime_after_negative_more_than_50,  f', {percentage(total_playtime_after_negative_more_than_50, negative_reviews)}% of all negatives')
print('Reviews with less than 10 hours after review:', total_playtime_after_negative_less_than_10,  f', {percentage(total_playtime_after_negative_less_than_10, negative_reviews)}% of all negatives')
print('Reviews with no playtime after review:', negative_reviews_with_no_playtime,  f', {percentage(negative_reviews_with_no_playtime, negative_reviews)}% of all negatives')
print('Average playtime after review:', to_hours(average_playtime_after_negative), 'hours')
print('Highest playtime after review:', to_hours(highest), 'hours')
print('Lowest playtime after review excluding 0:', to_hours(lowest), 'hours')
print('Average total playtime:', to_hours(average_playtime), 'hours')

