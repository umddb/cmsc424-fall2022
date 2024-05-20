queries = ["" for i in range(0, 25)]

### 0. List all the users who have at least 1000 UpVotes.
### Output columns and order: Id, Reputation, CreationDate, DisplayName
### Order by Id ascending
queries[0] = """
select Id, Reputation, CreationDate,  DisplayName
from users
where UpVotes >= 1000
order by Id asc;
"""

### 1. List the posts (Id, Title, Tags) for all posts that are tagged 'postgresql-9.4'
### Hint: use ``like'' -- note that tags are enclosed in '<>' in the Tags field.
### Output column order: Id, Title, Tags
### Order by Id ascending
queries[1] = """
select Id, Title, Tags
from Posts
where Tags like '%<postgresql-9.4>%'
order by Id asc;
"""


### 2. Write a query to output the number of years users have been on the
### platform (assuming they started on 'CreationDate') as of September 1, 2022
### Use 'age' function that operates on dates (https://www.postgresql.org/docs/12/functions-datetime.html)
### Restrict output to Users with DisplayName = 'Jason'
### Output columns: Id, DisplayName, Num_years
### Order output by Num_years increasing, and then by Id ascending
queries[2] = """
select Id, DisplayName, extract(year from age(timestamp '2022-09-01', CreationDate)) as Num_years
from Users 
where displayname = 'Jason'
order by Num_years asc, Id asc;
"""

### 3. Select all the "distinct" years that users with names starting with 'M'
### joined the platform (i.e., created their accounts).
### Output column: Year
### Order output by Year ascending
queries[3] = """
select distinct extract(year from CreationDate) as year 
from users
where displayname like 'M%'
order by year asc;
"""

### 4. Write a query to find users who have, on average, given at least 1 UpVote per
### day they have been on the platform as of September 1, 2022
### Hint: Use subtraction on "date" to get number of days between two dates.
### Count only full days (i.e., someone who joined 1.5 days ago only needs to
### have provided 1 UpVote to make it into the result)
### Output columns: DisplayName, CreationDate, UpVotes
### Order by Id ascending
queries[4] = """
select Id, DisplayName, CreationDate, UpVotes 
from Users
where date '2022-09-01' - CreationDate <= UpVotes
order by Id asc;
"""

### 5. Write a single query to report all Badges for the users with reputation between 10000 and 11000, by joining Users and Badges.
### Output Column: Id (from Users), DisplayName, Name (from Badges)
### Order by: Id increasing
queries[5] = """
select Users.Id, DisplayName, Name, Reputation
from Users, Badges
where Users.Id = Badges.UserId and Users.Reputation between 10000 and 11000
order by Users.Id asc;
"""

### 6. Write a query to find all Posts who satisfy one of the following conditions:
###        - the post title contains 'postgres' and the number of views is at least 50000
###        - the post title contains 'mongodb' and the number of views is at least 25000
### The match should be case insensitive
### Output columns: Id, Title, ViewCount
### Order by: Id ascending
queries[6] = """
select Id, Title, ViewCount
from posts
where (lower(title) like '%postgres%' and viewcount >= 50000) or 
      (lower(title) like '%mongodb%' and viewcount >= 25000)
order by Id asc;
"""


### 7. Count the number of the Comments made by the user with DisplayName 'JHFB'.
### Output columns: Num_Comments
queries[7] = """
select count(*) as Num_Comments
from users join comments on (users.id = comments.userid)
where users.displayname = 'JHFB';
"""

### 8. Find the Users who have received badges with names: "Guru" and "Curious". 
### Only report a user once even if they have received multiple badges with the above names.
### Hint: Use Intersect.
### Output columns: UserId
### Order by: UserId ascending
queries[8] = """
select userid from badges where name = 'Curious' 
intersect 
select userid from badges where name ='Guru';
"""

### 9. "Tags" field in Posts lists out the tags associated with the post in the format "<tag1><tag2>..<tagn>".
### Find the Posts with at least 6 tags, with one of the tags being postgresql (exact match).
### Hint: use "string_to_array" and "cardinality" functions.
### Output columns: Id, Title, Tags
queries[9] = """
select Id, Title, Tags
from Posts 
where cardinality(string_to_array(tags, '><')) >= 6 and lower(tags) like '%<postgresql>%';
"""


### 10. SQL "with" clause can be used to simplify queries. It essentially allows
### specifying temporary tables to be used during the rest of the query. See Section
### 3.8.6 (6th Edition) for some examples.
###
### Write a query to find the name(s) of the user(s) with the largest number of Comments. 
### We have provided a part of the query to build a temporary table.
###
### Output columns: Id, DisplayName, Num_Comments
### Order by Id ascending (there may be more than one answer)
queries[10] = """
with temp as (
        select Users.Id, DisplayName, count(*) as num_Comments 
        from users, comments 
        where users.id = comments.userid 
        group by users.id, users.displayname)
select id, displayname, num_comments
from temp 
where num_comments = (select max(num_comments) from temp)
order by Id;
"""



### 11. List the users who posted no comments and with at least 500 views. 
### Hint: Use "not in".
### Output Columns: Id, DisplayName
### Order by Id ascending
queries[11] = """
select Id, DisplayName
from users
where Views >= 500 and Id not in (
        select userid 
        from comments)
order by Id;
"""


### 12. Write a query to output a list of posts with comments, such that PostType = 'Moderator nomination' 
### and the comment has score of at least 10. So there may be multiple rows with the same post
### in the output.
### Output: Id (Posts), Title, Text (Comments)
### Order by: Id ascending
queries[12] = """
select p.id, p.title, c.text
from posts p, comments c, posttypes pt
where p.posttypeid = pt.posttypeid and pt.Description = 'Moderator nomination' and
    c.score >= 10 and c.postid = p.id
order by p.id asc;
"""


### 13. Generate a list - (Badge_Name, Num_Users) - containing the different
### badges, and the number of users who received those badges.
### Note: A user may receive the same badge multiple times -- they should only be counted once for that badge.
### Output columns: Badge_name, Num_users
### Order by Badge_name asc
### Use LIMIT to limit the output to first 20 rows.
queries[13] = """
select Badges.Name as Badge_name, count(distinct Users.Id) as Num_users
from badges, users
where badges.userid = users.id
group by badge_name
order by badge_name
limit 20;
"""

### 14. For each post, count the number of comments for that post.
###
### One way to do this is "Scalar" subqueries in the select clause.
### select Id,                             
### (select count(*) from comments where comments.postid = posts.id) as Num_comments
### from posts order by posts.id;
### 
### However, this takes too long, even on the relatively small database we
### have.
###
### Instead, use "left outer join" to do this task.
###
### Output Columns: Id, Num_Comments
### Order by: Id ascending
queries[14] = """
select posts.id, count(comments.postid) as Num_comments
from posts left outer join comments on (posts.id = comments.postid) 
group by posts.id 
order by posts.id;
"""


### 15. Generate a list - (Reputation, Num_Users) - containing the number
### of users with reputation between 1 and 100 (inclusive). If a particular reputation
### score does not have any users (e.g., 2), then that reputation should appear with a
### 0 count.
###
### HINT: Use "generate_series()" to create an inline table -- try 
### "select * from generate_series(1, 10) as g(n);" to see how it works.
### This is what's called a "set returning function", and the result can be used as a relation.
### See: https://www.postgresql.org/docs/12/functions-srf.html
###
### Output columns: Reputation, Num_users
### Order by Reputation
queries[15] = """
select n as Reputation, 
        (select count(*) from Users where reputation = n) as Num_users
from generate_series(1, 100) as g(n);
"""


### 16. Generalizing #14 above, associate posts with both the number of
### comments and the number of votes
### 
### As above, using scalar subqueries won't scale to the number of tuples.
### Instead use WITH and Left Outer Joins.
###
### Output Columns: Id, Num_Comments, Num_Votes
### Order by: Id ascending
queries[16] = """
with temp1 as (
    select posts.id, count(comments.postid) as Num_comments
    from posts left outer join comments on (posts.id = comments.postid) 
    group by posts.id 
),  temp2 as (
    select posts.id, count(votes.postid) as Num_Votes
    from posts left outer join votes on (posts.id = votes.postid) 
    group by posts.id 
)
select temp1.id, num_comments, num_votes
from temp1 join temp2 on temp1.id = temp2.id
order by temp1.id;
"""

### 17. Write a query to find the posts with at least 7 children (i.e., at
### least 7 other posts with that post as the parent
###
### Output columns: Id, Title
### Order by: Id ascending
queries[17] = """
select p1.ID, p1.Title
from posts p1, posts p2
where p1.id = p2.parentid
group by p1.id
having count(*) >= 7
order by id;
"""

### 18. Find posts such that, between the post and its children (i.e., answers
### to that post), there are a total of 100 or more votes
###
### HINT: Use "union all" to create an appropriate temp table using WITH
###
### Output columns: Id, Title
### Order by: Id ascending
queries[18] = """
with temp1 as (
select p1.id, p1.title, v.id as v_id
from posts p1, posts p2, votes v
where p1.id = p2.parentid and p2.id = v.postid
union all
select p1.id, p1.title, v.id as v_id
from posts p1, votes v
where p1.id = v.postid
) 
select id, title
from temp1
group by id, title
having count(v_id) >= 100;
"""

### 19. Write a query to find posts where the post and the accepted answer
### are both owned by the same user (i.e., have the same "OwnerUserId") and the
### user has not made any other post (outside of those two).
###
### Hint: Use "not exists" for the last one.
###
### Output columns: Id, Title
### Order by: Id Ascending
queries[19] = """
select p1.id, p1.title
from posts p1, posts p2
where p1.owneruserid = p2.owneruserid and p1.id = p2.parentid 
and not exists (select * from posts p3 where p3.owneruserid = p1.owneruserid 
        and p3.id not in (p1.id, p2.id))
order by p1.id;
"""

### 20. Write a query to generate a table: 
### (VoteTypeDescription, Day_of_Week, Num_Votes)
### where we count the number of votes corresponding to each combination
### of vote type and Day_of_Week (obtained by extract "dow" on CreationDate).
### So Day_of_Week will take values from 0 to 6 (Sunday to Saturday resp.)
###
### Don't worry if a particular combination of Description and Day of Week has 
### no votes -- there should be no row in the output for that combination.
###
### Output column order: VoteTypeDescription, Day_of_Week, Num_Votes
### Order by VoteTypeDescription asc, Day_of_Week asc
queries[20] = """
select Description as VoteTypeDescription, extract(dow from creationdate) as
Day_of_Week, count(*) as Num_Votes
from Votes, VoteTypes 
where votes.votetypeid = votetypes.votetypeid
group by Description, extract(dow from creationdate)
order by Description, Day_of_week;
"""
