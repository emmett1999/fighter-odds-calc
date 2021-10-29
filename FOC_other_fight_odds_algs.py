from FOC_build_fighters import build_fighter_object_dictionary
from FOC_Fighter import Fighter
from FOC_Fight import Fight
from FOC_calculate_basic_fight_odds import read_glicko_ranking
from FOC_calculate_basic_fight_odds import find_basic_odds
# TODO: In build fighter object dictionary, limit each fighter to one weight class

fighterA = "Jorge Masvidal"
fighterB = "Kamaru Usman"

def find_average_stats():
    """Return an 8-tuple of average stats for all fighters in a weightclass"""
    pass


def generalize_style():
    """Return a 8-tuple of my stat ratios relative to the average"""
    pass


def find_common_opponents(fighterA_name, fighterB_name, a_fighter_dict):
    """Return a list of common opponents"""
    fighter_a = a_fighter_dict[fighterA_name]
    fighter_b = a_fighter_dict[fighterB_name]
    fighterA_opponents = [fight.fighterB for fight in fighter_a.fights]
    fighterB_opponents = [fight.fighterB for fight in fighter_b.fights]
    common_opponent_list = set(fighterA_opponents) & set(fighterB_opponents)
    return common_opponent_list


def common_opponent_advantage(fighterA_name, fighterB_name, a_fighter_dict):
    """Return ratio of common opponent advantage"""
    fighter_a = a_fighter_dict[fighterA_name]
    fighter_a_fights = fighter_a.fights
    fighter_b = a_fighter_dict[fighterB_name]
    fighter_b_fights = fighter_b.fights
    common_opponents = find_common_opponents(fighterA_name, fighterB_name, a_fighter_dict)
    common_opponents_object_a = [fight for fight in fighter_a_fights if fight.fighterB in common_opponents]
    common_opponents_object_b = [fight for fight in fighter_b_fights if fight.fighterB in common_opponents]
    fighter_a_dict = {}
    fighter_b_dict = {}
    for f in common_opponents_object_a:
        fighter_a_dict[f.fighterB] = []
        fighter_b_dict[f.fighterB] = []
    for fight in common_opponents_object_a:
        fighter_a_dict[fight.fighterB].append((fight.result, fight.date))
    for fight in common_opponents_object_b:
        fighter_b_dict[fight.fighterB].append((fight.result, fight.date))
    opponent_result_dict_a = find_opponent_result_dict(fighter_a_dict)
    opponent_result_dict_b = find_opponent_result_dict(fighter_b_dict)
    result_list_a = [] # list of fights where fighter has the advantage
    result_list_b = []
    # get list of all fights where fighter has advantage
    for k in fighter_a_dict.keys():
        a_result = opponent_result_dict_a[k]
        b_result = opponent_result_dict_b[k]
        if a_result == -1 and b_result == 1:
            result_list_b.append(k)
        elif a_result == 1 and b_result == -1:
            result_list_a.append(k)
    final_result = len(result_list_a) - len(result_list_b)
    if final_result > 0:
        return (final_result, result_list_a)
    elif final_result < 0:
        return (final_result, result_list_b)


def find_opponent_result_dict(an_opponent_dict):
    """Returns an opponent dictionary where the values are -1 for all losses, 0 for mixed results, and 1 for all wins"""
    # TODO: Account for NC and non win or loss results.
    result_dict = {}
    for k in an_opponent_dict.keys():
        some_fights = an_opponent_dict[k]
        initial = some_fights[0][0]
        if initial == "Win":
            result = 1
        else:
            result = -1
        for f in some_fights:
            if f[0] != initial:
                result = 0
                break
        result_dict[k] = result
    return result_dict


def find_common_weight_class():
    """Return the weight classes in common for two fighters"""
    pass


def stylistic_advantage():
    """Return a ratio of stylistic advantage. Compare 2 fighter 8-tuples"""
    pass


def stylistic_advantage_description():
    """Return a description of a fighter's style"""


def print_test_common_opponent_advantage():
    print("TESTING COMMON OPPONENT ADVANTAGE")
    print("FIGHTER_A IS: " + fighterA)
    print("FIGHTER_B IS: " + fighterB)
    fighter_dict = build_fighter_object_dictionary()
    common_opponent_result = common_opponent_advantage(fighterA, fighterB, fighter_dict)
    if common_opponent_result[0] > 0:
        print(fighterA + " has the advantage")
        print("Num fights advantage: " + str(abs(common_opponent_result[0])))
        print("The fighters who " + fighterA + " has beat but " + fighterB + " lost to:")
        print(common_opponent_result[1])
    elif common_opponent_result[0] < 0:
        print(fighterB + " has the advantage")
        print("Num fights advantage: " + str(abs(common_opponent_result[0])))
        print("The fighters who " + fighterB + " has beat but " + fighterA + " lost to:")
        print(common_opponent_result[1])


def basic_and_common_opponent_odds(fighterA, fighterB, a_glicko_dict):
    basic_odds_result = find_basic_odds(fighterA, fighterB, a_glicko_dict)
    favorite = basic_odds_result[0]
    basic_odds = basic_odds_result[1]
    a_fighter_dict = build_fighter_object_dictionary()
    common_opponent_adv = common_opponent_advantage(fighterA, fighterB, a_fighter_dict)
    num_fight_advantage = abs(common_opponent_adv[0])

    indv_importance = .1
    importance_factor = indv_importance * num_fight_advantage
    new_odds = round(basic_odds * (1 + importance_factor),2)
    return (favorite, new_odds)


def print_test_basic_and_common_opponent_odds():
    print("TESTING BASIC + COMMON OPPONENT ODDS")
    print("FIGHTER_A IS: " + fighterA)
    print("FIGHTER_B IS: " + fighterB)
    a_glicko_dict = read_glicko_ranking("FOC_rankings_generator/FOC_glicko2.txt")
    result = basic_and_common_opponent_odds(fighterA, fighterB, a_glicko_dict)
    print("Favorite: " + result[0])
    print("Basic odds: " + str(find_basic_odds(fighterA, fighterB, a_glicko_dict)[1]))
    print("Basic odds + common opponent advantage: " + str(result[1]))


def main():
    print_test_common_opponent_advantage()
    print_test_basic_and_common_opponent_odds()


if __name__ == "__main__":
    main()
