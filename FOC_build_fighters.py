from FOC_file_read_functions import get_names_and_urls
from FOC_Fighter import Fighter
from FOC_Fight import Fight
from FOC_collect_stats.FOC_get_detailed_fighter_stats import read_detailed_stats_from_file
from FOC_algorithms.FOC_calculate_basic_fight_odds import read_json_fighter_data_from_file


def build_fighter_object_dictionary():
    detailed_stats_dict = read_detailed_stats_from_file("../FOC_collect_stats/FOC_detailed_fighter_stats.json")
    fighter_dict = read_json_fighter_data_from_file("../FOC_collect_stats/FOC_basic_fighter_stats.json")[0]
    fighter_names = get_names_and_urls("../FOC_collect_stats/FOC_basic_fighter_stats.json")[0]
    object_dict = {}
    i = 0
    while i < len(fighter_names):
        stats_dict = fighter_dict[fighter_names[i]]['stats']
        fights_list = fighter_dict[fighter_names[i]]['fights']
        the_name = stats_dict['name']
        the_weight = stats_dict['weight']
        the_division = stats_dict['division']
        fight_object_list = []
        for a_fight in fights_list:
            fight_object_list.append(Fight(a_fight['fighterA'], a_fight['fighterB'],
                                           a_fight['result'], a_fight['method'],
                                           a_fight['date'], a_fight['roundFinished'], a_fight['time']))
        if fighter_names[i] not in detailed_stats_dict:
            detailed_stats = {}
        else:
            detailed_stats = detailed_stats_dict[fighter_names[i]]
        fighter_object = Fighter(the_name, the_weight, the_division, fight_object_list, detailed_stats)
        object_dict[fighter_names[i]] = fighter_object
        i = i+1
    return object_dict


def main():
    pass


if __name__ == "__main__":
    main()
