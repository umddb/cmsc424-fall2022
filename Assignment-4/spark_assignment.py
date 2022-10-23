from pyspark import SparkContext
from functions import *
import re
import json

sc = SparkContext("local", "Simple App")
setDefaultAnswer(sc.parallelize([0]))

## Load data into RDDs
usersRDD = sc.textFile("datafiles/se_users.json").map(json.loads)
postsRDD = sc.textFile("datafiles/se_posts.json").map(json.loads)
playRDD = sc.textFile("datafiles/play.txt")
logsRDD = sc.textFile("datafiles/NASA_logs_sample.txt")
amazonInputRDD = sc.textFile("datafiles/amazon-ratings.txt")
nobelRDD = sc.textFile("datafiles/prize.json").map(json.loads)

## The following converts the amazonInputRDD into 2-tuples with integers
amazonBipartiteRDD = amazonInputRDD.map(lambda x: x.split(" ")).map(lambda x: (x[0], x[1])).distinct()


## Each of the tasks requires you to write one function
## The code below iterates through he
tasks = [
    (1, task1, postsRDD),
    (2, task2, postsRDD),
    (3, task3, postsRDD),
    (4, task4, (usersRDD, postsRDD)), # two inputs
    (5, task5, postsRDD),
    (6, task6, amazonInputRDD),
    (7, task7, amazonInputRDD),
    (8, task8, amazonInputRDD),
    (9, task9, logsRDD),
    (10, task10_flatmap, playRDD), # different format
    (11, task11, playRDD),
    (12, task12, nobelRDD),
    (13, task13, logsRDD), # different format
    (14, task14, logsRDD),
    (15, task15, amazonBipartiteRDD),
    (16, task16, nobelRDD),
]

for task in tasks:
     ## tasks where you have to write a function that takes in an RDD as input
     print("=========================== Task {}".format(task[0]))
     if task[0] in [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 15, 16]:
        r = task[1](task[2])
        for x in r.takeOrdered(50):
            print(x)

     ## tasks where you have to write a function that takes in two RDDs as input
     elif task[0] in [4]:
        r = task[1](task[2][0], task[2][1])
        for x in r.takeOrdered(50):
            print(x)

     ## tasks where you have to write a flatMap function
     elif task[0] in [10]:
        r = task[2].flatMap(task[1]).distinct()
        print(r.takeOrdered(50))

     ## special cases
     elif task[0] in [13]:
        r = task[1](task[2], ['01/Jul/1995', '02/Jul/1995'])
        for x in r.takeOrdered(50):
            print(x)
     elif task[0] in [14]:
        r = task[1](task[2], '01/Jul/1995', '02/Jul/1995')
        for x in r.takeOrdered(50):
            print(x)
