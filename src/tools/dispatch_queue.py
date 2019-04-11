# This code was extracted from `optimize_queue.py` on 2019.04.11 after initial commit
# It represents an earlier iteration which used a separate dispatch_queue, and an
# 'optimize' function to run the simulation.  There may still be some useful ideas
# in here that I would want to incorporate.

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


