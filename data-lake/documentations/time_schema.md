# Time Table Proposal

One of the tasks of the Data Lake Implementation is to create a dashboard for Lysa Hale on Clipper Data set. We have prototyped a reporting tool for her in Google Data Studio, but the performance is poor due to excessive time consumed on querying from RedShift. There is a need for restructure the data base table structure to improve performance. One possible factor of poor performance when filtering generationtime on clipper transaction because generationtime is a datetime column. 
<br><br>

Take Lysa Hale's report for example, one of the items in the report is <b>Average Weekday Ridership</b>, the query of this item is:<br>

select avg(countperday) from<br>
(<br>
    select count(\*) as countperday,<br>
    extract(day from generationtime) as day,<br>
    extract(dow from generationtime) as dow<br>
    from sfofaretransaction<br>
    where<br>
        extract(month from convert_timezone('UTC','PST', generationtime)) = 10 and<br>
        extract(year from convert_timezone('UTC','PST', generationtime)) = 2018 and<br>
        (subtype = 1 or subtype = 2  or subtype = 4)<br>
    group by 2,3<br>
) where dow between 1 and 5;<br>

The query is complex and computationally expensive.<br><br>

One solution is to create a table to store all the date information, called "Date Table". The code to create the date table can be found [here](https://github.com/BayAreaMetro/eps-projects).
<br><br>
The Date Table consists of the following columns:<br>
1. Key links to transaction (Could be integer or string, but int preferred)
2. Date in standard written format (YYYY-MM-DD)
3. Year (int)
4. Month (int)
5. Month (varchar, English spelling of the Month)
6. Day (int)
7. Day of Week(int, Sunday = 0 and Saturday = 6)
8. Quarter (int)
9. Quarter-Year (varchar, like "2019-Q1")
10. Week of Year (int)
11. Week of Year-Year (varchar, like "2019-51")
12. isWeekday (Boolean)<br><br>
Optional:
13. Holiday(varchar, like "Thanksgiving Day")
14. Season(varchar, like "Summer")
<br>
** When joining the date table to an existing data set (like sfo_fare_transactions) a date key column will need to be created in table being joined to the Date Table in the format YYYY-MM-DD. Views can also be created of data sets joined with the Date Table. **
<br><br>
The Date table does not limited to be used for Clipper transaction table but also other tables like Fastrak transaction table. 
<br><br>
For example, when a dashboard is querying, it will join the transaction table and date table on the key and filter the condition on column(s) on date table so that the database is filtering out integer data entries instead of converting datetime object for every condition. 
<br>
Similarly a table to store all time information, "Time Table", is also needed.<br>

1. Key links to transaction (Could be integer or string, but int preferred)
2. Hour (int, 24-hour-format)
3. Minute (int)
4. isAfternoon(Boolean, dummy indicate AM or PM, 0 is AM, 1 is PM)
5. isMorningCommute (Boolean, like 5am - 10am)
6. isEveningCommute (Boolean, like 4pm - 8 pm)<br><br>
Optional:
7. isNight (Boolean, when transportation operates less frequent after Evening commute time)<br><br>

generationtime column in Clipper transaction table is in UTC time, but the time in Time Table time entries is based on local California time PST, and adjusted for day light saving adjustment. It is the best to convert the time to PST because all the data entries are gathered in California and we do not have to worry about time inconsistent.
<br><br>

Another advantage of having Date and Time schema is that if in the future we decide to add new columns related to date or time, such as isRushHour, we can create new columns in Date and Time schema without making any adjustment on the transaction tables.
