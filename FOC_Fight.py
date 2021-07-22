import io, json

class Fight(object):
    """docstring"""

    def __init__(self, fighterA, fighterB, result, method, date, round_finished, time):
        """Constructor"""
        self.fighterA = fighterA
        self.fighterB = fighterB
        self.result = result
        self.method = method
        self.date = date
        self.round_finished = round_finished
        self.time = time


    def print_stats(self):
        print("--------------------------FIGHT--------------------------")
        print("%s vs. %s" % (self.fighterA, self.fighterB))
        a_str = "Result: %s %s by %s at %s of round %s on %s" % \
                (self.fighterA, self.result, self.method, self.time, self.round_finished, self.date)
        print(a_str)

    def get_json(self):
        a_str = '{\n\t"fighterA":"%s",\n\t"fighterB":"%s",\n\t"result":"%s",\n\t"method":"%s",\n\t' \
                % (self.fighterA, self.fighterB, self.result, self.method)
        a_str += '"date":"%s",\n\t"roundFinished":"%s",\n\t"time":"%s"\n}' %\
                 (self.date, self.round_finished, self.time)
        return a_str


if __name__ == "__main__":
    a_fight = Fight("Doo-ho Choi", "Cub Swanson", "Win", "Decision", "December 10, 2016", "Round 3", "5:00", )
    with open("FOC_fight_stats.json", "w") as handle:
        handle.write(a_fight.get_json())
    with open("FOC_fight_stats.json", "r") as file:
        data = json.load(file)
    assert(data["fighterA"] == a_fight.fighterA)
    assert(data["fighterB"] == a_fight.fighterB)
    assert(data["result"] == a_fight.result)
    assert(data["method"] == a_fight.method)
    assert(data["date"] == a_fight.date)
    assert(data["roundFinished"] == a_fight.round_finished)
    assert (data["time"] == a_fight.time)
    print("Done")


