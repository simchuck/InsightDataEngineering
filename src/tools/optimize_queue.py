#!/bin/python3
"""
Test the job queue dispatch optimizer
"""

import argparse
from collections import deque, namedtuple
import random

import generate_job_queue


class Job():
    """
    Simple class for tracking processing jobs.

    Each job is characterized by a unique id, the priority level for completion,
    and a measure of the "size" of the job, in compute-hours (c.hr)

    Attributes:
        id          int     unique job id
        priority    int     priority, in discrete levels
        size        float   the "size" of the job, measured in "compute-hours"
    """

    def __init__(self, id, priority, size):
        self.id = id
        self.priority = priority
        self.size = size

        self.node = ''
        self.status = ''
        self.started = ''
        self.completed = ''

    def __repr__(self):
        message = 'Job: {0} | {1} | {2} | {3} | {4} | {5} | {6}'
        return message.format(
            self.id,
            self.priority,
            self.size,
            self.node,
            self.status,
            self.started,
            self.completed
            )


class Dispatch():
    """
    Simple class for tracking jobs on the dispatch queue.

    Each dispatch includes a unique dispatch id, along with the associated job
    for that dispatch.

    Attributes:
        id          int     unique resource id
        job         Job     instance of Job object with associated details
    """

    def __init__(self, id, job):
        self.id = id
        self.job = job

    def __repr__(self):
        return 'Dispatch: {0} | {1}'.format(self.id, self.job)


class ResourceNode():
    """
    Simple class for tracking attributes and status of the resource nodes.

    Attributes:
        id          int     unique resource id

    """

    ### TODO: provide appropriate attributes (and methods?) for this class
    ###       dispatch time
    ###       completion time (?)

    def __init__(self, id, price, capacity):
        self.id = id
        self.price = price
        self.capacity = capacity

    def __repr__(self):
        return 'Resource: {0} | ${1}/c.hr | {2} c.hr'.format(self.id, self.price, self.capacity)


def select_node(job, resource_nodes):
    """
    Select optimum resource node for processing the job.

    Assumes a single item of class Job, and a fully-populated resource_nodes
    list.  The appropriate node is determined by looking for the lowest price
    node that has sufficient capacity available to process the job.

    Inputs:
        job             Job                 job record to be assigned
        resource_nodes  list(ResourceNodes) list of resources with type 'ResourceNode'

    Returns:
        node            int                 resource node id
    """

    # Optimize for lowest price resource node
    for resource in sorted(resource_nodes, key=lambda node: node.price):

        # The resource node must have sufficient capacity to accept the job
        if job.size <= resource.capacity:
            job.node = resource.id
            break

    return job.node


def optimize_queue(job_queue, resource_nodes, dispatch_queue):
    """
    Dispatch jobs based on current attributes of the resource nodes.

    The job_queue is sorted, then eqch job evaluated in turn to find the optimum
    resource node to which it can be dispatched.

    For simulation purposes, a new job is added to the job_queue upon completion,
    to provide an unbounded input stream.

    Inputs:
        job_queue       deque(Job)          double-ended queue (deque) of type 'Job'
        resource_nodes  list(ResourceNodes) list of resources with type 'ResourceNode'
        dispatch_queue  deque(Dispatch)     double-ended queue (deque) of type 'Dispatch'

    Returns
        all input variables are mutated and returned as a tuple

    Uses:
        from collections import deque, namedtuple
    """

    while len(job_queue):

        job_queue = deque(sorted(job_queue, key=lambda job: job.priority))

        job = job_queue.popleft()                   # pull from the front of the queue

        print('Attempting to dispatch job {0} with size {1}'.format(job.id, job.size)) ### DEBUG:
        # Optimizing by lowest price resource node
        for resource in sorted(resource_nodes, key=lambda node: node.price):

            dispatched = False
            print('{0}'.format(resource))  ### DEBUG:

            # The resource node must have sufficient capacity to accept the job
            if job.size <= resource.capacity:
                try:
                    dispatch_queue.append(job)      # add to the end of the queue
                    resource.capacity -= job.size   # new job reduces capacity of the resource
                    resource.capacity = max(resource.capacity, 0)
                    dispatched = True
                except Exception as e:
                    message = 'ERROR: Could not append job {0} to resource {1}.'
                    print(message.format(job.id. resource.id))

        if not dispatched:
            message = 'Insufficient capacity for job {0}.  Returning to job queue.'
            print(message.format(job.id))
            job.priority += 1   ### DEBUG: reduce the priority -- this is a hack to avoid infinite loop when no changes in resource capacity
            job_queue.append(job)                   # append to back of the queue

            print('job size: ', job.size)
            for rn in resource_nodes:
                print(rn.id, rn.capacity)
            #job_queue.appendleft(job)              # append back to front of the queue

        else:
            # For continuous simulation, generate a new job for the queue
            #job_queue.extend(generate_job_queue(1))
            pass

    return job_queue, resource_nodes, dispatch_queue


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

    ## Job Queue is created using a namedtuple to hold basic details for each job.
    #Job = namedtuple('Job', 'id priority size')

    job_queue = deque([
        Job(id, random.randint(0, 5), int(random.gauss(10, 2)))
            for id in range(number_of_jobs)
        ])

    return job_queue


def main(number_of_resources, number_of_jobs):
    """
    Main routine for simulating changes to the job queue and resource nodes.
    """

    # Initialize the Resource Nodes
    resource_nodes = [
        ResourceNode(
            i,
            round(random.gauss(20, 4), 2),
            random.randint(50, 100)
            )
            for i in range(number_of_resources)
        ]

    # Initialize the Job Queue and Dispatch Queue
    job_queue = generate_job_queue(number_of_jobs)
    #dispatch_queue = deque()

    print('Starting dispatch optimizer simulation...')
    counter = 0

    pending_jobs = len([job for job in job_queue if hasattr(job, 'node')])

    while pending_jobs:

        job_queue = deque(sorted(job_queue, key=lambda job: job.priority))

        job = job_queue.popleft()

        # If the job is not yet dispatched, find the appropriate node
        if not job.node:
            job.node = select_node(job, resource_nodes)

            print('After select_node, job.node= ',job.node)     ### DEBUG:
            # The resource node must have sufficient capacity to accept the job
            if job.node:
                job.started = counter
                job.status = 'dispatched'
                resource_nodes[job.node].capacity -= job.size
                resource_nodes[job.node].capacity = max(resource_nodes[job.node].capacity, 0)
                print('Job {} dispatched to node {}'.format(job.id, job.node))  ### DEBUG:

            else:
                message = 'Insufficient capacity for job {0}.  Returning to job queue.'
                print(message.format(job.id))
                # Return the job to the queue
                job.priority += 1   ### DEBUG: reduce the priority -- this is a hack to avoid infinite loop when no changes in resource capacity
                job_queue.append(job)                   # append to back of the queue
                resource_nodes[job.node].capacity +- job.size

        counter += 1

        # Check for job completion and adjust the status attributes as appropriate
        if job.status == 'dispatched' and (job.started + job.size) < counter:
            job.completed = counter
            job.status = 'completed'
            resoure_nodes[job.node].capacity += job.size

        ### DEBUG: output for monitoring
        print('\n{0}: Resource Nodes ({1} nodes)'.format(counter, len(resource_nodes)))
        print('node\tprice\tcapacity')
        for node in resource_nodes:
            print('{}\t{}\t{}'.format(node.id, node.price, node.capacity))
        print('\n{0}: Job Queue ({1} jobs)'.format(counter, len(job_queue)))
        print('id\tpri\tsize\tnode\tstatus\tstart\tcomplete')
        for job in job_queue:
            print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(
                job.id,
                job.priority,
                job.size,
                job.node,
                job.status,
                job.started,
                job.completed
                ))
        ### DEBUG: seems to be re-appending to the job_queue, so queue continues to grow...
        ### DEBUG: and not adding dispatch information

#    while len(job_queue):
#
#        # Run the optimization algorithm to process jobs from the queue
#        for job in deque(sorted(job_queue, key=lambda job: job.priority)):
#            print('Attempting to dispatch {0}'.format(job))
#            job_queue, resource_nodes, dispatch_queue = optimize_queue(job_queue, resource_nodes, dispatch_queue)
#
#        print('After Optimization:')
#        print('Job Queue\tDispatch Queue:')
#        for j, d in zip(job_queue, dispatch_queue):
#            print('{0} \t {1}'.format(j, d))

        # Simulate changes to the job_queue and resource_nodes
        job_queue.extend(generate_job_queue(random.randint(0, 3)))
        for rn in resource_nodes:

            rn.price += round(random.gauss(0, 0.1), 2)
            rn.price = round(rn.price, 2)
            #rn.capacity += round(random.gauss(20, 5), 2)
            rn.capacity = max(round(random.gauss(100, 25), 2), 0)

    return


if __name__ == '__main__':

    # Parse command line arguments.
    parser = argparse.ArgumentParser(description='Test job queue populator.')
    parser.add_argument('-j', '--jobs', help='Specify number of jobs to generate.')
    parser.add_argument('-r', '--resources', help='Specify number of resource nodes to generate.')
    args = parser.parse_args()

    number_of_resources = 3         # default to 3 resource nodes for demo
    if args.resources:
        number_of_resoureces = int(args.resoureces)

    number_of_jobs = 10             # default initial number of jobs in the queue
    if args.jobs:
        number_of_jobs = int(args.jobs)

    main(number_of_resources, number_of_jobs)

