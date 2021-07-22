import json
import datetime
import math
import time
from glicko2 import Player


def date_sort_function(a_fight):
    """Outputs the date of a fight in integer format, 2015-12-30 = 20151230"""
    if a_fight["date"] == "UNKNOWN":
        return 1
    a_fight_string = a_fight["date"].replace("-","")
    return int(a_fight_string)


def sort_by_date(a_list):
    """Returns a list of fights(sets) sorted by date"""
    a_list.sort(key=date_sort_function)
    return a_list


def format_date(a_str):
    """Returns a date object"""
    if a_str.find(",") > 0:
        some_str = a_str.split(",")
        date_string = ''.join([str(element) for element in some_str])
        date_string_list = date_string.split()
    else:
        date_string_list = a_str.split()
    year = ""
    month = ""
    day = ""
    if len(date_string_list) == 1:
        year = date_string_list[0]
    else:
        for element in date_string_list:
            if not element.isdigit():
                months_list = ["January", "February", "March", "April", "May", "June",
                               "July", "August", "September", "October", "November", "December"]
                for i, a_month in enumerate(months_list):
                    if element == a_month or element == a_month[:3]:
                        month = i+1
            elif len(element) == 4:
                year = element
            elif element.isdigit() and len(element) <= 2:
                day = element
            else:
                pass
                # print("The element: %s" % element)
    if year == "":
        return "UNKNOWN"
    if month == "":
        month = 1
    if day == "":
        day = 1
    d = datetime.date(int(year), int(month), int(day)).strftime("%Y-%m-%d")
    return d


def compare_dates(date1, date2):
    """Returns 1 if date1 is later than date2, 0 if equal, -1 otherwise"""
    assert(type(date1) == datetime.date)
    assert(type(date2) == datetime.date)
    a_str = "Date1 elements:\nDay: %s, Month: %s, Year: %s" % (date1.day, date1.month, date1.year)
    a_str += "\nDate2 elements:\nDay: %s, Month: %s, Year: %s" % (date2.day, date2.month, date2.year)
    # print(a_str)
    if date1.year > date2.year:
        return 1
    elif date1.year < date2.year:
        return -1
    elif date1.month > date2.month:
        return 1
    elif date1.month < date2.month:
        return -1
    elif date1.day > date2.day:
        return 1
    elif date1.day < date2.day:
        return -1
    else:
        return 0


def date_difference(date1, date2):
    """Return the difference of two dates in years"""
    assert (type(date1) == datetime.date)
    assert (type(date2) == datetime.date)
    #time_change = datetime.timedelta(days=num_days)
    #new_d = a_date + time_change
    #return new_d
    pass


def elo_formula(elo1, elo2, k, d):
    if d == 1:
        w1 = 1
        w2 = 0
    else:
        w1 = 0
        w2 = 1
    p1 = (1 / (1 + pow(10, ((elo2-elo1)/400))))
    p2 = (1 / (1 + pow(10, ((elo1 - elo2) / 400))))
    rating1 = round(elo1 + (k * (w1 - p1)), 2)
    rating2 = round(elo2 + (k * (w2 - p2)), 2)
    return (rating1, rating2)


def find_fighters_elo(all_fights, an_elo_dict):
    unknown_fighter_dict = {}
    for a_fight in all_fights:
        if a_fight['fighterB'] not in an_elo_dict:
            unknown_fighter_dict[a_fight['fighterB']] = 1000
    an_elo_dict.update(unknown_fighter_dict)
    for fight in all_fights:
        a_str = "%s vs %s. fighterA result: %s" % (fight['fighterA'], fight['fighterB'], fight['result'])
        a_str += "\n\tfighterA ELO before: %s, fighterB ELO before: %s" % \
                 (an_elo_dict[fight['fighterA']], an_elo_dict[fight['fighterB']])
        result = -1
        if fight['result'].lower() == 'win':
            result = 1
        elif fight['result'].lower() == 'loss':
            result = 0
        if result != -1:
            new_elo = elo_formula(an_elo_dict[fight['fighterA']], an_elo_dict[fight['fighterB']], 30, result)
            an_elo_dict[fight['fighterA']] = new_elo[0]
            an_elo_dict[fight['fighterB']] = new_elo[1]
            a_str += "\n\tfighterA ELO after: %s, fighterB ELO after: %s" % \
                 (an_elo_dict[fight['fighterA']], an_elo_dict[fight['fighterB']])
        else:
            a_str += "\n\tIgnored string: " + fight['result']
        #print(a_str)
    return an_elo_dict


def sort_fighters_elo(a_list):
    a_list.sort(reverse=True, key=elo_sort_function)
    return a_list


def elo_sort_function(a_fighter):
    return a_fighter[1]


def write_elo(elo_list, filename):
    with open(filename, "w", encoding="utf-8") as handle:
        for a_fighter in elo_list:
            handle.write(f'Fighter: {a_fighter[0]:26} ELO: {a_fighter[1]}' + "\n")


def print_elo(elo_list):
    for a_fighter in elo_list:
        print(f'Fighter: {a_fighter[0]:26} ELO: {a_fighter[1]}')


def write_glicko2(glicko2_list, filename):
    with open(filename, "w", encoding="utf-8") as handle:
        for a_fighter in glicko2_list:
            handle.write(f'Fighter: {a_fighter[0]:26} Glicko2: {a_fighter[1][0]}' + "\n")


def print_glicko2(glicko2_list):
    for a_fighter in glicko2_list:
        print(f'Fighter: {a_fighter[0]:26} Glicko2: {a_fighter[1][0]}')


def find_fighters_glicko2(all_fights, rating_dict, fighter_dict):
    """ Update dict with unknown fighters.
        For each fighter, find their fights within a rating period.
        Save glicko2 result to temp array and repeat with all fighters.
        After rating period, original array = temp array"""
    unknown_fighter_dict = {}
    parsed_fights = []
    for a_fight in all_fights:
        if a_fight['fighterB'] not in rating_dict:
            unknown_fighter_dict[a_fight['fighterB']] = (1500, 350, .06)
        if a_fight['date'] != "UNKNOWN":
            parsed_fights.append(a_fight)
    rating_dict.update(unknown_fighter_dict)
    earliest_date = parsed_fights[0]['date']
    latest_date = parsed_fights[len(parsed_fights)-1]['date']
    the_rating_period = 300
    current_date = earliest_date
    while compare_dates(string_to_date(current_date),string_to_date(latest_date)) < 0:
        temp_rating_dict = rating_dict
        # print("Current date: " + current_date)
        for i, a_key in enumerate(fighter_dict):
            #print("Fighter: " + a_key)
            fights_in_period = find_fights_from_date(a_key, fighter_dict, current_date, the_rating_period)
            if fights_in_period:
                # print("Rating before the rating period: " + str(rating_dict[a_key][0]))
                rating_list = []
                rd_list = []
                decision_list = []
                # Create a temp list containing all fighter's ratings before the time period
                for a_fight in fights_in_period:
                    # Find the rating and RD of all the fighter's opponents in the given time period
                    the_fighter_name = a_fight['fighterB']
                    rating_list.append(str(rating_dict[the_fighter_name][0]))
                    rd_list.append(str(rating_dict[the_fighter_name][1]))
                    decision_list.append(parse_outcome(a_fight['result']))
                rating_list = [math.floor(float(elem)) for elem in rating_list]
                rd_list = [math.floor(float(elem)) for elem in rd_list]
                a_glicko_fighter = Player(rating=rating_dict[a_key][0], rd=rating_dict[a_key][1], vol=rating_dict[a_key][2])
                a_glicko_fighter.update_player(rating_list, rd_list, decision_list)
                # print("Rating after the rating period: " + str(a_glicko_fighter.getRating()))
                temp_rating_dict[a_key] = (round(a_glicko_fighter.getRating(),2), round(a_glicko_fighter.getRd(),2), round(a_glicko_fighter._getVol(),2))
        current_date = str(add_days_to_date(string_to_date(current_date), the_rating_period))
        rating_dict = temp_rating_dict # update temp list with updated ratings after rating period
    return rating_dict


def has_fights_in_period(fighter_name, fighter_dict, current_date, period):
    """ Returns true if fighter has fights in the given time period"""
    pass


def parse_outcome(a_str):
    if a_str.lower() == "win":
        return True
    elif a_str.lower() == "loss":
        return False
    else:
        return False


def find_fights_from_date(target_fighter, fight_dictionary, start_date, rating_period):
    fights = fight_dictionary[target_fighter]["fights"]
    for a_fight in fights:
        if a_fight['date'] != 'UNKNOWN':
            a_fight['date'] = string_to_date(a_fight['date'])
    start_date = string_to_date(start_date)
    end_date = add_days_to_date(start_date, rating_period)
    targeted_fights = []
    for a_fight in fights:
        if a_fight['date'] != 'UNKNOWN' and compare_dates(a_fight['date'], start_date) > 0 and compare_dates(a_fight['date'], end_date) < 0:
            targeted_fights.append(a_fight)
    for a_fight in fights:
        a_fight['date'] = str(a_fight['date'])
    targeted_fights.reverse()
    return targeted_fights


def find_most_recent_fight_date(target_fighter, fight_dictionary):
    the_fights = fight_dictionary[target_fighter]["fights"]
    return the_fights[0]["date"]


def add_days_to_date(a_date, num_days):
    """ Make a datetime.datetime object from str, add days, return a str """
    time_change = datetime.timedelta(days=num_days)
    new_d = a_date + time_change
    return new_d


def string_to_date(a_str):
    nums = a_str.split("-")
    d = datetime.date(int(nums[0]), int(nums[1]), int(nums[2]))
    return d


def parse_results(a_string):
    # Return 1 if win, 0 if loss
    pass

start_time = time.time()
with open("FOC_fighter_stats.json", "r", encoding="utf-8") as handle:
    data = json.load(handle, strict=False)
data = data["data"]
fighter_key_string_list = [str(fighter.keys()) for fighter in data]
fighter_names = [fighter[fighter.find("[")+2:fighter.rfind("]")-1] for fighter in fighter_key_string_list]
fighter_dict = {a_fighter:{"stats":"","fights":""} for a_fighter in fighter_names}
all_fights_in_dict = []
for i, fighter in enumerate(fighter_names):
    fighter_dict[fighter] = {"stats":data[i][fighter]["stats"],"fights":data[i][fighter]["fights"]}
for a_fighter in fighter_dict:
    fights = fighter_dict[a_fighter]["fights"]
    for a_fight in fights:
        a_fight["date"] = format_date(a_fight["date"])
        all_fights_in_dict.append(a_fight)
sorted_fights = sort_by_date(all_fights_in_dict)
find_most_recent_fight_date("Conor McGregor", fighter_dict)
elo_dict = {a_name:1000 for a_name in fighter_names}
elo_result = find_fighters_elo(sorted_fights, elo_dict)
elo_result_list = [(name, elo_result[name]) for name in fighter_names]
sorted_elo_result = sort_fighters_elo(elo_result_list)
write_elo(sorted_elo_result, "FOC_elo.txt")
# glicko2_dict = {a_name:(1500, 350, .06) for a_name in fighter_names}
# glicko2_result = find_fighters_glicko2(sorted_fights, glicko2_dict, fighter_dict)
# glicko2_result_list = [(name, glicko2_result[name]) for name in fighter_names]
# sorted_glicko2_result = sort_fighters_elo(glicko2_result_list)
# write_glicko2(sorted_glicko2_result, "FOC_glicko2.txt")
rounded_time = round(time.time() - start_time, 3)
print("--- %s second runtime to calculate rankings ---" % rounded_time)
print(compare_dates(string_to_date("2012-12-01"), string_to_date("2018-03-22")))