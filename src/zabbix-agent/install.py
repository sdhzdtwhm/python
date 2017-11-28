#!/usr/bin/python
# -*- coding: utf-8 -*-
# The Author is by yanghang
# This script is for centos zabbix_agent2.4.8 install

#导入所需模块
import socket
import fileinput
import os
import shutil

#定义变量
log_dir = '/mvtech/nm/logs/zabbix/logs/'
package6_name = 'zabbix-agent-2.4.8-1.el6.x86_64.rpm'
package7_name = 'zabbix-agent-2.4.8-1.el7.x86_64.rpm'
#zabbix server服务器IP
zabbix_server = '192.168.2.250'
agent_conf = 'zabbix_agentd.conf' 
#操作系统版本：请填写centos6或centos7
os_version = 'centos7'

#获取本机IP函数
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

#处理文本函数
def dofile(file_name,str01,str02):
	for line in fileinput.input(file_name,inplace=True):
		print line.replace(str01,str02).strip()

#主函数
if __name__=="__main__":
	if os_version == 'centos7':
		#获取本机IP
		host = get_host_ip()
		#修改配置文件的hostname(注：脚本执行后安装文件夹内的配置文件的hostname的IP会变化，请从一台机器分发安装脚本。)
		dofile(agent_conf,'192.168.10.40',host)
		#修改配置文件中的server
		dofile(agent_conf,'192.168.2.250',zabbix_server)
		#安装rpm包
		os.system('rpm -ivh --nodeps %s' % package7_name)
		#删除原配置文件
		os.system('rm -rf /etc/zabbix/zabbix_agentd.conf')
		#拷贝配置文件
		shutil.copyfile('zabbix_agentd.conf','/etc/zabbix/zabbix_agentd.conf')
		#创建agent日志文件夹
		os.system('mkdir -p %s' % log_dir)
		#配置用户、组合、日志目录所属
		os.system('groupadd zabbix')
		os.system('useradd -g zabbix zabbix')
		os.system('chown -R zabbix:zabbix %s' % log_dir)
		#启动服务&&开机自启动
		os.system("systemctl start zabbix-agent.service")
		os.system("systemctl enable zabbix-agent.service")
	elif os_version == 'centos6':
		#获取本机IP
		host = get_host_ip()
		#修改配置文件的hostname
		dofile(agent_conf,'192.168.10.40',host)
		#修改配置文件中的server
		dofile(agent_conf,'192.168.2.250',zabbix_server)
		#安装rpm包
		os.system('rpm -ivh --nodeps %s' % package6_name)
		#删除原配置文件
		os.system('rm -rf /etc/zabbix/zabbix_agentd.conf')
		#拷贝配置文件
		shutil.copyfile('zabbix_agentd.conf','/etc/zabbix/zabbix_agentd.conf')
		#创建agent日志文件夹
		os.system('mkdir -p %s' % log_dir)
		#配置用户、组合、日志目录所属
		os.system('groupadd zabbix')
		os.system('useradd -g zabbix zabbix')
		os.system('chown -R zabbix:zabbix %s' % log_dir)
		#启动服务&&开机自启动
		os.system("service zabbix-agent start")
		os.system("chkconfig zabbix-agent on")
	else:
		print('此脚本不支持安装此操作系统.')
