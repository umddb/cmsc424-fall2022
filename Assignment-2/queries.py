queries = ["" for i in range(0, 13)]

### 0. List all the users who have at least 1000 UpVotes.
### Output columns and order: Id, Reputation, CreationDate, DisplayName
### Order by Id ascending
queries[0] = """
select Id, Reputation, CreationDate,  DisplayName
from users
where UpVotes >= 1000
order by Id asc;
"""

### 1 [0.25]. Create a copy of the "Posts" table using the following command:
### select * into PostsCopy from Posts, OR
### create table PostsCopy as (select * from Posts)
###
### Also, use the following command to create a new "Type"
### CREATE TYPE PopularityScale AS ENUM ('High', 'Medium', 'Low');
###
### For the next few questions, we will use this duplicated table
###
### Write a single query/statement to add three new columns to the "PostsCopy" table -- 
### Age (integer), OwnerDisplayName (varchar(40)), and Popularity (of type PopularityScale).
### See: https://www.postgresql.org/docs/current/datatype-enum.html if you are
### unsure how to use the enum type
queries[1] = """
select 0;
"""

### 2 [0.5]. Write a single query/statement to set the values of the new columns. 
### Use "age()" function to find the age of the Post as of "September 1, 2022" in years. 
###
### The "Popularity" column should be set as follows:
### High: ViewCount >= 20000, Medium: ViewCount between 10000 and 20000, 
###         and Low: viewcount < 10000
### (There are no posts with viewcounts 10000 or 20000 so you don't need to worry about edge cases)
### Use CASE to write this part.
### You may have to do an explicit cast for the popularity attribute using '::popularityscale'
### 
### OwnerDisplayName should be obtained from the Users table
###
### https://www.postgresql.org/docs/current/sql-update.html has examples at the
### bottom to show how to update multiple columns in the same query
queries[2] = """
select 0;
"""


### 3 [0.25]. Write a query "delete" all Posts from PostsCopy where tags is null.
queries[3] = """
select 0;
"""

### 4 [0.5]. Use "generate_series" to write a single statement to insert 10 new tuples
### to 'PostsCopy' of the form:
### (ID = 100001, 1, 'Post 100001', CreationDate = '2022-10-01', Score = 0, OwnerUserId = -1, LastEditorUserId = -1)
### (ID = 100002, 1, 'Post 100002', CreationDate = '2022-10-02', Score = 0, OwnerUserId = -1, LastEditorUserId = -1)
### ...
### (ID = 100010, 1, 'Post 100010', CreationDate = '2022-10-10', Score = 0, OwnerUserId = -1, LastEditorUserId = -1)
###
### All other attributes should be set to NULL. 
###
### Note: The maximum id in posts is below 100000, so this shouldn't give any errors.
###
### HINT: Use concatenation operator: 'Post' || 0, and addition on dates to simplify.
### 
### Use `select * from postscopy where id > 100000;` to confirm.
queries[4] = """
select 0;
"""

### 5 [0.25]. Write a single query to rank the "Posts" by the number of votes, with the Post 
### with the highest number of votes getting rank 1. 
### If there are ties, the two (or more) votes should get the same "rank", and next ranks 
### should be skipped.
###
### HINT: Use a WITH clause to create a temporary table (temp(PostID, NumVotes) 
### followed by the appropriate "RANK"
### construct -- PostgreSQL has several different
### See: https://www.eversql.com/rank-vs-dense_rank-vs-row_number-in-postgresql/, for some
### examples.
### PostgreSQL documentation has a more succinct discussion: https://www.postgresql.org/docs/current/functions-window.html
###
### Output Columns: PostID, Rank
### Order by: Rank ascending, PostID ascending
queries[5] = """
select 0;
"""


### 6 [0.25]. Write a statement to create a new View with the signature:
### UsersSummary(Id, NumOwnerPosts, NumLastEditorPosts, NumBadges)
### 
### Use inline scalar subqueries in "select" clause to simplify this.
###
### This View can be used to more easily keep track of the stats for the users.
### NumOwnerPosts = the number of posts where OwnerUserId is that user's ID
### 
### Confirm that the view is created properly by running:
###      select * from UsersSummary limit 10;
###
### Note that: depending on exactly the query used, a "select * from
### UsersSummary" will likely be very very slow.
### However a query like: select * from UsersSummary where ID = 1000;
### should run very fast.
###
### Ensure that the latter is case (i.e., the query for a single ID runs quickly).
###
queries[6] = """
select 0;
"""

### 7 [0.5]. Use window functions to construct a query to associate with each user
### the average number of views for users that joined in the same year.
###
### See here for a tutorial on window functions: https://www.postgresql.org/docs/current/tutorial-window.html
###
### We have created a table using WITH for you: 
###         temp(ID, DisplayName, JoinedYear, Views)
### Our goal is to create a new table with columns: 
###      (ID, DisplayName, JoinedYear, Views, AvgViewsForUsersFromThatYear)
### Here: AvgViewsForUsersFromThatYear is basically the average number of views across
### all users who joined in that year
###
### This kind of an output table will allow us to compare each user with the other users 
### who joined in that same year (e.g., to understand whether popularity is correlated with how
### long the user has been on StackExchange)
### Order by: JoinedYear first, and then ID
###
### Note: We will be checking that you are using window functions.
###
### First few rows would look like this:
### id   |                   displayname                   | joinedyear | views | avgviewsforusersfromthatyear
### -------+-------------------------------------------------+------------+-------+------------------------------
### -1 | Community                                       |       2011 |   863 |          65.2201739850869925
### 2 | Geoff Dalgas                                    |       2011 |    64 |          65.2201739850869925
### 3 | balpha                                          |       2011 |    35 |          65.2201739850869925
### 4 | Nick Craver                                     |       2011 |    61 |          65.2201739850869925
### 5 | Emmett                                          |       2011 |    32 |          65.2201739850869925
### 
queries[7] = """
with temp as (
        select ID, displayName, extract(year from CreationDate) as JoinedYear, Views
        from users
        )
select *
from temp;
"""

### 8 [0.25]. Write a function that takes in the ID of a Post as input, and returns the
### number of comments for that user.
###
### Function signature: NumComments(in integer, out NumComments bigint)
###
### There are several examples here at the bottom: https://www.postgresql.org/docs/10/sql-createfunction.html
### You should be writing one that uses SQL, i.e., has "LANGUAGE SQL" at the end.
### 
### So calling NumComments(75780) should return 12. Make sure your function returns 0
### appropriately (for Posts who do not have any Comments).
### 
### Confirm that the query below works after the function is created:
###             select ID, Title, NumComments(ID) from Posts limit 100
### As for one of the questions above, trying to run this query without "limit" 
### will be very slow given the number of posts.
###
queries[8] = """
select 0;
"""

### 9 [0.5]. Write a function that takes in an Userid as input, and returns a JSON string with 
### the details of Badges of that user.
###
### So SQL query: select UserBadges(5);
### should return a single tuple with a single attribute of type string/varchar as:
###  { "userid": 10, 
###    "displayname": "Kim", 
###   "badges": [ {"name": "Autobiographer", "class": 3, "date": "2011-01-03"}, 
###                {"name": "Supporter", "class": 3, "date": "2011-02-25"}, 
###                {"name": " Teacher", "class": 3, "date": "2011-02-25"}, 
###                {"name": "Critic", "class": 3, "date": "2011-02-28"}
###    ]}
### 
###
### You should use PL/pgSQL for this purpose -- writing this purely in SQL is somewhat cumbersome.
### i.e., your function should have LANGUAGE plpgsql at the end.
###
### Function signature: UserBadges(in integer, out BadgesJSON varchar)
###
### HINT: Use "string_agg" aggregate functions for creating the list of badges properly: https://www.postgresqltutorial.com/postgresql-aggregate-functions/postgresql-string_agg-function/
### Use "FORMAT()" function for constructing the JSON strings -- you can also
### use CONCAT, but FORMAT is more readable: https://www.postgresql.org/docs/current/functions-string.html#FUNCTIONS-STRING-FORMAT
###
### BE CAREFUL WITH WHITE SPACES -- we will remove any spaces before comparing answers, but there is
### still a possibility that you fail comparisons because of that.
### 
### Confirm that: 'select userbadges(10);' returns the result above.
queries[9] = """
    select 0;
"""

### 10/11 [0.5]. Create a new table using:
###         create table MostFavoritedPosts as
###             select p.ID, p.Title, count(v.ID) as NumFavorites
###             from posts p left join votes v 
###                            on (p.id = v.postid and v.votetypeid = 5)
###             group by p.id, p.title
###             having count(v.ID) > 10;
###
### Note: `votetypeid = 5` is `Favorite`
###
### Create a new trigger that: 
###         When a tuple is inserted in the Votes relation, appropriately
### modifies MostFavoritedPosts.
###         Specifically:
###             If the PostId for the new Votes tuple is already present in MostFavoritedPosts, 
###                  then the NumFavorites should be increased appropriately.
###             If the PostID for the new Votes tuple is NOT present in MostFavoritedPosts, 
###                 then it should check whether the addition of the new Vote makes the Post
###                 a MostFavoritedPost, and add the entry to MostFavoritedPosts table if so.
###
###  As per PostgreSQL syntax, you have to write two different statements -- queries[10] should be the CREATE FUNCTION statement, 
###  and queries[11] should be the CREATE TRIGGER statement.
###
###  We have provided some partial syntax, commented out because it gives an error.
###
### You can find several examples of how to write triggers at: https://www.postgresql.org/docs/10/sql-createtrigger.html, and a full example here: https://www.tutorialspoint.com/postgresql/postgresql_triggers.htm
###
### The trigger should also be named: UpdateMostFavoritedOnInsert
queries[10] = """
select 0;
"""
### CREATE OR REPLACE FUNCTION UpdateMostFavoritedOnInsert()
###  RETURNS TRIGGER
###  LANGUAGE PLPGSQL
###  AS
###  $$
###  $$;

queries[11] = """
select 0;
"""

### 12 [0.25]. The goal here is to write a query to count the number of posts for each
### tag. However, tags are currently stored in the format "<mysql><version-control><schema>"
### 
### So write a query to first convert the "tags" strings into an array (make
### sure to account for the "<" and ">" characters appropriately), and then
### use "unnest" to create a temporary table with schema: 
### temp(tag, postid)
###
### Three functions to make this easier: left(), right(), and unnest()
### 
### Given this table, we can find the number of posts for each tag easily. 
### We have provided that part of the query already. 
queries[12] = """
with temp as (
     select 0 as tag, 0 as postid
) 
select tag, count(*) as NumPosts
from temp
group by tag
order by tag;
"""
