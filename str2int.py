import time

class StringToInt:

    @classmethod
    def split_sign(cls, string):
        if len(string) == 0:
            raise ValueError('Invalid input string: %s' % repr(string))
        if string[0] == '+':
            return +1, string[1:]
        elif string[0] == '-':
            return -1, string[1:]
        else:
            return +1, string


    @classmethod
    def to_int(cls, string):
        sign_digit, numerical_part = cls.split_sign(string)
        if len(numerical_part) == 0:
            raise ValueError('Invalid input string: %s' % repr(string))

        num = 0
        numerical_part = numerical_part.lstrip('0')
        for char in numerical_part:
            digit = ord(char) - ord('0')
            if digit < 0 or digit > 9:
                raise ValueError('Invalid input string: %s' % repr(string))
            else:
                num *= 10
                num += digit
        return num * sign_digit


    @staticmethod
    def self_correctness_test():
        test_cases = ['001234567898765432100', 
                      '0', '00000000000000000000',
                      '+1234', '+00001', '+00000',
                      '-4321', '-0999998', '-00000',
                      '-Azz0', '012a', '1.3',
                      '', '+', '-', 'X']

        print '----- Start of Correctness Test -----'
        for string in test_cases:
            try:
                print 'Q:', repr(string)
                print 'A:', repr(StringToInt.to_int(string)), '\n'
            except Exception as e:
                print e


    @staticmethod
    def self_speed_test():
        def timer_wrapper(func):
            def func_with_timer(*args, **kargs):
                t0 = time.time()
                result = func(*args, **kargs)
                time_spent = time.time() - t0
                return result, time_spent
            return func_with_timer

        int_with_timer = timer_wrapper(int)
        my_int_with_timer = timer_wrapper(StringToInt.to_int)

        print '-------- Start of Speed Test --------'
        string_len = 1000
        while True:
            test_string = '0' * string_len
            result, time_spent = int_with_timer(test_string)
            my_result, my_time_spent = my_int_with_timer(test_string)
            print 'string_len:', string_len
            print 'result the same:', result == my_result
            print 'time:', time_spent, '/', my_time_spent, '\n'
            if my_time_spent > 5:
                break
            if my_time_spent < 0.5:
                string_len *= 10
            else:
                string_len *= 2


if __name__ == '__main__':

    problem = '-00123400556600'
    answer = StringToInt.to_int(problem)
    print 'Simple Demo:', repr(problem), '->', repr(answer), '\n'

    StringToInt.self_correctness_test()
    StringToInt.self_speed_test()
