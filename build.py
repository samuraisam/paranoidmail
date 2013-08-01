import os
import subprocess
from lib import *

if __name__ == '__main__':
	# create the build dir if it doesn't exist
	if not os.path.exists(fnrs('build')):
		chko(['mkdir', fnrs('build')])
	# create a virtualenv
	chko(['apt-get', 'install', '-y', 'python-virtualenv'])
	chko(['virtualenv', fnrs('build/mail'), '--distribute'])
	# install requirements into it
	chko([fnrs('build/mail/bin/pip'), 'install', 'jinja2'])
	# execute the stage 2 build in the virtualenv
	chko([fnrs('build/mail/bin/python'), fnrs('build2.py')])
