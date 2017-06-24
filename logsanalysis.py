import psycopg2

#SQL Requests
#what are the most popular three articles of all time
sql1 = """select articles.title, count(*) as num
    from log, articles
    where log.status='200 OK'
    and substr(log.path, 10) = articles.slug
    group by articles.title
    order by num desc
    limit 3;"""

#Who are the most popular article authors of all time?
sql2 = """select authors.name, count(*) as num
    from log, articles, authors
    where log.status='200 OK'
    and substr(log.path, 10) = articles.slug
    and articles.author = authors.id
    group by authors.name
    order by num desc;"""

#On which days did more than 1% of requests lead to errors?
sql3 = """select to_char(date_trunc('day', time), 'Mon DD, YYYY') as day,
    round(count(status='404 NOT FOUND' or null)*100.0/count(*), 2) as error
    from log
    group by day
    having count(status='404 NOT FOUND' or null)*100.0/count(*) > 1;"""

#Get data from database with sql requests
def get_data(sqlrequest):
  """Get data from database"""
  db = psycopg2.connect(database="news")
  c = db.cursor()
  c.execute(sqlrequest)
  data = c.fetchall()
  db.close()
  return data

#Title of the report
text = "Report\n\nMost popular articles\n"

#Make string from data with formatting
data1 = get_data(sql1)
for i in range(len(data1)):
    text = text + str(i+1) + ". \"" + data1[i][0] + "\" - " + str(data1[i][1]) + " views\n"

data2 = get_data(sql2)
text = text + "\nMost popular authors\n"
for i in range(len(data2)):
    text = text + str(i+1) + ". " + data2[i][0] + " - " + str(data2[i][1]) + " views\n"

data3 = get_data(sql3)
text = text + "\nErrors (1%+)\n"
for i in range(len(data3)):
    text = text + " " + data3[i][0] + " - " + str(data3[i][1]) + "%\n"

#Output to a report.txt file
f = open('report.txt', 'w')
f.write(text)
f.close()
