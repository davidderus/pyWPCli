#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importing a few things
import subprocess
import sys, os
import tools
import urllib2

# Default settings for Git
useGit = True
useGflow = True

# A few way to say yes and no (used later when asking the user)
yes = ['Y', 'y', 'yes']
no = ['N', 'n', 'no']

# All the WP-Cli Commands required by the script
coreCmds = [
	{'cmd': ['wp', 'core', 'download'], 'arg': [{'value': 'locale', 'descr': 'Langage locale'}], 'type' : 'Installing Core Bundle'},
	{'cmd': ['wp', 'core', 'config'], 'arg': [{'value': 'dbhost', 'descr': 'Database Host'}, {'value': 'dbname', 'descr': 'Database Name'}, {'value': 'dbuser', 'descr': 'Database User'}, {'value': 'dbpass', 'descr': 'Database Password'}, {'value': 'dbprefix', 'descr': 'Datapase prefix, like wp_'}], 'type': 'Writing config'},
	{'cmd': ['wp', 'core', 'install'], 'arg': [{'value': 'url', 'descr': 'WordPress URL'}, {'value': 'title', 'descr': 'WordPress Title'}, {'value': 'admin_user', 'descr': 'WordPress Admin User'}, {'value': 'admin_password', 'descr': 'WordPress Admin Password'}, {'value': 'admin_email', 'descr': 'WordPress Admin Email'}], 'type': 'Setting Up WordPress'},
]

themeCmds = [
	['wp', 'theme', 'install']
]

pluginCmds = [
	['wp', 'plugin', 'install']
]

# Printing credentials
cred = '''
                    __          _______   _____ _ _ 
                    \ \        / /  __ \ / ____| (_)
           _ __  _   \ \  /\  / /| |__) | |    | |_ 
          | '_ \| | | \ \/  \/ / |  ___/| |    | | |
          | |_) | |_| |\  /\  /  | |    | |____| | |
          | .__/ \__, | \/  \/   |_|     \_____|_|_|
          | |     __/ |                             
          |_|    |___/                              1.0

----------------------------------------------------------------------
By : David Dérus (@davidderus)
----------------------------------------------------------------------
'''

# Showing Credentials
print tools.colorize(cred, 'green')

# Checking WP-Cli existence, exiting if unavailable
if tools.processTester(['wp']):
	print tools.colorize('You have to install WP-Cli before running the script : http://wp-cli.org/', 'red', bold=True)
	sys.exit(0)

# Asking for destination directory
userInstallDir = raw_input('▲ Destination directory? (Default: %s) ' % tools.colorize('Current', 'blue', bold=True))

# Making a few checks about the destination dir
differentDir = False
if userInstallDir is '':
	installDir = os.getcwd()
elif not os.path.isdir(userInstallDir):
	os.makedirs(userInstallDir)
	if os.path.isdir(userInstallDir):
		installDir = userInstallDir
		differentDir = True
	else:
		print tools.colorize('Unable to create directory, aborting...', 'red')
else:
	installDir = userInstallDir
	differentDir = True

# Asking a few Git related questions
if raw_input('▲ Do you want to use git? (%s%s) ' % (tools.colorize('Y', 'green', bold=True), tools.colorize('n', 'blue'))) in no:
	useGit = False

if raw_input('▲ Do you want to use git flow? (%s%s) ' % (tools.colorize('Y', 'green', bold=True), tools.colorize('n', 'blue'))) in no:
	useGflow = False

# If user choose a different dir, we change script working directory
if differentDir:
	os.chdir(installDir)

# Initializing Git
if(useGit):
	print subprocess.check_output(['git', 'init'])

# Initializing Git Flow (great tool btw!)
if(useGflow):
	print subprocess.check_output(['git', 'flow', 'init', '-d'])

# Setting up gitignore from remote repo
if(useGit):
	try:
		data = urllib2.urlopen('https://raw.githubusercontent.com/github/gitignore/master/WordPress.gitignore')
	except Exception, e:
		print tools.colorize('Unable to get remote .gitignore content', 'red', bold=True)
	else:
		with open('.gitignore', 'w') as f:
			f.write(data.read())
		tools.doCommit('[+] Project: Adding WordPress .gitignore')

# Installing Core
print tools.doExec(coreCmds, None, useGit)
print tools.colorize('Core CMDs Done', 'green', highlight=True), '\n'

# Installing Theme
if raw_input('▲ Do you want to install a custom theme? (%s%s) ' % (tools.colorize('N', 'green', bold=True), tools.colorize('y', 'blue'))) in yes:
	print tools.doExec(themeCmds, raw_input('Theme Name or URL? '), useGit)
	print tools.colorize('Theme installed', 'green', highlight=True), '\n'

# Installing Plugins
pluginsInstall = raw_input('▲ Plugins to install? (%s or %s) \n' % (tools.colorize('Plugin name', 'blue'), tools.colorize('exit', 'red')))
while pluginsInstall.strip() != 'exit':
	print tools.colorize('Installing %s' % pluginsInstall, 'blue')
	print tools.doExec(pluginCmds, pluginsInstall, useGit)
	pluginsInstall = raw_input('▲ Plugins to install? (%s or %s) \n' % (tools.colorize('Plugin name', 'blue'), tools.colorize('exit', 'red')))

# The End
print tools.colorize('All Done, exiting!', 'green', highlight=True, bold=True)