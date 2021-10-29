import json
import datetime


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
    if year == "" or year == "Win" or year == "Loss":
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
    """ To determine if fighters are retired or not """
    the_fights = fight_dictionary[target_fighter]["fights"]
    return the_fights[0]["date"]


def find_most_recent_x_fights(target_fighter, fight_dictionary, num_fights):
    the_fights = fight_dictionary[target_fighter]["fights"]
    total_fights = len(the_fights)
    targeted_fights = []
    if total_fights < num_fights:
        return the_fights
    else:
        for i in range(0, num_fights):
            targeted_fights.append(the_fights[i])
    return targeted_fights


def find_dwyer_score(some_fights):
    """Return the current fighter's streak. Negative if losing streak, positive if winning"""
    most_recent_outcome = some_fights[0]['result']
    streak = 0
    for a_fight in some_fights:
        if a_fight['result'] == most_recent_outcome:
            streak = streak + 1
        else:
            break
    if most_recent_outcome.lower() == 'loss':
        return -1*streak
    else:
        return streak


def add_days_to_date(a_date, num_days):
    """ Make a datetime.datetime object from str, add days, return a str """
    time_change = datetime.timedelta(days=num_days)
    new_d = a_date + time_change
    return new_d


def string_to_date(a_str):
    nums = a_str.split("-")
    d = datetime.date(int(nums[0]), int(nums[1]), int(nums[2]))
    return d


def find_basic_odds(fighterA, fighterB, a_glicko_dict):
    glickoA = a_glicko_dict[fighterA]
    glickoB = a_glicko_dict[fighterB]
    a = False
    if glickoA > glickoB:
        ratio = glickoA / glickoB
        a = True
    else:
        ratio = glickoB / glickoA
    factor = 1.5
    result = ratio*factor*100
    result = round(result, 0)
    # print("The ratio: " + str(result))
    if a:
        return (fighterA,-1*result)
    else:
        return (fighterB,-1*result)


def read_json_fighter_data_from_file(filename):
    """ Returns dictionary of all fighters and a sorted list of all fights """
    with open(filename, "r", encoding='utf-8') as handle:
        data = json.load(handle, strict=False)
    data = data['data']
    fighter_key_string_list = [str(fighter.keys()) for fighter in data]
    fighter_names = [fighter[fighter.find("[") + 2:fighter.rfind("]") - 1] for fighter in fighter_key_string_list]
    fighter_dict = {a_fighter: {"stats": "", "fights": ""} for a_fighter in fighter_names}
    all_fights_in_dict = []
    for i, fighter in enumerate(fighter_names):
        fighter_dict[fighter] = {"stats": data[i][fighter]["stats"], "fights": data[i][fighter]["fights"]}
    for a_fighter in fighter_dict:
        fights = fighter_dict[a_fighter]["fights"]
        for a_fight in fights:
            a_fight["date"] = format_date(a_fight["date"])
            all_fights_in_dict.append(a_fight)
    sorted_fights = sort_by_date(all_fights_in_dict)
    return (fighter_dict, sorted_fights, fighter_names)


def format_fighter_stats(fighter_name, fighter_dict):
    a_str = "STATS\n"
    a_str += 'Name: ' + fighter_dict[fighter_name]['stats']['name'] + "\n"
    division = fighter_dict[fighter_name]['stats']['division']
    if len(division) > 1:
        a_str += 'Divisions fought in: '
        for d in division:
            a_str += '\n\t' + d
    else:
        a_str += 'Division: ' + division[0]
    a_str += '\nWeight: ' + remove_special_character(fighter_dict[fighter_name]['stats']['weight']) + '\n'
    a_str += 'CALCULATED STATS\n'
    dwyer = find_dwyer_score(fighter_dict[fighter_name]['fights'])
    dwyer = str(dwyer)
    a_str += 'Dwyer score: ' + dwyer + '\n'
    return a_str


def remove_special_character(a_word):
    if a_word.find('//') > 0:
        return a_word[:a_word.find('//')]
    return a_word


def format_fighter_fights(fighter_name, fighter_dict):
    the_fights = fighter_dict[fighter_name]['fights']
    a_str = "FIGHTS\n"
    for f in the_fights:
        #f'Fighter: {a_fighter[0]:26} Glicko2: {a_fighter[1][0]}' + "\n"
        a_str += f'Fighter A: {f["fighterA"]:26} FighterB: {f["fighterB"]}' + '\n'
        a_str += fighter_name + ' ' + f['result'] + ' by ' + f['method'] + ' at ' +\
               f['time'] + ' of round ' + f['roundFinished'] + ' on ' + f['date'] + '\n'
    return a_str


def format_all_fighter_stats(fighter_name, fighter_dict):
    a_str = format_fighter_stats(fighter_name, fighter_dict) + format_fighter_fights(fighter_name, fighter_dict)
    return a_str


def read_glicko_ranking(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        some_data = fh.readlines()
    a_glicko_dict = {}
    for a_data in some_data:
        the_glicko = a_data[a_data.rfind("2:") + 3:-1]
        the_name = a_data[9:a_data.find("Glicko")]
        the_name = the_name.rstrip()
        a_glicko_dict[the_name] = float(the_glicko)
    return a_glicko_dict


def main():
    a_tuple = read_json_fighter_data_from_file("FOC_collect_stats/FOC_basic_fighter_stats.json")
    fighter_dict = a_tuple[0]
    sorted_fights = a_tuple[1]
    fighter_names = a_tuple[2]
    a_glicko_dict = read_glicko_ranking("FOC_rankings_generator/FOC_glicko2.txt")
    command = ""
    while command.lower() != 'exit':
        command = input("Enter some command: ")
        command_list = command.split()
        if len(command_list) > 1:
            if command_list[0].lower() == 'stats':
                fighter_name = (command_list[1] + " " + command_list[2])
                print(format_fighter_stats(fighter_name, fighter_dict))
            elif command_list[0].lower() == 'fights':
                fighter_name = (command_list[1] + " " + command_list[2])
                print(format_fighter_fights(fighter_name, fighter_dict))
            elif command_list[0].lower() == 'fighter':
                fighter_name = (command_list[1] + " " + command_list[2])
                print(format_all_fighter_stats(fighter_name, fighter_dict))
            elif command_list[0].lower() == 'odds':
                fighter_nameA = (command_list[1] + " " + command_list[2])
                fighter_nameB = (command_list[3] + " " + command_list[4])
                the_odds = find_basic_odds(fighter_nameA, fighter_nameB, a_glicko_dict)
                print("Favorite: " + the_odds[0])
                print("Odds: " + str(the_odds[1]))


if __name__ == "__main__":
    main()