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
        print("%s vs. %s" % (self.fighterA, self.fighterB))
        a_str = "Result: %s %s by %s at %s of round %s on %s" % \
                (self.fighterA, self.result, self.method, self.time, self.round_finished, self.date)
        print(a_str)
        print("==========================================================")

    def get_json(self):
        a_str = '{\n\t"fighterA":"%s",\n\t"fighterB":"%s",\n\t"result":"%s",\n\t"method":"%s",\n\t' \
                % (self.fighterA, self.fighterB, self.result, self.method)
        a_str += '"date":"%s",\n\t"roundFinished":"%s",\n\t"time":"%s"\n}' %\
                 (self.date, self.round_finished, self.time)
        return a_str


if __name__ == "__main__":
    print("Hello world")


