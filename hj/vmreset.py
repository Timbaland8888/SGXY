#!/usr/bin/evn python
# -*- encoding:utf-8 -*-
# function: connect exsi server api  for restart vm
# date:2020-04-09
# Author:Timbaland
#version:1.1
#update:2020-04-10
_Arthur_ = 'Timbaland'
import pysphere, pymysql
from pysphere import VIServer
import logging
import ssl
import datetime, os, time
import configparser, codecs
import logging

# 全局取消证书验证,忽略连接VSPHERE时提示证书验证
ssl._create_default_https_context = ssl._create_unverified_context
class Info_log():
        def __init__(self,rq):
            self.rq = rq
        def log(self):
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            # rq = time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time()))
            log_name = self.rq + '.log'
            logfile = log_name
            fh = logging.FileHandler(logfile, mode='w',encoding='utf-8')
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            logger.addHandler(fh)
            logger.addHandler(ch)
            return logger


class VcentTools():

    def __init__(self, host_ip, user, password,flag):

        self.host_ip = host_ip
        self.user = user
        self.password = password
        self.flag = flag
    # 可以连接esxi主机，也可以连接vcenter

    def _connect(self):

        reserver_obj = VIServer()

    def esxi_version(self):

        m = Info_log(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        log = m.log()
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            servertype, version = server_obj.get_server_type(), server_obj.get_api_version()
            server_obj.disconnect()
            return servertype, version,self.flag
        except Exception as  e:
            server_obj.disconnect()

            log.info(e)

    def vm_status(self, vm_name):
        m = Info_log(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        log = m.log()
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
            # servertype, version = server_obj.get_server_type(),server_obj.get_api_version()


        except Exception as  e:
            server_obj.disconnect()
            log.info(e)

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
            if vm.is_powered_off() == False:
                server_obj.disconnect()
                return 1

            if vm.is_powered_off() == True:
                server_obj.disconnect()
                return 2

        except Exception as e:
            server_obj.disconnect()
            return 3

    def vmaction(self, vm_name, vm_hz):
        m = Info_log(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        log = m.log()
        server_obj = VIServer()
        try:
            server_obj.connect(self.host_ip, self.user, self.password)
        except Exception as  e:
            server_obj.disconnect()
            log.info(e)

        # 通过名称获取vm的实例
        try:
            vm = server_obj.get_vm_by_name(vm_name)
        except Exception as e:
            server_obj.disconnect()
            return 0
        if vm.is_powered_off() == False:
            try:
                vm.reset()
                # logger.info (type(int(vm_hz)))
                for i in range(1, int(vm_hz)):
                    log.info('虚拟机%s 正在重置中。。。。，请等待注册\n' % (vm_name))
                    time.sleep(1)
                log.info('重置完成')
                server_obj.disconnect()

                return 1
            except Exception as e:
                server_obj.disconnect()
                log.info(e)

        if vm.is_powered_off() == True:
            try:
                vm.power_on()
                log.info('虚拟机%s 正在开机中。。。。' % (vm_name))
                server_obj.disconnect()

            except Exception as e:
                server_obj.disconnect()
                return 2

class Class_VM():
    def __init__(self, host, user, pwd, port, db, charset):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.db = db
        self.charset = charset

    # 获取教室里面的虚拟机信息
    def get_vmname(self, query_sql):
        m = Info_log(time.strftime('%Y-%m-%d', time.localtime(time.time())))
        log = m.log()

        try:
            # 连接mysql数据库参数字段
            con = None
            db = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, port=self.port,
                                 charset=self.charset)
            cursor = db.cursor()
            vmlist = []
            cursor.execute(query_sql)
            result = cursor.fetchall()
            # 获取教室云桌面数量
            vm_count = len(result)
            log.info(f'教室云桌面虚拟机数量共{vm_count}台')

            # logger.info len(cursor.fetchall())
            # cursor.execute(query_vm)
            for vm_id in range(0, vm_count, 1):
                # logger.info result[vm_id][0]
                # logger.info result[vm_id][1]
                vmlist.append(result[vm_id][0])
                # logger.info result[vm_id][0]

            # logger.info type(cursor.fetchall()[0])

            db.commit()

        except ValueError:
            db.roolback
            super().logger.info('error')
        # 关闭游标和mysql数据库连接
        cursor.close()
        db.close()
        return vmlist

class SchdulerVM(VcentTools):
    def __init__(self,result,vm_counts):
        self.cf = result
        self.vm_counts = vm_counts

    def esxi_vm(self,vm_name,vm_hz):
        m = self.cf['vc']
        # for i in self.cf['vc']:
        # print(m['vc_ip'])
        # print(m['vc_acount'])
        # print(m['vc_pwd'])
        # print(m['flag'])
        super().__init__(m['vc_ip'],m['vc_acount'],m['vc_pwd'],m['flag'])
        super().vmaction(vm_name,vm_hz)

    def class_vmreset(self):
        for vm in self.vm_counts:
            print(vm)
            self.esxi_vm(vm,self.cf['vm_hz'])

if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    import yaml
    with open('config.yml', 'r', encoding='utf-8') as f:
        result = yaml.load(f.read(), Loader=yaml.Loader)
    cf = result['hj_db']
    # 查询教室虚拟机
    query_vm = ''' SELECT vm.vm_name
                    from hj_vm vm
                    INNER JOIN hj_dg dg on dg.id=vm.dg_id
                    WHERE vm.vm_name not like 'tempool%' 
               '''
    # 查询虚拟机信息
    p = Class_VM(cf['db_host'], cf['db_user'], cf['db_pwd'],
                 cf['db_port'], cf['db'], 'utf8')
    print(p.get_vmname(query_vm))
    vm_counts = p.get_vmname(query_vm)
    pd = SchdulerVM(result,vm_counts)

    # 获取当前时间
    now_date = datetime.datetime.now().strftime('%H:%M')
    #配置调度
    scheduler = BlockingScheduler()
    # pd.class_vmreset()
    scheduler.add_job(pd.class_vmreset,'cron',hour=21,minute=3)
    scheduler.start()
