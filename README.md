# LogsAnalysis
Udacity/Full Stack Web Development/Project3

logsanalysis.py is a python script, which outputs a text file from a database.
The database contains three table: authors, articles and log.
The text file will contain three data, which tells the most popular articles and authors and errors.


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
select to_char(date_trunc('day', time), 'Mon DD, YYYY') as day,
    round(count(status='404 NOT FOUND' or null)*100.0/count(*), 2), '%') as error
    from log
    group by day
    having count(status='404 NOT FOUND' or null)*100.0/count(*) > 1;
