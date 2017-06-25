# LogsAnalysis
Udacity/Full Stack Web Development/Project3

<Description>
logsanalysis.py is a python script, which outputs a text file from a database.
The database, caled newsdata.sql, contains three table: authors, articles and log.
The text file will include three data, which tells the most popular articles and authors and errors.

<How to implement>
1. Set up the Vagrant environment
2. Load the news database using the newsdata.sql file
3. execute your Python code with python3

<Note>
The SQL request are as follows:
#what are the most popular three articles of all time
select articles.title, count(*) as num
  from log, articles
  where log.status='200 OK'
  and substr(log.path, 10) = articles.slug
  group by articles.title
  order by num desc
  limit 3;

#Who are the most popular article authors of all time?
select authors.name, count(*) as num
  from log, articles, authors
  where log.status='200 OK'
  and substr(log.path, 10) = articles.slug
  and articles.author = authors.id
  group by authors.name
  order by num desc;

#On which days did more than 1% of requests lead to errors?
select to_char(_day, 'FMMonth FMDD, YYYY') as day, error from
    (select date_trunc('day', time) as _day,
    round(count(status='404 NOT FOUND' or null)*100.0/count(*), 2) as error
    from log
    group by _day
    having count(status='404 NOT FOUND' or null)*100.0/count(*) > 1) as result;
