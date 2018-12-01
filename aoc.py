import collections


def d1():
    inp = "./input/1a.txt"
    init = 0

    def p1(inp, init):
        with open(inp, "r") as f:
            instructions = [int(i) for i in f.read().strip().split('\n')]
        freq_shift = init + sum(instructions)
        return freq_shift, instructions

    print("Day 1 Part 1 result: {}".format(p1(inp, init)[0]))

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

    print("Day 1 Part 2 result: {}".format(p2(inp, init)))


if __name__ == "__main__":
    d1()




