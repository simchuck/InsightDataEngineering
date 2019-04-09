Real Time Resource Dispatch
presentatation script - draft
2019.04.08


## Title / Introduction

[slide: Title]

Hello everyone.  My name is Charles Simchick and I am a Data Engineering Fellow with Insight.  

I built a data pipleline that ingests and processes data from multiple sources in real-time, and executes an algorithm to determine the optimum dispatch of jobs across those resources.  


## Motiviation & Business Value

[slide: Motivation]

My background is in Mechanical Engineering, with specific domain expertise in the management and analysis of data related to energy efficiency, and I have drawn on this background for inspiration in my project.  

Energy is a commodity that is traded much like the financial markets, although the price for that energy can vary widely for different geographic locations.  The main drivers for these variations are the weather and the population density.  Hot weather leads to increased energy required for cooling.  High population density creates very acute demand spikes during the busiest times of the workday.  The energy markets account for these variations and provide "real-time" pricing.  

[slide: Sample Data]

For my hypothetical use case, I would like you to imagine a business model in which there are an arbitrary number of data processing resources at geographically distributed locations.  You woperate a business which leverages these distributed computing resources to process jobs from a prioritized job queue.  

[slide: Data Transformations]

Using real-time data for each of the "resource nodes", we can determine the cost for use of that resource, along with the available capacity at that resource, and dispatch our job queue appropriately.  For now, we will optimize on the lowest total cost for processing.  


## Demonstration

[slide: Demonstration]
[live demo of application]

I am going to switch over now to demonstrate my application.  

This is the main user interface, which is built using Python and Dash.  On the left of the display is my prioritized job queue, which lists all of the jobs in my pipeline, along with some information on the "size" of the job and its relative priority.  The time-series plots in the middle of the screen track the real-time status of the relevant metrics for each available resource node -- the price per compute-hour, and the total available capacity at the node.  The output of the algorithm is on the right, in the form of an optimized dispatch queue.  Jobs from the job queue are assigned to different resource nodes based on the optimization algorithm and placed on this list.  

Data is ingested into a Kafka cluster, processed in real-time using the KSQL stream processing API, and then read from the Kafka topics for display on the user interface.  

Now I started the app a little bit before this presentation, and configured it to read real-time data from a couple of actual web APIs for a single location near XXX.  Since all of the elements for my hypothetical use case do not exist, I am simulating some of the input streams to generate the necessary data.  As you can see, the "real-time" data interval is relatively slow at about five minutes per record.  

In order to exercise the data pipeline and explore its limitations with regards to the rate of ingestion and processing, I have downloaded representative historical data into an AWS S3 bucket, and wrote a simulation engine in Python to ingest from these static sources at an arbitrarily faster rate, and publish to my Kafka topics.  

I am going to activate a few simulated resource nodes now, with a faster but still modest rate of about XXX events per second, to demonstrate the processing and dispatch.  

...

As you can see, the time series plot indicates the variation in the pricing and capacity at each resource node, and the dispatch queue is populated to take advantage of the lowest cost resource available at the time of processing.  


## Technology

[slide: Technology Stack]

My pipeline is currently hosted entirely on Amazon AWS.  I have an S3 bucket to which I downloaded the representative historical data used as a basis for the simulated data streams.  A single EC2 instance hosts all of my producer code, written in Python, to read records from the S3 bucket and make appropriate transformations for the simulation, before publishing to the corresponding Kafka topics.  

My Kafka cluster consists of four EC2 instances, with one master and three workers.  

A separate EC2 instances hosts the Confluent KSQL API, which provides an abstraction over the Kafka KStreams API to perform real-time stream processing using a declarative SQL-like syntax.  The simplicity of this interface, along with the close integration into Kafka, makes this a very attractive option for real-time processing.  

I have another EC2 instance that hosts my Python consumer scripts.  These read data from the Kafka topics and implement the job queue dispatch optimization algorithm to determine the appropriate resource nodes for each job.  

A final EC2 instance hosts my user interface, which uses the Dash package to provide a web interface with dynamic charting appropriate for display of the real-time processing pipeline.  

In addition to the data streams for each resource, node I am taking advantage of the Kafka architecture to publish both the job queue and dispatch queue into separate topics, which provides a convenient storage for accessing this information.  I am also using a Kafka topic to store "clickstream" data from the user interface input.  

You may have noticed that I do not have a separate database in my pipeline.  I had originally planned to use a Postgres database to store the structured time-series data.  But my use case does not require access to historical data, and the persistent nature of the Kafka topics provides all of the necessary storage for my application.  Eliminating a separate database reduces the overall complexity of the pipeline, and also avoids a potential bottleneck for transactions to and from the database.  

If some future case can be made for permanent storage of the data, it would be relatively trivial to implement the Kafka Connect API to directly transfer the data from the topics into the appropriate database.  This approach would appear to offer the most straightforward and efficient solution.  


## Challenges

[slide: Engineering Challenges]

There were a number of technical challenges in the course of this project, but two are most notable.

[slide: Challenge #1: KSQL Documentation and Operation]

First, KSQL is relatively new and immature technology.  The first release of the API was in December 2017, and the current version stands at 0.XXX.  While the Confluent website appears to have a lot of documentation, I found it to be somewhat obtuse and difficult to search effectively for answers to specific questions.  And discussions on Stack Overflow seem to suggest that this is difficulty is shared, with more questions and speculation than definitive answers.  

Through the course of my research, I was able to offer at least one solution to a shared problem (((deleting a KSQL stream after having first deleted the kafka topic registration))).  After completing my project, I intend to write a blog article discussing some of the difficulties I had, and to offer a straightforward "getting started" tutorial.  

[slide: Challenge #2: Coordination of Topic Streams]

The other major challenge I faced is around the coordination of timing for the different topic streams.  This issue manifests itself both in the separate streams associated with each particular resource node, and in the combination of data streams from different nodes during the dispatch optimization algorithm.  

Energy markets are time-sensitive -- the offered price at any time is only valid until the subsequent offer is made available, after which the previous offer is "expired".  These offers are typically made at regular intervals, but network communications and other factors could lead to more irregular ingestion of the data.  The processing of multiple streams needs to assure that it is using data which is valid with a certain time window.  Within any window, missing or duplicate events on any data stream will render the results incorrect and invalid.  The resource would not actually be available at the expected price.  

To solve this problem, I specified a time interval for each resource node based on the shortest update interval across all of its streams.  I should note that this I am using the "origination" time stamp when the record was actually created at the source, rather than the time of ingestion or processing in my pipeline.  The assigned timestamp for any processed results uses the most recent timestamp within that window.  This was a relatively naive algorithm, and there are probably further improvements that could be made.  


## Future Enhancements

[slide: Future Plans]

This project was conceived and implemented over the course of three weeks of intensive work, during which I was also gaining my first significant exposure to data engineering concepts in general, and to Kafka and its ecosystem more specifically.  so the time constraints required some quick decision-making that was not always fully informed, and there are probably many areas for improvement.  

Putting aside these questions, my roadmap for enhancing this project would include the following steps.  

First, I would like to look into moving most, if not all, of the processing logic into KSQL to take advantage of the efficiencies it offers.  

I would also like to implement the Connect API and an approriate database to provide an option for permanent storage of the data.  

There is also a possibility that the Connect API can be used for the original data ingestion from either the web APIs or the S3 data store, with any pre-processing logic for the simulation incorporated into a real-time KSQL stream.  

Finally, I would like to implement a "monitoring" topic to store data and metrics related to the operation of the data pipeline.  


## About Me

[slide: About Me]

That's the quick and dirty summary of my project, and I would be happy to discuss more of the details if you are interested.  

I would like you to also be interested in me, so I would like to share a little bit more about my interests.  

I will always consider myself first and foremost to be a Mechanical Engineer, and perhaps some of you may understand what I mean by this.  I have a lot of experience with project management and product development, and an affinity for filling the void whenever I find myself in a situation where effective leadership or management is not apparent.  

However I have many interests separate from my profession.  My dog consumes a substantial part of my daily live, and I enjoying getting out into nature as much as possible.  I am a member of a Japanese taiko drumming group, which provides an opportunity for both artistic expression and physical exertion.  I am a BJCP Master beer judge, and enjoy being able to make a critical analysis of the things I put into my body.  

Beyond this, I have what I might refer to as an addiction to understanding, and I have been pursuing self-directed education for as long as I can remember, and in whatever topic I find interesting at the time.  

I want to thank you again for your time, and I would be happy to answer any questions you might have.  
