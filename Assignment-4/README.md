# Assignment 4: Apache Spark

The goal of this assignment is to learn how to do large-scale data analysis tasks using Apache Spark: for this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

### Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

The Docker image has been updated to include the spark distribution. But if you want to set it up manually: 

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 3.2.0, Pre-built for Hadoop 3.3 or later**.
2. Move the downloaded file to the `Assignment-4/` directory (so it is available in '/data/Assignment-4'), and uncompress it using: 
`tar zxvf spark-3.3.0-bin-hadoop3.tgz`
3. This will create a new directory: `spark-3.3.0-bin-hadoop3/`. 
4. Set the SPARKHOME variable: `export SPARKHOME=/data/Assignment-3/spark-3.2.0-bin-hadoop3.2/` (modify appropriately if it is downloaded somewhere else).

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

To be posted soon.
