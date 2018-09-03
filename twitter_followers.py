import core
import json
import time

def main_loop():
    next_batch = -1
    data_bel = {}
    data_bel["Bedrijven"] = []

    data_int = {}
    data_int["Bedrijven"] = []
    count = 1
    while(next_batch is not 0):
        print("Starting new batch")
        try:
            followers = core.api.GetFollowerIDsPaged(screen_name='SofieStael', cursor=next_batch, count=200)
        except core.twitter.TwitterError:
            print("Sleeping")
            time.sleep(60 * 15)
        next_batch = followers[0]
        for follower in followers[2]:
            try:
                user = core.api.GetUser(follower, return_json=True)
            except core.twitter.TwitterError:
                print("Sleeping")
                time.sleep(60 * 15)
            print(count, ": ", user["name"])
            count+= 1
            if(valid_company(user)):
                loc = location(user) 
                if(loc == "BE"):
                    data_bel["Bedrijven"].append({
                        "name": user["name"],
                        "url": user["entities"]["url"]["urls"][0]["expanded_url"]
                    })
                elif(loc == "INT"):
                    data_int["Bedrijven"].append({
                        "name": user["name"],
                        "url": user["entities"]["url"]["urls"][0]["expanded_url"]
                    })
    
    with open('Sofie_be.json', 'w') as output_bel:
        json.dump(data_bel, output_bel)
    with open('Sofie_int.json', 'w') as output_int:
        json.dump(data_int, output_int)

    print('Done')

def valid_company(user):
    invalid_urls = ["facebook", "linkedin", "twitter", "kickstarter", "about.me"]

    try:
        website = user["entities"]["url"]["urls"][0]["expanded_url"]
    except:
        return False
    if(website is None):
        return False
    if(any(url in website for url in invalid_urls)):
        return False
    
    return True
def location(user):
    valid_location_belgium = ["belgian", "belgium", "belgië", "brussels", "vlaanderen", "belgique", "brussel"]
    location = user["location"]

    if(any(valid_location in location.lower() for valid_location in valid_location_belgium)):
        return "BE"
    else:
        return "INT"
    
    return False
    #if(any())

main_loop()
# with open('test.json', 'w') as output:
#     json.dump(core.api.GetUser(screen_name='iReachm', return_json=True), output)