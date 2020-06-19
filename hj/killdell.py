
#!/usr/bin/evn python
#Author:Timbaland
#function:close rundll32.exe procece
''' navicat.exe
    rundll32.exe
'''
#create date:2020-04-08
#version:1.0
#update:2020-04-08
import  os,time
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd()
print(log_path)
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

def kill_rundll32(process_name):
        try:
                if isRunning(process_name):
                    result = os.system(f'taskkill /IM {process_name} /F')
                    logger.info(f'succes kill {process_name} {str(result)} ')
                else:
                    logger.info(f'{process_name} not succces)' )
        except Exception as e:
            print(e)


def net_disk():
    try:
        gustcmd = r""" net use Y: \\172.16.56.46\class1 "123456" /user:"ftp\student" """
        result = os.popen(gustcmd)
        print(result.read())
    except Exception as e:
        print('netdisk',e)

def isRunning(process_name) :
    try:
        process=len(os.popen('tasklist | findstr '+process_name).readlines())

        if process >=1 :
            logger.info(f'{process_name} is find')
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False


if __name__ == '__main__':
    N = 1
    while N <=120:
        N +=1
        print(N)
        logger.info(N)
        kill_rundll32('rundll32.exe')






































