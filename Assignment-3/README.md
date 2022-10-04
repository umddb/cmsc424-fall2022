# Assignment 3: SQL + Programming Languages

**This assignment is to be done by yourself, but you are welcome to discuss the assignment with others.**

## Setup 
You can use the same setup as for Assignment 1 for this assignment. The only additional thing we will use here is Java and a couple of other packages, which are installed in the latest image.

## SQL and Java (1.5 point)
One of more prominent ways to use a database system is using an external client, using APIs such as ODBC and JDBC, or proprietary protocols.
This allows you to run queries against the database and access the results from within say a Java or a Python program.

For this part, you have to write/complete a Java program that accesses the database using JDBC, does some computations that are better done in a
programming langauge, and writes back the result to the database.

Here are some useful links:
- [Wikipedia Article](http://en.wikipedia.org/wiki/Java_Database_Connectivity)
- [Another resource](http://www.mkyong.com/java/how-do-connect-to-postgresql-with-jdbc-driver-java/)
- [PostgreSQL JDBC](http://jdbc.postgresql.org/index.html)

The last link has detailed examples in the `documentation` section. The `Assignment-3` directory (in the git repository) also contains an example 
file (`JDBCExample.java`). To run the JDBCExample.java file, do: 
`javac JDBCExample.java` followed by `java -classpath .:./postgresql-42.2.10.jar JDBCExample` (the `jar` file is in the `Assignment-3` directory).


Our goal is to find, for each user, its `nearest neighbor` based on the tags of the posts that they have made (defined more formally below). We will ignore posts where `OwnerUserId` is Null.

The simple algorithm we have listed below wouldn't work for the number of users we have, so we will only focus on the first 1000 users.
Here are the main steps:

1. Execute an SQL statement to add a new column to the `users` table called `most_similar_users`. This should be an `Array` column (i.e., `integer[]`).
1. Use the following query to fetch relevant data from the database: 
```
select users.id, array_remove(array_agg(posts.tags), null) 
from users, posts 
where users.id = posts.OwnerUserId and users.id < 5000 
group by users.id
```
This will give us, for each user, an array of `tags` strings (which themselves are lists).
1. Parse and separate out the tags for each user, so that, for each userid, we get a set of tags (use Java HashSet to store these).
1. For each user, say ID = A, go through the rest of the users and find the user with the highest `Jaccard Similarity Coefficient` based on the tag sets for the two users.
    1. Given two sets of tags, S1 and S2, the Jaccard Similarly is computed as: (size of the intersection of S1 and S2)/(size of the union of S1 and S2)
    1. We have provided you with a function (`jaccard`) that takes in two HashSets of Strings and return the Jaccard Coefficient.
1. If there is a tie (say B and C both have the same Jaccard Similarity with A), you should use the user with the lowest ID (i.e., use B if B < C).
1. Write out the id of the closest user computed above to the `most_similar_user` column for A.
1. Make sure to commit after you are done.

First rows of `select * from users order by id limit 5` afterwards look like:
```
userid  |        name         | birthdate  |   joined   |     lcc
---------+---------------------+------------+------------+-------------
user0   | Anthony Roberts     | 1998-10-20 | 2007-02-04 |  0.21904762
user1   | Anthony Taylor      | 1967-02-09 | 2014-08-19 |  0.24242425
```

We have provided a skeleton code to get you started. As above, the code will be run using: `javac NearestNeighbor.java` followed by `java -classpath
.:./postgresql-42.2.10.jar NearestNeighbor`, and should result in a modified `users` table as described above.

Some resources:
- https://docs.oracle.com/javase/tutorial/jdbc/basics/array.html discusses how to retrieve and operate upons Arrays using JDBC.

## SQL and Python (1.5 point)
This project is similar to the above, in that you are being asked to write (complete) a Python program that accesses the database using `psycopg2` -- unlike
the above case, `psycopg2` uses a proprietary protocol, not JDBC or ODBC.

Specifically, we have provided a partial program that implements a Web API to execute update/delete/retrieval operations against our `stackexchange` database. This API
is built using the Python `Flask` library, and couple of other packages built on top of it. 
- You will need to install three more Python modules using `pip3 install requests flask flask-restful flask_cors` (we have updated the Docker image to do this)
- If you are using Docker, when running docker, make sure to map the port 5000 (that's the default port for Flask).
- Ensure that PostgreSQL is running in the container.
- Now, in the Assignment-3 directory, you can start the Flask server by doing: `python3 rest.py`
- This should get the Flask server running, and listening on port 5000.
- In your web browser, go to: `http://127.0.0.1:5000/users/10' -- you should see the JSON response from the web server with the basic information for user 10 in the database.
    - If the web server is successfully up but this doesn't work, it's likely a problem with port mapping
- Your task is implement three other, user-specific endpoints:
    - `GET /posts/<postid>/`: Given a specific postid, this should return a JSON with the details about the post as listed in `rest.py`
        - Don't worry about the case where the post is not found in the database
    - `DELETE /user/<userid>`: Given a specific userid, this should delete the user from the backend database
        - You cannot run this from the Web browser easily, instead, the simplest way is to...
        - Use `curl`: Try `curl -X DELETE http://127.0.0.1:5000/user/user10sk3` -- it should return a default message
    - `POST /user/<userid>`: Given the information in the POST payload, this should create a new user with the specific userid
        - As above, you cannot easily run this from the web browser
        - Instead, try: `curl -X POST -d "birthdate=xyz" -d "joined=xyz" -d 'name=linuxize' 127.0.0.1:5000/user/user1`
        - We have already provided code for parsing the POST payload -- in the server output, you should see the parsed values to be inserted
- In addition, you need to implement one "Analytics Dashboard" endpoint that returns the top 100 users by reputation 
    - `GET /dashboard/top100users`: should return a JSON with a ranked list of top 100 users by reputation, using the standard PostgreSQL RANK function
- For more details, see the `rest.py` file -- it includes specific locations where you have to make the changes as well as discusses the error conditions that need to be
handled.

## Metadata Operations with JDBC (1 point)
JDBC also allows inspection of the schema, which can be a powerful feature to explore new databases (or datasets). Here, your task is to use that functionality to create a short summary of the tables in a database and the possible joins between the tables of the database based on the `foreign keys`.

Specifically, you should use the `getMetaData()` function to obtain `DatabaseMetaData` object, and use that fetch information about the tables in the database as well as information about the primary keys and foreign keys. 

This resource here has detailed examples of how to use this functionality: https://www.baeldung.com/jdbc-database-metadata

We have provided a skeleton file, `MetaData.java` -- your task is to complete the function within.

For the expected output format, see the files `exampleOutputMetadataStackexchange.txt` and `exampleOutputMetadataUniversity.txt`, which should be the output of running the program on our `stackexchange` and `university` databases. The overall order of tables and joinable relationships doesn't matter -- however, the lists of attributes (for a table and for a primary key) should be sorted in the increasing order (use `Collections.sort()`).

Notes/Hints:
1. Use `.toUpperCase()` to convert table/attribute names to uppper case.
1. We have provided a function to map the integer `type` that JDBC uses to a String, that you can use when printing out the data type of a column.
1. Use `Collections.sot()` to sort the attribute lists.


### Submission
Upload the three files `NearestNeighbor.java`, `rest.py`, and `MetaData.java` as separate files to Gradescope.
