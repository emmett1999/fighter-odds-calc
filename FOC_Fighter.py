from FOC_Fight import Fight
import json

class Fighter(object):
    """docstring"""

    def __init__(self, name, weight, division, fights, stats_dict):
        """Constructor"""
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

    def get_json(self):
        a_str = '{\n\t"name":"%s",\n\t' % self.name
        some_str = '"weight":"%s",\n\t' % self.weight
        a_str += some_str
        if type(self.division) == list:
            a_str += '"division":['
            for i, a_division in enumerate(self.division):
                if i == len(self.division)-1:
                    some_str = '"%s"' % a_division
                    a_str += some_str
                else:
                    some_str = '"%s",' % a_division
                    a_str += some_str
            a_str += "]"
        else:
            some_str = '"division":"%s"' % self.division
            a_str += some_str
        a_str += '\n}'
        return a_str


if __name__ == "__main__":
    a_fight = Fight("Doo-ho Choi","Cub Swanson","Loss","Decision","December 10, 2016","Round 3","5:00")
    some_fight = Fight("Joe Rogan","Wesley Snipes","Win","TKO","June 12, 2003","Round 2","3:13")
    a_list = [a_fight, some_fight]
    a_fighter = Fighter("Doo-ho Choi","145","Featherweight",a_list)
    print(a_fighter.get_json())
    with open("FOC_collect_stats/FOC_basic_fighter_stats.json", "w") as handle:
        handle.write(a_fighter.get_json())
    with open("FOC_collect_stats/FOC_basic_fighter_stats.json", "r") as file:
        data = json.load(file)