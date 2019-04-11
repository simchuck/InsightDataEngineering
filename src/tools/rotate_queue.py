#!/bin/python3
"""
Test the queue rotator function.
"""

from collections import deque
import random

import argparse


def rotate_queue(queue):
    """
    Returns the first item from a double-ended queue and returns the first item.

    Used to provide a continuous loop of values for a process.

    Input:
        queue       deque   a double-ended queue object

    Output:
        next_value  obj     the first item in the original deque
        queue       deque   the mutated deque object, rotated left by one position

    USES:
        from collections import deque
    """

    next_value = queue[0]
    queue.rotate(-1)

    return next_value


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test job queue populator.')
    parser.add_argument('-d', '--deque', help='Specify a deque object.')
    args = parser.parse_args()


    if args.deque:
        deque_object = deque(args.deque)
        print('deque object before function call: {0}'.format(deque_object))
        item = deque_object[0]
        deque_object.rotate(-1)
        print('deque object after function call: {0}'.format(deque_object))
        print(item)

