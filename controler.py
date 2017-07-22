import pymysql
import random
import time

from 一些项目.Processon.ProcessOn项目 import main


def controler_main():
    print('Processon controler主线程开始工作')

    print('查询数据库')
    connect=pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='1123',
        db='processon',
        charset="utf8"
    )
    cursor=connect.cursor()

    #查找数据库是否有executetime执行时间小于现在,且balance余额大于0的任务,若有则运行下面的代码
    now=int(time.time())
    if cursor.execute('SELECT * FROM tasklist WHERE executetime<{} and balance>0;'.format(now))>0:
        #将查找到的任务情况存入变量
        pending_execution_tasks=(cursor.fetchall())
        print('有需要执行的任务: 数量{}'.format(len(pending_execution_tasks)))
        #遍历所有任务,对每个任务执行1次
        for pending_execution_task in pending_execution_tasks:
            #
            id,usrname,inviteurl,balance,executetime=pending_execution_task
            #执行1次任务
            main(1,regurl=inviteurl,speed=(1,2))

            #执行完成则重写数据
            print('执行完成,记录数据!')
            random_new_time=now+random.randint(18000,86400)
            new_balance=balance-1

            cursor.execute('UPDATE tasklist SET executetime={} WHERE id={};'.format(random_new_time,id))
            cursor.execute('UPDATE tasklist SET balance={} WHERE id={};'.format(new_balance,id))

    connect.commit()
    cursor.close()
    connect.close()
    print('本轮执行完毕')


if __name__=='__main__':
    while True:
        controler_main()
        time.sleep(3600)