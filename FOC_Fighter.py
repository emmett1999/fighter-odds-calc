from FOC_Fight import Fight


class Fighter(object):
    """Defines a Fighter object, which contains the basic fighter info, all their fights, and a dictionary of their
    detailed stats (like strikes landed per minute, takedown defense %) """

    def __init__(self, name, weight, division, fights, stats_dict):
        self.name = name
        self.weight = weight
        self.division = division
        self.fights = fights
        self.stats_dict = stats_dict

    def print_stats(self):
        print("-------------------------FIGHTER-------------------------")
        print("Name: " + self.name)
        print("Weight: " + self.weight)
        print("Division(s) fought in:")
        if type(self.division) == str:
            print("\t" + self.division + " division")
        else:
            for a_division in self.division:
                print("\t" + a_division + " division")

    def print_fights(self):
        print("-------------------------FIGHTS--------------------------")
        for a_fight in self.fights:
            if type(a_fight) == Fight:
                pass
                a_fight.print_stats()
            else:
                pass
                print("UNKNOWN_FIGHTS")

    def print_detailed_stats(self):
        print("----------------------DETAILED STATS----------------------")
        print("Strikes landed per minute: " + self.stats_dict['SLpM'])
        print("Striking accuracy %: " + self.stats_dict['StrAcc'])
        print("Strikes absorbed per minute: " + self.stats_dict['SApM'])
        print("Striking defense %: " + self.stats_dict['StrDef'])
        print("Takedown average per 15 minutes: " + self.stats_dict['TDAvg'])
        print("Takedown accuracy %: " + self.stats_dict['TDAcc'])
        print("Takedown defense %: " + self.stats_dict['TDDef'])
        print("Submissions attempted per 15 minutes: " + self.stats_dict['SubAvg'])

    def get_stats_tuple(self):
        self.stats_dict['StrAcc'] = self.stats_dict['StrAcc'][:-1]
        self.stats_dict['StrDef'] = self.stats_dict['StrDef'][:-1]
        self.stats_dict['TDAcc'] = self.stats_dict['TDAcc'][:-1]
        self.stats_dict['TDDef'] = self.stats_dict['TDDef'][:-1]
        return (self.stats_dict['SLpM'], self.stats_dict['StrAcc'], self.stats_dict['SApM'], self.stats_dict['StrDef'],
                self.stats_dict['TDAvg'], self.stats_dict['TDAcc'], self.stats_dict['TDDef'], self.stats_dict['SubAvg'])

    def get_json(self):
        json_string = '{\n\t"name":"%s",\n\t' % self.name
        weight_string = '"weight":"%s",\n\t' % self.weight
        json_string += weight_string
        if type(self.division) == list:
            json_string += '"division":['
            for i, a_division in enumerate(self.division):
                if i == len(self.division)-1:
                    division_string = '"%s"' % a_division
                    json_string += division_string
                else:
                    division_string = '"%s",' % a_division
                    json_string += division_string
            json_string += "]"
        else:
            division_string = '"division":"%s"' % self.division
            json_string += division_string
        json_string += '\n}'
        return json_string


if __name__ == "__main__":
    test_fightA = Fight("Doo-ho Choi", "Cub Swanson", "Loss", "Decision", "December 10, 2016", "Round 3", "5:00")
    test_fightB = Fight("Joe Rogan", "Wesley Snipes", "Win", "TKO", "June 12, 2003", "Round 2", "3:13")
    fight_list = [test_fightA, test_fightB]
    a_fighter = Fighter("Doo-ho Choi", "145", "Featherweight", fight_list)
    print(a_fighter.get_json())