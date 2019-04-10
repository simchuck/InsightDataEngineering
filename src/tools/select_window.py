#!/bin/python3
"""
Test the data windowing routine
"""

from collections import deque
import random

import argparse


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test job queue populator.')
    parser.add_argument('-s', '--size', help='Specify size of the data set.')
    parser.add_argument('-w', '--window', help='Specify number of elements to include in the window.')
    args = parser.parse_args()

    data_size = 10
    window_size = 5
    if args.size:
        data_size = int(args.size)
    if args.window:
        window_size = int(args.window)

    # Use the 'double-ended queue' to optimize stack operations for a rolling window in real-time.

    # Create some sample data for the test.
    ts_range = range(data_size)
    data_range = [round(random.gauss(75, 5), 2) for _ in ts_range]

    print('x,y data:')
    # Index the window across the dataset, starting at the beginning.
    for indx in range(data_size):
        X_window = deque(ts_range[:indx+1], maxlen=window_size)
        Y_window = deque(data_range[:indx+1], maxlen=window_size)
        print(list(zip(X_window, Y_window)))
        #print(select_window(window_size, ts_range[:indx], data_range[:indx]))

    print('DONE WITH INDEXED WINDOW')

    # Print each value pair in the window.
    ### DEBUG: Following lines work, but ugly.  Why can't I combine into a single operation:
    X, Y = (
        deque(ts_range, maxlen=window_size),
        deque(data_range, maxlen=window_size)
        )
    for x, y in zip(X, Y):
        print(x, y)

    print('DONE WITH WINDOW ITEMIZATION')
