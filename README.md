# babyguard
六、配置过程
（1）购买云服务器

（2）公网IP登陆---设置root账号---加载磁盘（手动）---SSH设置60秒发NOP---配置locale

dpkg-reconfigure locales
http://www.qcloud.com/wiki/Linux%E7%B3%BB%E7%BB%9F%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%B0%8F%E4%BA%8E2TB%E6%95%B0%E6%8D%AE%E7%9B%98%E6%93%8D%E4%BD%9C%E6%8C%87%E5%BC%95

echo '/dev/vdb1 /data ext3 defaults 0 0' >> /etc/fstab
apt-cache search ffmpeg

apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev
apt-get install php5-common libapache2-mod-php5 php5-cli
apt-get install nodejs-legacy
apt-get install npm
apt-get install mysql-server
apt-get install php5-mysql
apt-get install autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev
apt-get install readline readline-devel readline-static
apt-get install openssl openssl-devel openssl-static
apt-get install sqlite-devel
apt-get install bzip2-devel bzip2-libs
apt-get install git
apt-get install apache2
apt-get install python-pip
apt-get install subversion
apt-get install install readline readline-devel readline-static
apt-get install install openssl openssl-devel openssl-static
apt-get install install sqlite-devel
apt-get install install bzip2-devel bzip2-libs

/etc/init.d/apache2 stop
/etc/init.d/apache2 start

/etc/init.d/ssh restart
PasswordAuthentication yes
PermitRootLogin yes

配置硬盘
mount /dev/vdb1 /data
echo '/dev/vdb1 /data ext3 defaults 0 0' >> /etc/fstab
http://www.qcloud.com/wiki/%E7%99%BB%E5%BD%95%E5%88%B0Linux%E4%BA%91%E6%9C%8D%E5%8A%A1%E5%99%A8

（3）安装pyenv+virtualenv
http://seisman.info/python-pyenv.html
https://github.com/yyuu/pyenv-virtualenv

CFLAGS=-I/usr/include/openssl \
LDFLAGS=-L/usr/lib64 \
pyenv install -v 3.3.3

pyenv install --list
pyenv rehash
pyenv global 3.3.3
pyenv versions

git clone https://github.com/yyuu/pyenv-virtualenv.git
cd pyenv-virtualenv/
./install.sh
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
pyenv virtualenv 3.3.3 env333

pyenv global env333
pyenv versions


（4）安装配置django
pip install Django-1.8.12
pip install pytz
pip3 install tencentyun
pip install requests

https://github.com/Grokzen/redis-py-cluster
https://github.com/tencentyun/python-sdk

./redis-trib.rb fix 123.206.69.25:7000
redis-cli -p 7000 cluster nodes

（5）配置redis集群
apt-get install ruby rubygems

下载gz文件
解压
make
配置redis.conf
启动

ps aux | grep redis | grep 700 | awk '{print $2}' | xargs -i kill -9 {}
wget http://download.redis.io/releases/redis-3.0.7.tar.gz
wget  https://rubygems.org/downloads/redis-3.1.0.gem
http://www.cnblogs.com/gomysql/p/4395504.html
gem install -l redis-3.1.0.gem

./redis-trib.rb create --replicas 1 123.206.69.25:7000 123.206.71.180:7000 123.206.69.205:7000 123.206.71.180:7001 123.206.69.205:7001 123.206.69.25:7001

 删除所有数据
/data/file_dir/redis-3.0.7/src/redis-cli -c -p 7000 -h 123.206.71.180

（6）配置反向代理
http://blog.chinaunix.net/uid-27155075-id-3446846.html
原理讲解：
1、启用3个模块
2、配置好proxy.load
3、重启服务
即可。至于.htaccess可以不要

(1)安装启用
aptitude install -y libapache2-mod-proxy-html libxml2-dev
a2enmod wsgi
a2dismod proxy
/usr/sbin/a2enmod rewrite
/usr/sbin/a2enmod proxy_http
/usr/sbin/a2enmod proxy_html
apache2ctl -t
cat /var/log/apache2/error.log

(2)在/var/www/html目录下增加文件 .htaccess，配置如下
Options -Indexes
<IfModule mod_rewrite.c>
RewriteEngine on
RewriteBase /test
RewriteRule .*$ http://182.254.217.24:8000/lab/wx_open
</IfModule>

（3）配置proxy.load
root@VM-167-55-debian:/etc/apache2/mods-enabled# cat proxy.load
LoadModule proxy_module /usr/lib/apache2/modules/mod_proxy.so

ProxyPass /test http://182.254.217.24:8000/lab/wx_open
ProxyPass /test http://182.254.217.24:8000/lab/wx_open
ProxyPass /net/ http://182.254.217.24:8000/net/
ProxyPass /king http://182.254.217.24/kinconfuse
ProxyPass /vr http://123.206.69.25:9000/

service apache2 restart

(7)配置gunicorn，supervisorctrl
apt-get install supervisor
pip install gunicorn

vi /etc/supervisor/conf.d/vr.conf
supervisorctl reread
supervisorctl update
supervisorctl stop vr
supervisorctl start vr

(8)配置ftp
安装软件
aptitude install vsftpd

添加ftp用户useradd
useradd -d /data/ftpuser -s /bin/bash -m ftpuser
/etc/init.d/vsftpd restart
passwd ftpuser
chmod -R 777 ftpuser

改动后要重启服务
/etc/init.d/vsftpd restart

（9）配置apache2的conf，使得http可以链接
Alias /ftpuser/ "/var/www/html/ftpuser/"
<Directory /var/www/html/ftpuser/>
    AllowOverride None
    Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    Order allow,deny
    Allow from all
</Directory>

（10）libav音视频工具的操作
apt-get install libav-tools

五、最终方案
（1）安装redis cluster
https://github.com/Grokzen/redisco/tree/python3

（2）使用redisco的cluster版本调用
https://github.com/Grokzen/redis-py-cluster
https://github.com/Grokzen/redisco/tree/python3

修改源码redisco的__init__.py：
from rediscluster import StrictRedisCluster
return StrictRedisCluster(startup_nodes=startup_nodes, max_connections=32, socket_timeout=0.1, decode_responses=True)

（3）操作步骤
http://www.cnblogs.com/gomysql/p/4395504.html
ps aux | grep redis | grep 700 | awk '{print $2}' | xargs -i kill -9 {}
redis-trib create --replicas 1 127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005

(error) NOAUTH Authentication required.

sh-3.2# /usr/local/redis-2.8.1/src/redis-cli -a mypassword
bind 0.0.0.0
git remote show origin
service zookeeper restart
/usr/share/zookeeper/bin/zkServer.sh restart
ls /zk/codis/db_test/fence
rmr /zk/codis
