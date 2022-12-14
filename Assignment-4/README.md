# Assignment 4: Apache Spark

The goal of this assignment is to learn how to do large-scale data analysis tasks using Apache Spark: for this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

### Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

The Docker image has been updated to include the spark distribution. But if you want to set it up manually: 

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 3.3.0, Pre-built for Hadoop 3.3 or later**.
2. Move the downloaded file to the `Assignment-4/` directory (so it is available in '/data/Assignment-4'), and uncompress it using: 
`tar zxvf spark-3.3.0-bin-hadoop3.tgz`
3. This will create a new directory: `spark-3.3.0-bin-hadoop3/`. 
4. Set the SPARKHOME variable: `export SPARKHOME=/data/Assignment-3/spark-3.3.0-bin-hadoop3/` (modify appropriately if it is downloaded somewhere else).

We are ready to use Spark. 

### Spark and Python

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. We will use Python here -- you can follow the instructions at the tutorial
and quick start (http://spark.apache.org/docs/latest/quick-start.html) for other languages. The Java equivalent code can be very verbose and hard to follow. The below
shows a way to use the Python interface through the standard Python shell.

### Jupyter Notebook

To use Spark within the Jupyter Notebook (and to play with the Notebook we have provided), you can do:
	```
	PYSPARK_PYTHON=/usr/bin/python3 PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook --allow-root --no-browser --ip=0.0.0.0 --port=8881" $SPARKHOME/bin/pyspark
	```
You need to make sure you are mapping the port 8881 for this to work.

### PySpark Shell

You can also use the PySpark Shell directly.

1. `$SPARKHOME/bin/pyspark`: This will start a Python shell (it will also output a bunch of stuff about what Spark is doing). The relevant variables are initialized in this python
shell, but otherwise it is just a standard Python shell.

2. `>>> textFile = sc.textFile("README.md")`: This creates a new RDD, called `textFile`, by reading data from a local file. The `sc.textFile` commands create an RDD
containing one entry per line in the file.

3. You can see some information about the RDD by doing `textFile.count()` or `textFile.first()`, or `textFile.take(5)` (which prints an array containing 5 items from the RDD).

4. We recommend you follow the rest of the commands in the quick start guide (http://spark.apache.org/docs/latest/quick-start.html). Here we will simply do the Word Count
application.

#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.

`>>> counts = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)`

Here is the same code without the use of `lambda` functions.

```
def split(line): 
    return line.split(" ")
def generateone(word): 
    return (word, 1)
def sum(a, b):
    return a + b

textfile.flatMap(split).map(generateone).reduceByKey(sum)
```

The `flatmap` splits each line into words, and the following `map` and `reduce` do the counting (we will discuss this in the class, but here is an excellent and detailed
description: [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code) (look for Walk-Through).

The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

### Running it as an Application

Instead of using a shell, you can also write your code as a python file, and *submit* that to the spark cluster. The `project5` directory contains a python file `wordcount.py`,
which runs the program in a local mode. To run the program, do:
`$SPARKHOME/bin/spark-submit wordcount.py`

### More...

We encourage you to look at the [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html) and play with the other RDD manipulation commands. 
You should also try out the Scala and Java interfaces.

### Assignment Details

We have provided a Python file: `spark_assignment.py`, that initializes the folllowing RDDs:
* An RDD consisting of tuples from Stackexchange "Users" table (`se_users.json`), each tuple as a dictionary
* An RDD consisting of tuples from Stackexchange "Posts" table (`se_posts.json`), each tuple as a dictionary
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of 2-tuples indicating user-product ratings from Amazon Dataset (`amazon-ratings.txt`)
* An RDD consisting of JSON documents pertaining to all the Noble Laureates over last few years (`prize.json`)

The file also contains some examples of operations on these RDDs. 

Your tasks are to fill out the 14 functions that are defined in the `functions.py` file (starting with `task`). The amount of code that you 
write would typically be small (several would be one-liners), with the exception of the last one. 

- **Task 1 (0.25)**: Use `filter` to find all posts where tags are not `null` (None in python) and that are tagged 'postgresql-9.4', and then a
`map` so that the output RDD has tuples of the form: (ID, Title, Tags). Note that postsRDD contains dictionaries -- see the contents
by running `postsRDD.take(10)`.

- **Task 2 (0.25)**: Use `flatMap` on the postsRDD to create an RDD (ID, Tag), listing all the tags for each post as a separate tuple. If a post has no tags, it should not appear in the output RDD.

- **Task 3 (0.25)**: The goal here is to find the 5 lexicographically smallest tags for each year, for the posts from that year. So the outputRDD should be contain tuples of the form: ('2001', ['tag1', 'tag2', ..., 'tag5']), with 'tag1' < 'tag2' and 'tag5' being smaller (lexicographically) than any other tag for a post from that year. All the five (or fewer for some of the years) tags should be distinct. Use a `map` followed by `reduceByKey` for doing this. 

- **Task 4 (0.25)**: Use `join` to join the usersRDD and postsRDD on `users.id = owneruserid`. The output should be a tuple of the form: (userid, displayname, postid, posttitle). You will need to do several `map`s to do this. Make sure you look at the structure of the objects with the RDD after the join; it will need to postprocessed using a `map` to get to the desired output.

- **Task 5 (0.25)**: Using the postsRDD, create an RDD where the key is a 2-tuple (title-word, tag), where the former is a word in a title, and the later is a tag.  The value associated with the key should be the number of posts in which the title-word is in the title, and the tag is in the tags for that post. This will require a couple of flatMaps (to separate `tags` into individual tag values as well as to separate the title into its words) and an aggregateByKey to count.

- **Task 6 (0.25)**: Write the function that takes as input the `amazonInputRDD` (which is an RDD of lines) and `maps` each line to a tuple while removing the initial descriptor, i.e., the first line "user1 product1 5.0" gets mapped to a tuple `(1, 1, 5.0)`.  This just requires a single `map`.

- **Task 7 (0.25)**: Complete the function that takes as input the `amazonInputRDD` and computes the
average rating for each user across all the products they reviewed. 
The output should be an RDD of 2-tuples of the form `(user1, 2.87)` (not the correct answer).
You can either use `aggregateByKey` or a `reduceByKey` followed by a `map`.

- **Task 8 (0.25)**: Complete the function that takes as input the `amazonInputRDD` and computes the
`mode` rating for each product across all users (i.e., the rating that was most common for that
product). If there are ties, pick the higher rating. Easiest way to do this would be a
`groupByKey` followed by a map to compute the `mode`.

- **Task 9 (0.25)**: For `logsRDD`, write a function that computes the number of log requests for each year. So the output should be an RDD with records of
teh form `(1995, 2952)` (not the correct answer). This can be done through a `map` to extract the years, followed by a group by aggregate.

- **Task 10 (0.25)**: Write just the flatmap function `task10_flatmap` that operates on `playRDD` -- for each line, it outputs the individual words sanitized
to remove any non-alphanumerical characters. So for the 3rd line, it would output a list: `[Enter, LEONATO, HERO, and, BEATRICE, with, a, Messenger]`.

- **Task 11 (0.25)**: This takes as input the playRDD and for each line, finds the first word in the line, and also counts the number of words. It should then filter the RDD by only selecting the lines where the count of words in the line is > 10. The output will be an RDD where the key is the first word in the line, and the value is a 2-tuple, the first being the line and the second being the number of words (which must be >10). Simplest way to do it is probably a `map` followed by a `filter`.

- **Task 12 (0.25)**: Write a sequence of transformations starting from prizeRDD that returns an PairRDD where the key is the `category` (`physics` etc), and the value is a list of all Nobel Laureates for that category (just their surnames). Make sure the final values are `list`s, and not some other class objects (if you do a `take(5)`, it should print out the lists).

- **Task 13 (0.25)**: This function operates on the `logsRDD`. It takes as input a list of *dates* and returns an RDD with "hosts" that were present in the log on all of those dates. The dates would be provided as strings, in the same format that they appear in the logs (e.g., '01/Jul/1995' and '02/Jul/1995').  The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html) Try to minimize the number of RDDs you end up creating. Note that the list of dates may contain more than 2 entries.

- **Task 14 (0.25)**: On the `logsRDD`, for two given days (provided as input analogous to Task 9 above), use a 'cogroup' to create the following RDD: the key of 
the RDD will be a host, and the value will be a 2-tuple, where the first element is a list of all URLs fetched from that host on the first day, and the second element
is the list of all URLs fetched from that host on the second day. Use `filter` to first create two RDDs from the input `logsRDD`.


- **Task 15 (0.25)**: Complete a function to calculate the degree distribution of user nodes in the Amazon graph (i.e., `amazonBipartiteRDD`). In other words, calculate the degree of each user node (i.e., number of products each user has rated), and then use a reduceByKey (or aggregateByKey) to find the number of nodes with a given degree. The output should be a PairRDD where the key is the degree, and the value is the number of nodes in the graph with that degree.

- **Task 16 (0.25)**: [Bigrams](http://en.wikipedia.org/wiki/Bigram) are sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task is to write a bigram counting application for counting the bigrams in the `motivation`s of the Nobel Prizes (i.e., the reason they were given the Nobel Prize). The return value should be a PairRDD where the key is a bigram, and the value is its count, i.e., in how many different `motivations` did it appear. Don't assume 'motivation' is always present.


### Sample results.txt File
You can use `spark-submit` to run the `spark_assignment.py` file, but it would be easier to develop with `pyspark` (by copying the commands over). 

**results.txt** shows the results of running `spark_assignment.py` on our code using: `$SPARKHOME/bin/spark-submit assignment.py`
