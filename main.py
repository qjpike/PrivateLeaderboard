import json
from datetime import datetime
import pytz
import requests

class Person:
    def __init__(self,name, id):
        self.name = name
        self.points = 0
        self.last_star = 0
        self.scoreboard = {}

    def __eq__(self,other):
        return self.name == other


def print_ts(ts_str):
    tz = pytz.timezone("US/Eastern")
    timestamp = datetime.utcfromtimestamp(ts_str)
    timestamp = timestamp.replace(tzinfo=pytz.utc)
    timestamp = timestamp.astimezone(tz)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def get_data():
    url = "https://adventofcode.com/2020/leaderboard/private/view/614401.json"
    r = requests.get(url)
    print(r.json())
    # f = open(r.text)
    # return json.loads(f.read().strip())

def main():
    f = open("data.json")
    dat = f.read().strip()
    # info = get_data()
    tz = pytz.timezone("US/Eastern")

    info = json.loads(dat)

    people = []
    users = info['members']
    for id in users:
        a = Person(users[id]['name'], id)
        for i in range(1,len(users[id]['completion_day_level'])+1):
            for j in range(1,len(users[id]['completion_day_level'][str(i)])+1):
                a.scoreboard[(i,j)] = int(users[id]['completion_day_level'][str(i)][str(j)]['get_star_ts'])
        people.append(a)

    day = 4
    print("User                     ",end='')
    for i in range(day):
        print("Day " + str(i + 1) + " Part 1             Day " + str(i + 1) + " Part 2             ",end='')
    print("")
    for a in people:
        print(f'{a.name:25s}', end='')
        for i in range(day):

            if people[people.index(a)].scoreboard.__contains__((i+1,1)):
                print(f'{print_ts(people[people.index(a)].scoreboard[(i+1,1)]):25s}',end='')
            if people[people.index(a)].scoreboard.__contains__((i+1,2)):
                print(f'{print_ts(people[people.index(a)].scoreboard[(i+1,2)]):25s}',end='')

        print("")





if __name__=="__main__":
    main()