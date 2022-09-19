import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse

from queries import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("host=127.0.0.1 dbname=stackexchange user=root password=root")
cur = conn.cursor()

cur.execute("drop table if exists postscopy;")
cur.execute("drop type if exists popularityscale;")
cur.execute("create table postscopy as (select * from posts);")
cur.execute("CREATE TYPE PopularityScale AS ENUM ('High', 'Medium', 'Low')");

cur.execute("drop trigger if exists UpdateMostFavoritedOnInsert on votes;")

cur.execute("drop table if exists MostFavoritedPosts;")
cur.execute("create table MostFavoritedPosts as select p.ID, p.Title, count(v.ID) as NumFavorites from posts p left join votes v on (p.id = v.postid and v.votetypeid = 5) group by p.id, p.title having count(v.ID) > 10;")
conn.commit()

input('Press enter to proceed')


test_queries_to_run = [None] * 100
test_queries_to_run[1] = ("SELECT * FROM postscopy where id < 100 order by id", 
                                "-- Result (should have appropriate new columns)") 
test_queries_to_run[2] = ("SELECT * FROM postscopy where id < 100 order by id", 
                                "-- Result (should have appropriate new columns)") 
test_queries_to_run[3] = ("select count(*) from postscopy where tags is null", 
                                    "-- Result (single tuple with a 0)")
test_queries_to_run[4] = ("select * from postscopy where id > 100000", 
                                "-- Result (new 10 tuples)")
test_queries_to_run[8] = ("select id, title, numcomments(id) from posts limit 100", 
                                "-- Result")
test_queries_to_run[9] = ("select userbadges(10)", "-- Result")
test_queries_to_run[10] = (
                'SELECT n.nspname as "Schema", p.proname as "Name", pg_catalog.pg_get_function_result(p.oid) as "Result data type" FROM pg_catalog.pg_proc p LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE p.proname = \'UpdateMostFavoritedOnInsert\'' ,
                "-- Result (should list the trigger function)")
for i in range(0, 13):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i in [5, 6, 7, 12]:
                ans = cur.fetchall()

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            elif i in [1, 2, 3, 4, 8, 9, 10]:
                conn.commit()
                print("--------- Running {} -------".format(test_queries_to_run[i][0]))
                cur.execute(test_queries_to_run[i][0])
                ans = cur.fetchall()
                print(test_queries_to_run[i][1])
                for t in ans:
                    print(t)
                print("")
            elif i in [7]:
                conn.commit()
                query_string = "insert into votes values(1000001,9306 , 5, -1, null, null)"
                cur.execute(query_string)
                conn.commit()
                query_string = "insert into votes values(1000002,590 , 5, -1, null, null)"
                cur.execute(query_string)
                conn.commit()
                query_string = "insert into votes values(1000002,590 , 5, -1, null, null)"
                cur.execute(query_string)
                conn.commit()
                query_string = "select * from MostFavoritedPosts"
                print("--------- Running {} -------".format(query_string))
                cur.execute(query_string)
                ans = cur.fetchall()
                print("-- Result (should list 9306 with 53 and 590 with 12)")
                for t in ans:
                    print(t)
                print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
