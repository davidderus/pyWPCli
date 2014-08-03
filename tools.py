#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import subprocess

######################################################
# Generate syntax to display colors in Terminal
######################################################

# First Color, then Text
model = '\033[%sm%s\033[1;m'

# Accepted color in a terminal
colorList = {
	'gray': '30',
	'red': '31',
	'green': '32',
	'yellow': '33',
	'blue': '34',
	'magenta': '35',
	'cyan': '36',
	'white': '37',
	'crimson': '38'
}

# Main function, accepting a text, a color in text, and boolean options like bold or highlight 
def colorize(text, color, bold=False, highlight = False):
	# Checking if we output text in a TTY
	if not sys.stdout.isatty(): return text
	# Putting the dict value in a var
	foundColor = colorList[color]
	# Making the colorvalue string for the output 
	colorValue = ';'.join([str(int(bold)), foundColor if not highlight else str(int(foundColor)+10)])
	# Returning the formated string
	return model % (colorValue, text)

######################################################
# Test tool existence via SubProcess
######################################################

def processTester(processList):

	missing = []

	for process in processList:
		try:
			result = subprocess.check_output([process, '--version'])
		except Exception, e:
			missing.append(process)

	if missing:
		return missing
	else:
		return None


######################################################
# Short func to commit changes
######################################################

def doCommit(gitMsg = None):
	subprocess.call(['git', 'add', '-A'])
	subprocess.call(['git', 'commit', '-m', str(gitMsg)])


######################################################
# Launch install commands in shell and commit if asked
# Why exec? Because PHP? #IYKWIM
######################################################

def doExec(cmds, answer = None, useGit = False):
	msg = None
	for item in cmds:
		argz = []
		if type(item) is dict:
			print '\n', colorize(item['type'], 'blue', highlight=True)
			for arg in item['arg']:
				answer = raw_input('▲ ' + arg['descr'] + '? ')
				argz.append('--' + arg['value'] + '=' + answer)
			try:
				msg = subprocess.check_output(item['cmd'] + argz)
			except Exception, e:
				sys.exit(0)
		else:
			item.append(answer)
			try:
				msg = subprocess.check_output(item)
			except Exception, e:
				sys.exit(0)

		if useGit:
			gitMsg = item['type'] if type(item) is dict else 'Adding ' + answer
			doCommit('[+] Project: %s' % gitMsg)

	return msg