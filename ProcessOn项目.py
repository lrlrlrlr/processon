import random
import requests
import time
from bs4 import BeautifulSoup


# url='https://www.processon.com/i/592a3d59e4b0265ca26fa549'


class Processon(object):
    headers={
        'Host':'www.processon.com',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Origin':'https://www.processon.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 '
                     'Safari/537.36',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'https://www.processon.com/signup',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8'}

    # headers={'Host': 'www.processon.com','Connection': 'keep-alive','Content-Length': '66','Cache-Control':
    # 'max-age=0','Origin': 'https://www.processon.com','Upgrade-Insecure-Requests': '1','User-Agent': 'Mozilla/5.0 (
    # Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
    # 'Content-Type': 'application/x-www-form-urlencoded','Accept': 'text/html,application/xhtml+xml,
    # application/xml;q=0.9,image/webp,*/*;','Referer': 'https://www.processon.com/signup','Accept-Encoding': 'gzip,
    # deflate, br','Accept-Language': 'zh-CN,zh;'}

    def sendreq(emailaddr,domain,regurl):
        make_jsessionid=requests.get(regurl).url.partition('=')[2]
        cookies={
            'JSESSIONID':make_jsessionid}
        data='email={}%40{}&pass={}&fullname={}'.format(emailaddr,domain,random.randint(100000000,99999999999),
                                                        emailaddr)
        r=requests.post('https://www.processon.com/signup/submit',headers=Processon.headers,cookies=cookies,data=data)
        print('构造注册请求:',BeautifulSoup(r.content,'lxml').p.text)

    def active(activeurl):
        r=requests.get(activeurl)
        print('激活:done',r)


class Tenminmail(object):
    get_cookies=requests.get('http://www.bccto.me').headers.get('Set-Cookie').split('\"')[1]
    assert type(get_cookies)==str


    headers={
        'Host':'www.bccto.me',
        'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0(WindowsNT 10.0;WOW64) AppleWebKit/537.36(KHTML,likeGecko) Chrome/57.0.2987.98 '
                     'Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;',
        'Referer':'http://www.bccto.me/',
        'Accept-Encoding':"gzip, deflate",
        'Accept-Language':"zh-CN,zh;q=0.8"}
    cookies={
        'mail':get_cookies}
    maillist=[]
    activeaddr=[]

    def applymail(usrname,domain):
        print('正在申请邮箱',usrname)
        r=requests.post('http://www.bccto.me/applymail',headers=Tenminmail.headers,cookies=Tenminmail.cookies,data={
            'mail':str(usrname)+'@'+str(domain)},timeout=5)
        print(r,r.content)

    def checkmail(mailaddr,domain):
        for i in range(10):
            if i==9:
                raise 'no mail..'
            time.sleep(10)
            print('检查邮箱..',end='')
            try:
                print(str(mailaddr)+'@'+str(domain))
                r=requests.post('http://www.bccto.me/getmail',headers=Tenminmail.headers,cookies=Tenminmail.cookies,
                                data={
                                    'mail':str(mailaddr)+'@'+str(domain)},timeout=5)
                if r.json()['mail'] is not None:
                    eml=r.json()['mail'][0][4]
                    print('有新邮件:',r.json())

                    try:
                        Tenminmail.gotactiveurl(mailaddr,domain,eml)
                        break
                    except:
                        pass
            except:
                pass

    def gotactiveurl(mailaddr,domain,eml):
        pos=domain.index(('.'))
        domain=transdomain(domain,pos)
        print(domain)
        url='http://www.bccto.me/win/'+str(mailaddr)+'(a)'+str(domain)+'/'+str(eml)
        r=requests.get(url,headers=Tenminmail.headers,cookies=Tenminmail.cookies)
        html=BeautifulSoup(r.content,'lxml')
        for i in html.find_all('a'):
            try:
                if 'signup/verification' in i.text:
                    new=i.text
                    if new not in Tenminmail.activeaddr:
                        print(new)
                        print('提取邮件内容:done(new)')
                        Processon.active(new)
                    else:
                        pass
            except:
                pass


def transdomain(domain,pos):
    transdomain=list(domain)
    transdomain[pos]='-_-'
    result=''.join(transdomain)
    return result


def randomname(length=(8,12)):
    def randomchar():#生成随机英文小写
        return chr(random.randint(97,122))

    def randomnum():
        return random.randint(0,9)

    name=''
    for i in range(random.randint(*length)):
        if random.randint(0,1)==0:
            name+=randomchar()
        else:
            name+=str(randomnum())
    return name


def randomain():
    domainlst=['11163.com','zhewei88.com','deiie.com','zv68.com','sohus.cn','zymuying.com','zhaoyuanedu.cn',
               'cuirushi.org','a7996.com','svip520.cn','hg0388.com','chaichuang.com','jy5201.com','ado0.cn',
               'xtianx.cn',
               'mail.sian.ml','mail.piaa.me','dayone.ren','mail.tianfamh.com']
    return domainlst[random.randint(0,len(domainlst))]


def main(succtimes_required,regurl='https://www.processon.com/i/5800a44be4b02e112242671e',speed=(1,10)):
    succtimes=0
    while succtimes<int(succtimes_required):
        time.sleep(2)
        print(succtimes,time.strftime('%m-%d %H:%M:%S'),'----start..-------------------------')
        try:
            random.seed(time.time())
            nowname=randomname()
            tempdomain=randomain()
            Tenminmail.applymail(nowname,tempdomain)
        except:
            print('applymail error')
        else:
            try:
                Processon.sendreq(nowname,tempdomain,regurl)
            except:
                print('sedreq error')
            else:
                try:
                    Tenminmail.checkmail(nowname,tempdomain)
                    for actaddr in Tenminmail.activeaddr:
                        Processon.active(actaddr)
                    succtimes+=1
                    randomsec=random.randint(*speed)#(7200,40000)
                    print('执行成功!现在休眠%s秒!'%randomsec)
                    time.sleep(randomsec)
                except:
                    print('check or active error!')

    pass


if __name__=='__main__':
    main(1,'https://www.processon.com/i/56593b61e4b010dc0fa2b62c')
    # emailaddr=input('email: \n')
    # Processon.sendreq(emailaddr,'zymuying.com','https://www.processon.com/i/56593b61e4b010dc0fa2b62c')
    # url=input('active url')
    # Processon.active(url)
    pass
