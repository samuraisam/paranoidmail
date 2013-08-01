import os
import subprocess


# filename relative to self
def fnrs(filename):
	return os.path.join(
		os.path.abspath(os.path.dirname(__file__)),
		filename
	)


# check output of a shell command. arguments passed to subprocess.Popen
def chko(*a, **kw):
	kw['stderr'] = subprocess.PIPE
	kw['stdout'] = subprocess.PIPE
	kw['stdin'] = subprocess.PIPE

	input = kw.pop('_input', None)

	if chko.verbose:
		print ''
		print '===>', ' '.join(a[0])
		print ''

	proc = subprocess.Popen(*a, **kw)
	if input:
		if chko.verbose:
			print '<=== (stdin)'
			print input
			print ''
		output = proc.communicate(input=input)
		if chko.verbose and len(output[0]):
			print output[0]
	else:
		output = ['', '']
	
		if chko.verbose:
			while proc.poll() is None:
				o = proc.stdout.readline()
				if len(o):
					print o,
				o = proc.stderr.readline()
				if len(o):
					print o,
			output = proc.communicate()
			if len(output[0]):
				print output[0]
		else:
			output = proc.communicate()
			if len(output[0]):
				print output[0]

	if proc.returncode != 0:
		print 'Unsuccessful return code:', proc.returncode
		print 'Output: ', output[1]
		raise Exception("Bad Return Code")

	return proc

chko.verbose = True

def rtmpl(template_name, **kw):
	ct = open(fnrs('templates/{}'.format(template_name)), 'r').read()
	from jinja2 import Template
	t = Template(ct)
	return t.render(**kw)

def rtmpl_to_file(template_name, file_name, **kw):
	"""
	Renders a template `template_name` to file `file_name` with
	the replacements `**kw`.

	Returns the filename that was written out.
	"""
	fn = fnrs('build/{}'.format(file_name))
	with open(fn, 'w') as f:
		f.write(rtmpl(template_name, **kw))
	return fn
