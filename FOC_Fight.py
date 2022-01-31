
class Fight(object):
    """Defines a Fight, which is contains the information about an MMA fight."""

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
        print("%s vs. %s" % (self.fighterA, self.fighterB))
        stat_string = "Result: %s %s by %s at %s of round %s on %s" % \
                (self.fighterA, self.result, self.method, self.time, self.round_finished, self.date)
        print(stat_string)
        print("==========================================================")

    def get_json(self):
        json_string = '{\n\t"fighterA":"%s",\n\t"fighterB":"%s",\n\t"result":"%s",\n\t"method":"%s",\n\t' \
                % (self.fighterA, self.fighterB, self.result, self.method)
        json_string += '"date":"%s",\n\t"roundFinished":"%s",\n\t"time":"%s"\n}' %\
                 (self.date, self.round_finished, self.time)
        return json_string


if __name__ == "__main__":
    pass


