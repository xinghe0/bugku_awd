from queue import Queue
import threading
import busima

class WebshellSpaider(threading.Thread) :
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self) :
        while not self._queue.empty() :
            domain = self._queue.get()
            try:
                self.spider(domain)
            except Exception as e:
                pass

    def spider(self,domain):
        try:
            busima.all(domain)
        except Exception as e:
            print(domain + e)
            pass


def Webshell():
    queue = Queue(maxsize=5000)
    for i in range(0,256) :
        queue.put('http://192-168-1-%s.pvp1457.bugku.cn/' % i)

    thread = []
    thread_count = 50

    for i in range(thread_count):
        thread.append(WebshellSpaider(queue))
    for t in thread:
        t.start()
    for t in thread:
        t.join()

if __name__ == '__main__':
    Webshell()
