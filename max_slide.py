import itertools
import operator

#####################################################################
# Problem Description:
#    Given a binary string s, calculate its maximum len of `slide`.
#    A `slide` is a string that can be divided into two parts, 
#    the first part of the string: count('1') > count('0')
#    the second part of the string: count('0') > count('1')
#####################################################################


def get_lens_of_segments(s):
    segments_lens = [0]
    prev_char = '0'
    for char in s:
        if char == prev_char:
            segments_lens[-1] += 1
        else:
            prev_char = char
            segments_lens.append(1)
    return segments_lens

def segments_lens_to_string(segments_lens, cut_idx):
    cycler = itertools.cycle('01')
    left = ''.join( itertools.imap(operator.mul, segments_lens[:cut_idx], cycler) )
    right = ''.join( itertools.imap(operator.mul, segments_lens[cut_idx:], cycler) )
    return left, right

def find_max_stretched(segments_lens):
    middle_part_ones = 0
    middle_part_zeros = 0
    for len_ones, len_zeros in zip(*[iter(segments_lens[1:-1])]*2):
        middle_part_ones += len_ones
        middle_part_zeros += len_zeros

    for idx in range(1, len(segments_lens)-1, 2):
        if idx == 1:
            left_part_remained_ones = segments_lens[1]
            right_part_remained_zeros = middle_part_zeros - middle_part_ones + segments_lens[1]
        else:
            left_part_remained_ones += segments_lens[idx]    # 1's
            left_part_remained_ones -= segments_lens[idx-1]  # 0's
            right_part_remained_zeros += segments_lens[idx]    # 1's
            right_part_remained_zeros -= segments_lens[idx-1]  # 0's

        left_streched_zeros = min(left_part_remained_ones-1, segments_lens[0])
        right_streched_ones = min(right_part_remained_zeros-1, segments_lens[-1])
        stretched_len = left_streched_zeros + right_streched_ones

        if idx == 1 or stretched_len > ans[0]:
            ans = (stretched_len, idx, left_streched_zeros, right_streched_ones)
    return ans[1:]

def calculate_special_slide_len(s):
    # s = (0*)(1*0*...)
    segments_lens = get_lens_of_segments(s)

    # s = (0+) | (0*)(1+) => no solution
    if len(segments_lens) <= 2:
        return None
    # segments_lens = [ len(0*), ..., len(1*) ]
    if len(segments_lens) % 2 == 1:
        segments_lens.append(0)
    """
    # s = (1+)...(0+) => s is the whole slide
    if segments_lens[0] == 0 and segments_lens[-1] == 0:
        zeros = s.count('0')
        ones = s.count('1')
        if ones >= zeros:
            return len(s), s[:-1], s[-1:]
        else:
            return len(s), s[:1], s[1:]
    """

    idx, max_left_zeros, max_right_ones = find_max_stretched(segments_lens)
    ans_segments_lens = [max_left_zeros] + segments_lens[1:-1] + [max_right_ones]
    left, right = segments_lens_to_string(ans_segments_lens, idx + 1)
    return len(left + right), left, right

######################################################################

def test(*testcases):
    for testcase in testcases:
        print "Q:", ( len(testcase), testcase )
        ans = calculate_special_slide_len(testcase)
        if ans:
            print "A:", ans, 
            print ans[1].count('1') > ans[1].count('0'),
            print ans[2].count('0') > ans[2].count('1')
        else:
            print "A: Can't be cut"
        print ''

def preset_test():
    testcases = [
        "", "0", "1", "01", "10", "00", "11",
        "010101", "101010", "10000", "0110101" ]
    test(*testcases)

import random
def random_test(prefix='', suffix=''):
    binary_str = []
    while True:
        digit = random.randint(0, 10)
        if digit == 10:  # P_stop_generating_string = 1/11
            binary_str = ''.join(binary_str)
            break
        else:
            binary_str.append(str(digit % 2))
    binary_str = prefix + binary_str + suffix

    test(binary_str)

######################################################################

if __name__ == '__main__':

    preset_test()

    test('00010000011111110000000001111111111')

    test('11111110111111111111')

    test('101111111111000001111111111')
    test('10111111111100000')
    test('101111111111000001')

    for _ in range(3):
        random_test()
    for _ in range(3):
        random_test(prefix = '0')
    for _ in range(3):
        random_test(suffix = '1')
    for _ in range(3):
        random_test(prefix = '0', suffix = '1')

