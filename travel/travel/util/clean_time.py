import time


def cleantime(date_time):
    t = time.time()
    if date_time[-1] == 's':
        t -= int(date_time.replace('s', ''))
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time
    if date_time[-1] == 'm':
        t -= int(date_time.replace('m', '')) * 60
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time
    if date_time[-1] == 'h':
        t -= int(date_time.replace('h', '')) * 3600
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time
    if date_time[-1] == 'd':
        t -= int(date_time.replace('d', '')) * 3600 * 24
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time
    if date_time[-1] == 'w':
        t -= int(date_time.replace('w', '')) * 3600 * 24 * 7
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time
    if date_time[-1] == 'y':
        years = int(date_time.replace('y', ''))
        d = [2019 - x for x in range(years)]
        l = []
        for b in d:
            if (b % 100 != 0 and b % 4 == 0) or (b % 100 == 0 and b % 400 == 0):
                l.append(b)
        n = len(l)
        t -= ((years * 365) + n) * 3600 * 24
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
        return date_time

# cleantime('20y')

# t = time.time()
# yu = time.localtime(t)
# print(yu)
# t -= 600
# print(time.asctime(time.localtime(t)))

# d = [2019 - x for x in range(8)]
# print(d)
# b = 2012
# if (b % 100 != 0 and b % 4 == 0) or (b % 100 == 0 and b % 400 == 0):
#     print("%d这个年份是闰年" % b)
# # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)), t)
# import datetime
#
# date1 = '2011-08-25'
# date2 = '2019-08-25'
# # date1=time.strptime(date1,"%Y-%m-%d %H:%M:%S")
# # date2=time.strptime(date2,"%Y-%m-%d %H:%M:%S")
# date1 = time.strptime(date1, "%Y-%m-%d")
# date2 = time.strptime(date2, "%Y-%m-%d")
# # 根据上面需要计算日期还是日期时间，来确定需要几个数组段。下标0表示年，小标1表示月，依次类推...
# # date1=datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
# # date2=datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
# date1 = datetime.datetime(date1[0], date1[1], date1[2])
# date2 = datetime.datetime(date2[0], date2[1], date2[2])
# # 返回两个变量相差的值，就是相差天数
# print(date2 - date1)
# print(8 * 365)
