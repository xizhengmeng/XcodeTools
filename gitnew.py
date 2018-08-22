#!/usr/bin/env python
#coding:utf-8

import sys,os,time,shutil
import urllib 
import urllib2

os.system('cd ../../')

if os.path.exists(".config"):
   shutil.rmtree(".config")

os.mkdir(".config")
os.chdir(".config")

os.system('pwd')

print "start to download ..."
url = 'https://github.com/xizhengmeng/XcodeTools.git'
os.system('git clone https://github.com/xizhengmeng/XcodeTools.git')
os.system('cd XcodeTools')
os.system('/usr/bin/git add .')
os.system('/usr/bin/git commit -m \'ceshi\'')
os.system('/usr/bin/git pull')
os.system('/usr/bin/git checkout templete')

filePath = "/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/Xcode/Templates/File Templates/JDJRCustom"
if os.path.exists(filePath):
   print 'file exists. start to remove file'
shutil.rmtree(filePath)
print 'file remove done'
shutil.copytree("XcodeTools/Custom",filePath)
os.chdir("../../")
shutil.rmtree(".config")
print 'update success'
