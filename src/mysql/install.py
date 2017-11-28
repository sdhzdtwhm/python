#coding=utf-8
#!/usr/bin/python
import os,commands
#适用于centos编译安装mysql5.6.36 需要配置yum
#定义变量

install_dir = '/data/mysql'
data_dir = '/data/mysql/data'
package_dir = '/data/mysql'
log_dir = '/data/mysql/logs'
current_dir = os.getcwd()
cmake = 'cmake -DCMAKE_INSTALL_PREFIX=%s -DMYSQL_UNIX_ADDR=%s/mysql.sock -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DMYSQL_DATADIR=%s -DMYSQL_TCP_PORT=3306' % (install_dir, install_dir, data_dir)


#安装依赖包
os.system('yum install gcc gcc-c++ gcc-g77 autoconf automake zlib* fiex* libxml* ncurses-devel libmcrypt* libtool-ltdl-devel* make cmake perl -y')
#安装函数
def install_mysql():
    if os.system('groupadd mysql') == 0:
        print 'group mysql add success!'
    else:
        exit('group mysql add failed!')
    if os.system('useradd -r -g mysql -s /bin/false mysql') == 0:
        print 'user mysql add success!'
    else:
        exit('user mysql add failed!')

    if not os.path.exists(install_dir):
        os.system('mkdir -p %s' % install_dir)
    if not os.path.exists(data_dir):
        os.system('mkdir -p %s' % data_dir)
    if not os.path.exists(package_dir):
        os.system('mkdir -p %s' % package_dir)
    if not os.path.exists(log_dir):
        os.system('mkdir -p %s' % log_dir)

    if os.system('tar zxvf mysql-5.6.36.tar.gz') == 0:
        print 'uncompress v success!'
    else:
        exit('uncompress mysql-5.6.36.tar.gz failed!')
    os.chdir('mysql-5.6.36')
    if os.system(cmake) == 0:
        print '编译成功'
    else:
        exit('编译mysql失败')
    if os.system('make && make install') == 0:
        print '编译安装mysql成功'
    else:
        exit('编译安装mysql失败')

    if os.system('chown -R mysql:mysql %s' % install_dir) == 0:
        print '安装目录权限配置成功'
    else:
        exit()
    os.system('chown -R mysql:mysql %s' % data_dir)
    os.system('chown -R mysql:mysql %s' % log_dir)
    os.chdir(install_dir)

    if os.system('./scripts/mysql_install_db --user=mysql --datadir=%s' % data_dir) == 0:
        print 'mysql初始化成功'
    else:
        exit('mysql初始化失败')
		
    os.system('cp support-files/mysql.server /etc/init.d/mysqld')
    os.system('mv /etc/my.cnf /etc/my.cnf.bak')
    os.chdir(current_dir)
    os.system('cp my.cnf /etc/my.cnf')
    os.system('service mysqld start')
    os.system('chkconfig mysqld on')

install_mysql()

if os.path.exists('/etc/profile'):
    os.system('cp /etc/profile /etc/profile.bak')
if os.system('echo "PATH=%s/bin:%s/lib:$PATH" >> /etc/profile' % (install_dir, install_dir)) == 0:
    print '修改/etc/profile成功'
else:
    exit()
if os.system('echo "export PATH" >> /etc/profile') == 0:
    print '修改/etc/profile文件成功'
else:
    exit()
