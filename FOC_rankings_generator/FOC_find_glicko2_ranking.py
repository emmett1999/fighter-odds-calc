from FOC_calculate_basic_fight_odds import read_json_fighter_data_from_file
from FOC_rankings_generator.glicko2 import Player
import datetime
import math
import json


def write_glicko2(glicko2_list, filename):
    with open(filename, "w", encoding="utf-8") as handle:
        for a_fighter in glicko2_list:
            handle.write(f'Fighter: {a_fighter[0]:26} Glicko2: {a_fighter[1][0]}' + "\n")


def print_glicko2(glicko2_list):
    for a_fighter in glicko2_list:
        print(f'Fighter: {a_fighter[0]:26} Glicko2: {a_fighter[1][0]}')


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


def string_to_date(a_str):
    nums = a_str.split("-")
    d = datetime.date(int(nums[0]), int(nums[1]), int(nums[2]))
    return d


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


def parse_outcome(a_str):
    if a_str.lower() == "win":
        return True
    elif a_str.lower() == "loss":
        return False
    else:
        return False


def add_days_to_date(a_date, num_days):
    """ Make a datetime.datetime object from str, add days, return a str """
    time_change = datetime.timedelta(days=num_days)
    new_d = a_date + time_change
    return new_d


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
    with open("../FOC_expand_database/FOC_potential_fighters.json", "w", encoding='utf-8') as fh:
        fh.write(json.dumps(unknown_fighter_dict, indent=4))
    rating_dict.update(unknown_fighter_dict)
    earliest_date = "2000-01-01"
    print(earliest_date)
    latest_date = parsed_fights[len(parsed_fights)-1]['date']
    print(latest_date)
    the_rating_period = 300
    current_date = earliest_date
    while compare_dates(string_to_date(current_date),string_to_date(latest_date)) < 0:
        temp_rating_dict = rating_dict
        # print("Current date: " + current_date)
        for i, a_key in enumerate(fighter_dict):
            print("Finding odds for " + a_key + "...")
            fights_in_period = find_fights_from_date(a_key, fighter_dict, current_date, the_rating_period)
            print(fights_in_period)
            if fights_in_period != []:
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
                # print("HERE")
                rating_list = [math.floor(float(elem)) for elem in rating_list]
                rd_list = [math.floor(float(elem)) for elem in rd_list]
                a_glicko_fighter = Player(rating=rating_dict[a_key][0], rd=rating_dict[a_key][1], vol=rating_dict[a_key][2])
                if a_key != "Donald Sanchez": # THIS IS THE SMELLIEST OF CODE SMELLS, BUT I JUST GOTTA FIGURE OUT WTF IS WRONG WITH THIS ONE GUY
                    a_glicko_fighter.update_player(rating_list, rd_list, decision_list)
                temp_rating_dict[a_key] = (round(a_glicko_fighter.getRating(),2), round(a_glicko_fighter.getRd(),2), round(a_glicko_fighter._getVol(),2))
                print("Key: " + a_key + "0: " + str(temp_rating_dict[a_key][0]) + " 1: " + str(temp_rating_dict[a_key][1]) + " 2: " + str(temp_rating_dict[a_key][2]))
        current_date = str(add_days_to_date(string_to_date(current_date), the_rating_period))
        print(current_date)
        rating_dict = temp_rating_dict # update temp list with updated ratings after rating period
    return rating_dict


def sort_fighters_elo(a_list):
    a_list.sort(reverse=True, key=elo_sort_function)
    return a_list


def elo_sort_function(a_fighter):
    return a_fighter[1]


a_tuple = read_json_fighter_data_from_file("../FOC_collect_stats/FOC_basic_fighter_stats.json")
fighter_dict = a_tuple[0]
sorted_fights = a_tuple[1]
fighter_names = a_tuple[2]
glicko2_dict = {a_name:(1500, 350, .06) for a_name in fighter_names}
glicko2_result = find_fighters_glicko2(sorted_fights, glicko2_dict, fighter_dict) # a dictionary
glicko2_result_list = [(name, glicko2_result[name]) for name in fighter_names]
sorted_glicko2_result = sort_fighters_elo(glicko2_result_list)
print_glicko2(sorted_glicko2_result)
write_glicko2(glicko2_result_list, "FOC_glicko2.txt")
