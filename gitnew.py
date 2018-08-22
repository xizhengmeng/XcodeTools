#!/usr/bin/env python
#coding:utf-8

import sys,os,time,shutil
import urllib 
import urllib2

if os.path.exists(".config"):
   shutil.rmtree(".config")

os.mkdir(".config")
os.chdir(".config")

os.system('pwd')

print "start to download ..."
url = 'https://github.com/xizhengmeng/XcodeTools.git'
os.system('git clone https://github.com/xizhengmeng/XcodeTools.git')
os.chdir("XcodeTools")

os.system('pwd')

os.system('git branch')

# os.system('/usr/bin/git add .')
# os.system('/usr/bin/git commit -m \'ceshi\'')
# os.system('/usr/bin/git pull')
os.system('/usr/bin/git checkout snippets')

home = os.environ['HOME']

filePath = home + "/Library/Developer/Xcode/UserData/CodeSnippets"
if os.path.exists(filePath):
   print 'file exists. start to remove file'
   shutil.rmtree(filePath)
   print 'file remove done'
shutil.copytree("Snippets",filePath)
os.chdir("../../")
shutil.rmtree(".config")
print 'update success'

os.system('pwd')
