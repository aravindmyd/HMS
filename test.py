import datetime
data = '2020-05-27'.split('-')
print(data)
today = datetime.date.today()
someday = datetime.date(int(data[0]),int(data[1]),int(data[2]))
diff = someday - today
print(diff.days)