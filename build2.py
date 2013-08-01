"""
Second stage build.

This file must be executed from the virtualenv!
"""
import os
import subprocess
from lib import *

HOST = 'localhost'
MYSQL_ROOT_PASSWORD = 'O_MAH_GAH'
MYSQL_MAIL_PASSWORD = 'YA_WAI_LOL'


# set up the firewall
def setup_firewall():
	print 'setting up firewall...'

	# copy the configs 
	chko(['apt-get', 'install', '-y', 'shorewall', 'shorewall-doc'])
	chko(['cp', '/usr/share/doc/shorewall/default-config/zones', '/etc/shorewall'])
	for name in ['hosts', 'interfaces', 'policy', 'routestopped', 'rules', 'zones']:
		chko(['cp', fnrs('conf/shorewall/' + name), '/etc/shorewall/' + name])
	chko(['cp', fnrs('conf/default/shorewall'), '/etc/default/shorewall'])

	print 'starting firewall...'

	chko(['/etc/init.d/shorewall', 'restart'])


def setup_mysql():
	print 'setting up mysql...'
	chko(['debconf-set-selections'], 
		 _input=rtmpl('mysql_debconf', password=MYSQL_ROOT_PASSWORD))
	chko(['debconf-set-selections'],
		 _input=rtmpl('mysql_debconf_again', password=MYSQL_ROOT_PASSWORD))
	
	chko(['apt-get', 'install', '-y', 'mysql-client', 'mysql-server'])

	# create databases/permissions
	chko(['mysql', '-u', 'root', '-p{}'.format(MYSQL_ROOT_PASSWORD)],
		 _input=rtmpl('create_table_and_perms.sql', password=MYSQL_MAIL_PASSWORD))

	# create tables
	chko(['mysql', '-u', 'mail', '-p{}'.format(MYSQL_MAIL_PASSWORD), 'maildb'],
		 _input=rtmpl('aliases_domains_users.sql'))

	# config and restart
	chko(['cp', fnrs('conf/mysql/my.cnf'), '/etc/mysql/my.cnf'])
	chko(['/etc/init.d/mysql', 'restart'])


def setup_postfix():
	print 'setting up postfix...'

	chko(['debconf-set-selections'],
		 _input="postfix postfix/mailname string {}".format(HOST))
	chko(['debconf-set-selections'],
		 _input="postfix postfix/main_mailer_type string 'Internet Site'")

	chko(['apt-get', 'install', '-y', 'postfix', 'postfix-mysql'])


if __name__ == '__main__':
	setup_firewall()
	setup_mysql()
	setup_postfix()
