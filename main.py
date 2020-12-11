import json
from datetime import datetime
import pytz
import requests
import collections

class Scoreboard:
    def __init__(self):
        self.people = []

    def add(self,Person):
        sb_key = list(Person.scoreboard.keys())
        sb_key.sort()
        if len(sb_key) > 0:
            Person.last_star = Person.scoreboard[sb_key[-1]]
        self.people.append(Person)

    def sort(self):
        self.people.sort(reverse=True)

    def calc_points(self):
        for i in range(2,52):
            times = {}
            for j in self.people:
                if (i//2, i%2+1) in j.scoreboard:
                    times[j.name] = j.scoreboard[(i//2,i%2+1)]
            z = len(self.people)
            for j in sorted(times,key = times.get):
                self.people[self.people.index(j)].scores[i] = z
                z -= 1

        for person in self.people:
            person.calc_score()


class Person(Scoreboard):
    def __init__(self,name):
        self.name = name
        self.points = 0
        self.last_star = 0
        self.scoreboard = {}
        self.scores = {}

    def __eq__(self,other):
        return self.name == other

    def get_time(self,day,part):
        return self.scoreboard[(day,part)]

    def __lt__(self,other):
        if self.points < other.points:
            return True
        else:
            if self.points == other.points:

                return self.last_star < other.last_star

        return False

    def calc_score(self):
        self.points = sum(list(self.scores.values()))
        if 2 in self.scores:
            self.points -= self.scores[2]
        if 3 in self.scores:
            self.points -= self.scores[3]



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

    sb = Scoreboard()
    users = info['members']
    z = 50
    for id in users:
        a = Person(users[id]['name'])
        for i in list(users[id]['completion_day_level'].keys()):
            for j in list(users[id]['completion_day_level'][str(i)]):
                a.scoreboard[(int(i),int(j))] = int(users[id]['completion_day_level'][str(i)][str(j)]['get_star_ts'])
        a.points = z
        sb.add(a)
    sb.calc_points()
    sb.sort()
    day_start = 0
    day_end = 11
    empty = ' '
    print("User                           ",end='')
    for i in range(day_start,day_end):
        print("Day " + str(i + 1) + " Part 1             Day " + str(i + 1) + " Part 2             ",end='')
    print("")
    for a in sb.people:
        print(f'{a.name:25s}', end='')
        print(f'{str(a.points):6s}',end='')
        for i in range(day_start,day_end):

            if sb.people[sb.people.index(a)].scoreboard.__contains__((i+1,1)):
                print(f'{print_ts(sb.people[sb.people.index(a)].scoreboard[(i+1,1)]):25s}',end='')
            else:
                print('                         ',end='')
            if sb.people[sb.people.index(a)].scoreboard.__contains__((i+1,2)):
                print(f'{print_ts(sb.people[sb.people.index(a)].scoreboard[(i+1,2)]):25s}',end='')
            else:
                print('                         ', end='')

        print("")

    f = open("q_stats.txt")
    a = f.readlines()

    for i in a:
        j = i
        i = i.split()
        # print("Day " + str(a.index(j) + 1) + ": " + i[2] + " " + i[5] + " " + str(int(i[5])/int(i[2])))



if __name__=="__main__":
    main()