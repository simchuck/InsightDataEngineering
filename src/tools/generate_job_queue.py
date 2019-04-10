#!/bin/python3
"""
Test the job queue process generator
"""

from collections import namedtuple
import random

import argparse


def generate_job_queue(number_of_jobs=10):
    """
    Generates a list of jobs with randomized priority and size.

    The jobs are returned as a list of namedtuple objects, each with the
    associated job id, priority level, and size.

    Priorities are generated randomly in the range of 0 to 5.  The job size is
    generated using a Gaussian probability density function with a mean of 10
    and a standard deviation of 2.

    USES:
        from collections import namedtuple
        import random
    """

    # Job Queue is created using a namedtuple to hold basic details for each job.
    Job = namedtuple('Job', 'id priority size')

    job_queue = [
        Job(id, random.randint(0, 5), int(random.gauss(10, 2)))
            for id in range(number_of_jobs)
        ]

    return job_queue


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test job queue populator.')
    parser.add_argument('-n', '--number', help='Specify number of jobs to generate.')
    args = parser.parse_args()

    number_of_jobs = 10
    if args.number:
        number_of_jobs = int(args.number)

    print('Job Queue:')
    job_queue = generate_job_queue(number_of_jobs)
    for job in job_queue:
        print(job)
