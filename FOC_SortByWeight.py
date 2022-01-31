
class FOC_SortByWeight:

    def __init__(self, a_fighter_dict, a_glicko_dict):
        self.fighter_dict = a_fighter_dict
        self.glicko_dict = a_glicko_dict

    def query(self, weightclass_name):
        fighter_list = self.get_parsed_fighter_list()
        error_fighters = []
        for fighter in fighter_list:
            try:
                fighter.weight = int(str(fighter.weight)[:3])
            except ValueError:
                fighter_list.remove(fighter)
                error_fighters.append(fighter)
        if weightclass_name == "Flyweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if fighter.weight < 135]
        elif weightclass_name == "Bantamweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 135 <= fighter.weight < 145]
        elif weightclass_name == "Featherweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 145 <= fighter.weight < 155]
        elif weightclass_name == "Lightweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 155 <= fighter.weight < 170]
        elif weightclass_name == "Welterweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 170 <= fighter.weight < 185]
        elif weightclass_name == "Middleweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 185 <= fighter.weight < 205]
        elif weightclass_name == "Light heavyweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if 205 <= fighter.weight < 210]
        elif weightclass_name == "Heavyweight":
            fighters_in_weightclass = [fighter for fighter in fighter_list if fighter.weight > 210]
        else:
            print("ERROR: Invalid query")
        glicko_fighters = self.get_glicko_fighter_list(fighters_in_weightclass)
        sorted_fighters = self.sort_fighters_glicko2(glicko_fighters)
        return sorted_fighters

    def query_glicko(self):
        fighter_list = self.get_parsed_fighter_list()
        glicko_list = self.get_glicko_fighter_list(fighter_list)
        sorted_fighters = self.sort_fighters_glicko2(glicko_list)
        return sorted_fighters

    def get_parsed_fighter_list(self):
        fighter_list_keys = list(self.fighter_dict)
        fighter_list = [self.fighter_dict[key] for key in fighter_list_keys]
        fighter_list = [fighter for fighter in fighter_list if fighter.weight != "UNKNOWN_WEIGHT"]
        for fighter in fighter_list:
            if "(" in fighter.name:
                fighter.name = fighter.name[:fighter.name.find("(") - 1]
        return fighter_list

    def get_glicko_fighter_list(self, a_glicko_list):
        glicko_fighters = []
        for fighter in a_glicko_list:
            if fighter.name not in self.glicko_dict:
                glicko_fighters.append((1500, fighter))
            else:
                glicko_fighters.append((self.glicko_dict[fighter.name], fighter))
        return glicko_fighters

    def glicko2_sort_function(self, a_fighter):
        return a_fighter[0]

    def sort_fighters_glicko2(self, a_list):
        a_list.sort(reverse=True, key=self.glicko2_sort_function)
        return a_list


if __name__ == "__main__":
    pass

