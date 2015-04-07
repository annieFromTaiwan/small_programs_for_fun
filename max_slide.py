import sys

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

def lens_of_segments_to_string(segments_lens, cut_idx):
    slide_str_left = ''.join( [ '0'*zeros + '1'*ones for zeros, ones in zip(*[iter(segments_lens[:cut_idx])]*2) ] )
    slide_str_right = ''.join( [ '0'*zeros + '1'*ones for zeros, ones in zip(*[iter(segments_lens[cut_idx:])]*2) ] )
    return slide_str_left, slide_str_right

def calculate_special_slide_len(s):
    # s = (0*)(1*0*...)
    segments_lens = get_lens_of_segments(s)

    # s = (0+) | (0*)(1+) => no solution
    if len(segments_lens) <= 2:
        return (0, "can't be cut", "can't be cut")
    # segments_lens = [ len(0*), ..., len(1*) ]
    if len(segments_lens) % 2 == 1:
        segments_lens.append(0)
    # s = (1+)...(0+) => s is the whole slide
    if segments_lens[0] == 0 and segments_lens[-1] == 0:
        zeros = s.count('0')
        ones = s.count('1')
        #if ones >= zeros:
        #    left, right = lens_of_segments_to_string(segments_lens, 1)
        #else:
        #    left, right = lens_of_segments_to_string(segments_lens, -1)
        return len(s), "cut it yourself", "cut it yourself"

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

    segments_lens[0] = ans[2]
    segments_lens[-1] = ans[3]
    cut_idx = ans[1] + 1
    left, right = lens_of_segments_to_string(segments_lens, cut_idx)
    return len(left + right), left, right

######################################################################

def test(*testcases):
    for testcase in testcases:
        print "Q:", repr(testcase)
        ans = calculate_special_slide_len(testcase)
        print "A:", ans, 
        print ans[1].count('1') > ans[1].count('0'),
        print ans[2].count('0') > ans[2].count('1')
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
        if digit == 10:  # 1/11 to end
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

    test('10000')

    for _ in range(3):
        random_test()
    for _ in range(3):
        random_test('0')
    for _ in range(3):
        random_test('1')
    for _ in range(3):
        random_test('0', '1')

