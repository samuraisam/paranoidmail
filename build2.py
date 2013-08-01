"""
Second stage build.

This file must be executed from the virtualenv!
"""
import os
import subprocess
import pwd
import grp
from lib import *

HOST = 'localhost'
MAILSERVER_NAME = 'smtp.localhost'
MYSQL_ROOT_PASSWORD = 'O_MAH_GAH'
MYSQL_MAIL_PASSWORD = 'YA_WAI_LOL'
ROOT_MAIL_PASSWORD = 'MYPASSWORDLOLOL'

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
		 _input=rtmpl('templates/mysql_debconf', password=MYSQL_ROOT_PASSWORD))
	chko(['debconf-set-selections'],
		 _input=rtmpl('templates/mysql_debconf_again', password=MYSQL_ROOT_PASSWORD))
	
	chko(['apt-get', 'install', '-y', 'mysql-client', 'mysql-server'])

	# create databases/permissions
	chko(['mysql', '-u', 'root', '-p{}'.format(MYSQL_ROOT_PASSWORD)],
		 _input=rtmpl('templates/create_table_and_perms.sql', password=MYSQL_MAIL_PASSWORD))

	# create tables
	chko(['mysql', '-u', 'mail', '-p{}'.format(MYSQL_MAIL_PASSWORD), 'maildb'],
		 _input=rtmpl('templates/aliases_domains_users.sql'))

	# config and restart
	chko(['cp', fnrs('conf/mysql/my.cnf'), '/etc/mysql/my.cnf'])
	chko(['/etc/init.d/mysql', 'restart'])


def setup_postfix():
	print 'setting up postfix...'

	# install postfix
	chko(['debconf-set-selections'],
		 _input="postfix postfix/mailname string {}".format(HOST))
	chko(['debconf-set-selections'],
		 _input="postfix postfix/main_mailer_type string 'Internet Site'")

	chko(['apt-get', 'install', '-y', 'postfix', 'postfix-mysql'])

	chko(['tee', '/etc/mailname'],
		 _input=MAILSERVER_NAME)

	# configure postfix
	chko(['cp', fnrs('conf/postfix/main.cf'), '/etc/postfix/main.cf'])
	chko(['cp', '/etc/aliases', '/etc/postfix/aliases'])
	chko(['postalias', '/etc/postfix/aliases'])

	# set up mail dir and users
	chko(['mkdir', '-p', '/var/spool/mail/virtual'])
	try:
		grp.getgrnam('virtual')
	except KeyError:
		chko(['groupadd', '--system', 'virtual', '-g', '5000'])
	try:
		pwd.getpwnam('virtual')
	except KeyError:
		chko(['useradd', '--system', 'virtual', '-u', '5000', '-g', '5000'])
	chko(['chown', '-Rv', 'virtual:virtual', '/var/spool/mail/virtual'])

	for nam in ['alias', 'domains', 'mailbox']:
		chko(['cp', rtmpl_to_file('conf/postfix/mysql_{}.cf'.format(nam), 
							      'postfix_mysql_{}.cf'.format(nam), 
							      password=MYSQL_MAIL_PASSWORD), 
		      '/etc/postfix/mysql_{}.cf'.format(nam)])

def setup_courier():
	print 'setting up courier...'
	
	# install courier and dependencies
	chko(['debconf-set-selections'],
		 _input="courier courier-base/webadmin-configmode boolean 1")
	chko(['debconf-set-selections'],
		 _input="courier courier-ssl/certnotice boolean 1")

	chko(['apt-get', 'install', '-y', 'courier-base', 'courier-authdaemon',
		  'courier-authlib-mysql', 'courier-imap', 'courier-imap-ssl', 'courier-ssl'])

	# configure courier
	chko(['cp', fnrs('conf/courier/authdaemonrc'), '/etc/courier/authdaemonrc'])
	chko(['cp', fnrs('conf/courier/authmysqlrc'), '/etc/courier/authmysqlrc'])

def setup_root_mail_account():
	chko(['mysql', '-u', 'mail', '-p{}'.format(MYSQL_MAIL_PASSWORD), 'maildb'],
		 _input=rtmpl('templates/localhost_users.sql', password=ROOT_MAIL_PASSWORD))

if __name__ == '__main__':
	setup_firewall()
	setup_mysql()
	setup_postfix()
	setup_courier()
	setup_root_mail_account()
