
import numpy as np
import datetime
from collections import Counter
from operator import itemgetter

def d1():

    def p1(inp, init):
        with open(inp, "r") as f:
            instructions = [int(i) for i in f.read().strip().split('\n')]
        freq_shift = init + sum(instructions)
        return freq_shift, instructions

    def find_first_repeat(l, l_next):
        for i in l_next:
            if l.count(i) > 1:
                return i

    def p2(inp, init):
        freq_history = [init]
        freq_next_segment = []
        freq_shift, instructions = p1(inp, init)
        for i in instructions:
            init += i
            freq_next_segment.append(init)
        freq_history += freq_next_segment

        while len(set(freq_history)) == len(freq_history):
            freq_next_segment = [i+freq_shift for i in freq_next_segment]
            freq_history = freq_history + freq_next_segment

        return find_first_repeat(freq_history, freq_next_segment)

    inp = "./input/1.txt"
    init = 0
    print("Day 1 Part 1 result: {}".format(p1(inp, init)[0]))
    print("Day 1 Part 2 result: {}".format(p2(inp, init)))


def d2():

    def letter2(d):
        if len([i for i in d.elements() if d[i] == 2]) > 0:
            return 1
        else:
            return 0

    def letter3(d):
        if len([i for i in d.elements() if d[i] == 3]) > 0:
            return 1
        else:
            return 0

    def p1(inp):
        with open(inp) as f:
            l = f.read().strip().split()
            l_counted = [Counter(i) for i in l]

            l_tuples = [(letter2(counter_obj), letter3(counter_obj)) for counter_obj in l_counted]
        return sum([i[0] for i in l_tuples])*sum([i[1] for i in l_tuples])

    def p2(inp):
        with open(inp) as f:
            l = f.read().strip().split()

            length = len(l[0])

            for i in range(length):
                newlist = []
                for j in l:
                    word = list(j)
                    del word[i]
                    newlist.append(''.join(word))

                if len(set(newlist)) < len(l):
                    return Counter(newlist).most_common(1)[0][0]

    inp = "./input/2.txt"
    print("Day 2 Part 1 result: {}".format(p1(inp)))
    print("Day 2 Part 2 result: {}".format(p2(inp)))


def d3():

    def get_covered_fabric(claims):
        fabric = np.array([[0]*1000]*1000)
        for claim in claims:
            x = claim[0][0]
            y = claim[0][1]
            w = claim[1][0]
            l = claim[1][1]
            fabric[x:x+w, y:y+l] += np.array([[1]*l]*w)
        return fabric

    def p1(inp):
        with open(inp) as f:
            claims_ = f.read().strip().split('\n')
            claims_ = [i.split('@ ')[1].split(': ') for i in claims_]
            claims = [(tuple([int(j) for j in i[0].split(',')]), tuple([int(j) for j in i[1].split('x')])) for i in claims_]

        fabric = get_covered_fabric(claims)
        fabric[fabric == 1] = 0
        fabric[fabric > 1] = 1
        return sum(sum(fabric))

    def p2(inp):
        with open(inp) as f:
            claims_ = f.read().strip().split('\n')
            claims_ = [i.split('@ ')[1].split(': ') for i in claims_]
            claims = [(tuple([int(j) for j in i[0].split(',')]), tuple([int(j) for j in i[1].split('x')])) for i in claims_]

        fabric = get_covered_fabric(claims)

        for i, claim in enumerate(claims):
            x = claim[0][0]
            y = claim[0][1]
            w = claim[1][0]
            l = claim[1][1]

            if sum(sum(fabric[x:x + w, y:y + l])) == w*l:
                return i+1

    inp = "./input/3.txt"
    print("Day 3 Part 1 result: {}".format(p1(inp)))
    print("Day 3 Part 2 result: {}".format(p2(inp)))


def d4():

    def get_sleep_sheet_guards(inp):
        with open(inp) as f:
            records = [i.lstrip('[').split('] ') for i in f.read().strip().split('\n')]
        records = [[datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M"), i[1]] for i in records]
        records = sorted(records, key=itemgetter(0))

        guards = []
        sleep_sheet = dict()

        for record in records:
            if record[1].split()[0] == 'Guard':
                guard = record[1].split()[1]
                if guard not in guards:
                    guards.append(guard)
                    sleep_sheet[guard] = dict()
            if record[1].split()[0] == 'falls':
                if record[0].hour != 0:
                    sleep_sheet[guard][record[0].date() + datetime.timedelta(days=1)] = np.array([1] * 60)
                else:
                    if record[0].date() in sleep_sheet[guard]:
                        sleep_sheet[guard][record[0].date()][record[0].minute:] = 1
                    else:
                        if not record[0].date() in sleep_sheet[guard]:
                            sleep_sheet[guard][record[0].date()] = np.array([0] * 60)
                        sleep_sheet[guard][record[0].date()][record[0].minute:] = 1


            elif record[1].split()[0] == 'wakes':

                if record[0].hour != 0:
                    sleep_sheet[guard][record[0].date() + datetime.timedelta(days=1)] = np.array([0] * 60)
                else:
                    if record[0].date() in sleep_sheet[guard]:
                        sleep_sheet[guard][record[0].date()][record[0].minute:] = 0
                    else:
                        sleep_sheet[guard][record[0].date()][record[0].minute:] = 0

        return sleep_sheet, guards

    def p1(inp):
        sleep_sheet, guards = get_sleep_sheet_guards(inp)

        tot_sleep = []
        for guard in guards:
            tot = 0
            for key in sleep_sheet[guard]:
                tot += sum(sleep_sheet[guard][key])
            tot_sleep.append(tot)

        guard_id_most_asleep = int(guards[tot_sleep.index(max(tot_sleep))][1:])

        total_slept_minutes = np.array([0]*60)
        for key in sleep_sheet['#'+str(guard_id_most_asleep)]:
            total_slept_minutes = np.add(total_slept_minutes, sleep_sheet['#'+str(guard_id_most_asleep)][key])

        most_slept_minute = list(total_slept_minutes).index(max(total_slept_minutes))

        return guard_id_most_asleep * most_slept_minute

    def p2(inp):
        sleep_sheet, guards = get_sleep_sheet_guards(inp)

        most_slept_matrix = []
        for guard in guards:
            tot = np.array([0]*60)
            for key in sleep_sheet[guard]:
                tot = np.add(tot, sleep_sheet[guard][key])

            most_slept_matrix.append(list(tot))
        most_slept_matrix = np.array(most_slept_matrix)

        ind = np.argmax(most_slept_matrix) // 60
        return int(guards[ind][1:]) * (np.argmax(most_slept_matrix) % 60)

    inp = "./input/4.txt"
    print("Day 4 Part 1 result: {}".format(p1(inp)))
    print("Day 4 Part 2 result: {}".format(p2(inp)))


def d5():

    def p1():
        pass

    def p2():
        pass

if __name__ == "__main__":
    d4()
