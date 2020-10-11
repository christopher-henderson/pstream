from __future__ import division
from random import randrange

from pstream import Stream


def forever_random():
    while True:
        yield randrange(0, 99999)


def limiter(enumeration):
    """
    limit the iterator to either a maximum of 1000 numbers
    or bail early if we manage to get a number that is divisible
    by 100.
    """
    return enumeration.count <= 1000 or enumeration.element % 100 != 0


def fizz_buzzable(num):
    """
    We're only interested in valid fizz buzz numbers.
    """
    return num % 3 == 0 or num % 5 == 0


def fizz_buzz(num):
    num = num.element
    print("{}: {}{}".format(
        num,
        "Fizz" if num % 3 == 0 else "",
        "Buzz" if num % 5 == 0 else "",
    ))


def average(accumulator, enumeration):
    # Thanks math.stackexchange for the incremental averaging.
    #
    # https://math.stackexchange.com/a/106720
    return accumulator + ((enumeration.element - accumulator)/(enumeration.count+1))


# Generate random numbers for a game of FizzBuzz until we either
# have 1000 numbers or we find one that is divisible by 100 flat.
# Play the game and find the average of the numbers generated.
avg = Stream(forever_random()).\
    filter(fizz_buzzable).\
    enumerate().\
    take_while(limiter).\
    inspect(fizz_buzz).\
    reduce(0, average)

print("The average FizzBuzzer was {}".format(avg))
