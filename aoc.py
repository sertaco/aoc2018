from collections import Counter
import numpy as np


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
    def get_total_claim_size(claims):
        return sum([np.prod(i[1]) for i in claims])

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


if __name__ == "__main__":
    d3()



