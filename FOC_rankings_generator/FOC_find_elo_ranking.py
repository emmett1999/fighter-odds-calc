from FOC_calculate_basic_fight_odds import read_json_fighter_data_from_file
import datetime
import math


def write_elo(elo_list, filename):
    with open(filename, "w", encoding="utf-8") as handle:
        for a_fighter in elo_list:
            handle.write(f'Fighter: {a_fighter[0]:26} ELO: {a_fighter[1]}' + "\n")


def sort_fighters_elo(a_list):
    a_list.sort(reverse=True, key=elo_sort_function)
    return a_list


def elo_sort_function(a_fighter):
    return a_fighter[1]


def print_elo(elo_list):
    for a_fighter in elo_list:
        print(f'Fighter: {a_fighter[0]:26} ELO: {a_fighter[1]}')


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


def main():
    a_tuple = read_json_fighter_data_from_file("../FOC_collect_stats/FOC_basic_fighter_stats.json")
    fighter_dict = a_tuple[0]
    sorted_fights = a_tuple[1]
    fighter_names = a_tuple[2]
    elo_dict = {a_name: 1000 for a_name in fighter_names}
    elo_result = find_fighters_elo(sorted_fights, elo_dict)  # a dictionary
    elo_result_list = [(name, elo_result[name]) for name in fighter_names]
    sorted_elo_result = sort_fighters_elo(elo_result_list)
    print_elo(sorted_elo_result)
    write_elo(sorted_elo_result, "FOC_elo.txt")


if __name__ == "__main__":
    main()