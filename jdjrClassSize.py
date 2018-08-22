#!/usr/bin/env python
#coding:utf-8

import sys,os,time
from pyExcelerator import *
from biplist import *

def analyse():

	if os.path.exists('JDFinance.xcworkspace') == False:
	   print '请切换至京东金融代码库下'
	   sys.exit(1)

	time1 = time.time()

	filestring = os.popen('find . -name *.m').read()

	fileitems = filestring.split('\n')

	projectList = []

	cureentProName = ''
	cureentFileList = []

	fileHnotExists = []

	for item in fileitems:
	    if 'Target Support Files' in item:
	    	continue

	    filePaths = item.split('/')
	    if len(filePaths) < 2:
	    	continue
	    projectName = filePaths[1]
	    projectFile = filePaths[-1].replace('.m','')

	    modelList = []
	    itemh = item.replace('.m','.h')
	    if os.path.exists(itemh):
	       lines = open(itemh,'r').read().split('\n')
	       for line in lines:
	           if '@interface' in line:
	              filenameN = line.split(' ')[1]
	              filenameN = filenameN.replace(':','')
	              if filenameN not in modelList:
	                 modelList.append(filenameN)
	    else:
	       fileHnotExists.append(item)          
	       
	    index = projectFile.find('+')
	    if index != -1:
	       filenames = projectFile.split('+')
	       projectFile = filenames[0] + '(' + filenames[1] + ')'	

	    if len(cureentProName) == 0:
	       cureentProName = projectName
	       cureentFileList.append(projectFile)
	       continue
	    
	    if cureentProName == projectName:
	    	if len(modelList) > 0:
	           cureentFileList = cureentFileList + modelList 
	        else:
	           cureentFileList.append(projectFile)
	    else:
	       Dict = {}
	       Dict[cureentProName] = cureentFileList
	       cureentFileList = []
	       cureentProName = projectName
	       if len(modelList) > 0 and projectFile in modelList:
	           cureentFileList = cureentFileList + modelList 
	       else:
	           cureentFileList.append(projectFile)
	       projectList.append(Dict) 

	filepathString = os.popen('find ~/Library/Developer/Xcode/DerivedData -name JDMobile.app').read()
	filepaths = filepathString.split('\n')

	lastTime = 0
	lastTimeString = ''
	lastPath = ''

	if len(filepaths) == 0:
	   sys.exit(1)

	for filepath in filepaths:
	    timestring = os.popen('GetFileInfo ' + filepath + ' | grep modified').read()
	    if 'modified:' in timestring:
	        timestring = timestring.replace('modified: ','')
	        timestring = timestring.replace(chr(10),'')

	        localtime = time.mktime(time.strptime(timestring, '%m/%d/%Y %H:%M:%S'))
	        if localtime > lastTime:
	           lastTime = localtime
	           lastPath = filepath
	           lastTimeString = timestring


	Dict = readPlist(lastPath+'/Info.plist') 

	appversion = Dict['CFBundleShortVersionString']
	buildversion = Dict['CFBundleVersion']

	lastPath = lastPath + '/JDMobile'       

	filestring = os.popen('nm -v ' + lastPath).read()
    
	index64 = filestring.find('for architecture')
	if index64 == -1:
	   print '\033[1;31m' + ('只有64位架构，请执行command + b') + '\033[0m' 

	classitems = filestring.split('\n')

	currentClass = ''
	firstAddress = 0
	cachAdd = 0
	cachAddVar = 0
	currentClassVar = ''
	firstAddressVar = 0

	count = 0
	arm32Dict = {}
	arm64Dict = {}

	for item in classitems:
	    
	    if 'for architecture' in item:
	    	currentClass = ''
	        firstAddress = 0
	        continue

	    if 'IVAR_$' in item:

	        items = item.split(chr(32))
	        address = int(items[0],16)
	        className = items[2]

	        className = className.replace('_OBJC_IVAR_$_','')
	        className = className.split('._')[0]

	        if len(currentClass) == 0:
	           currentClassVar = className
	           firstAddressVar = address
	           continue
	        if className != currentClassVar:
	           if '_OBJC_CLASS_' in items[0]:
	               currentClassVar = ''
	               firstAddressVar = 0
	           
	           if len(currentClassVar) == 0:
	           	   continue
	           if '000000' in items[0]:
	               size = arm64Dict.get(currentClassVar)
	               if type(size) == type(None):
	               	  size = 0
	               arm64Dict[currentClassVar] = size + address - firstAddressVar
	           else:
	               size = arm64Dict.get(currentClassVar)
	               if type(size) == type(None):
	                  size = 0
	               arm32Dict[currentClassVar] = size + address - firstAddressVar
	      
	           firstAddressVar = address
	           currentClass = className

	        cachAddVar = address    

	    if '-[' in item or '+[' in item or '_conv_kernel' in item:

	       items = item.split(chr(32))
	       address = int(items[0],16)
	       className = items[2]

	       indexL = items[2].find('-[')
	       indexR = items[2].find('+[')

	       if indexL != -1:
	          className = items[2][indexL + 2:]
	       
	       if indexR != -1:	
	       	  className = items[2][indexR + 2:]
	       
	       if len(currentClass) == 0:
	          currentClass = className
	          firstAddress = address
	       	  continue
	       
	       if className != currentClass:
	       	  if '_conv_kernel' in item:
	       	  	 address = cachAdd + 350
	           
	       	  if '000000' in items[0]:
	             arm64Dict[currentClass] = address - firstAddress + 700
	             count = count + 1
	          else:
	          	 arm32Dict[currentClass] = address - firstAddress + 700
	          	 count = count + 1
	          
	          if '_conv_kernel' in item:
	             currentClass = ''
	             firstAddress = 0
	          else:  
	       	     firstAddress = address
	       	     currentClass = className

	       cachAdd = address     

	print ''
	print ''
	print '******************'

	totalSize = 0

	for item in projectList:
	    key = item.keys()
	    fileList = item[key[0]]
	    size = 0
	    for fileName in fileList:
	    	
	        file32Size = arm32Dict.get(fileName)
	        file64Size = arm64Dict.get(fileName)
	        if type(file32Size) == type(None):
	           # print fileName
	           file32Size = 100
	        if type(file64Size) == type(None):
	           file64Size = 100 

	        size = file32Size + file64Size + size
	    
	    totalSize = totalSize + size
	    print '模块名称:'+ key[0],'   模块体积:%.2fM' % (size / 1024.0 / 1024.0), '--->%.3fK' % (size / 1024.0),'  模块文件个数%d' % len(fileList)  
	 
	print '加载类总数%d' % (count / 2)
	print '代码总体积:%.2fM' % (totalSize / 1024.0 / 1024.0)

	w = Workbook()  #创建一个工作簿

	for item in projectList:
	    
	    detailList = []
	    key = item.keys()
	    ws = w.add_sheet(key[0])  #创建一个工作表
	    fileList = item[key[0]]

	    for fileName in fileList:
	        file32Size = arm32Dict.get(fileName)
	        file64Size = arm64Dict.get(fileName)

	        if type(file32Size) == type(None):
	           file32Size = 0
	        if type(file64Size) == type(None):
	           file64Size = 0 
	   
	        size = file32Size + file64Size
	        detail = [fileName,size]
	        detailList.append(detail)

	    sortListNew = sorted(detailList, key=lambda detailItem: detailItem[1],reverse=True)
	    
	    countM = 0
	    for sortItem in sortListNew:
	        
	        ws.write(countM,0,sortItem[0]) #在1行1列写入bit
	        ws.write(countM,1,sortItem[1])
	        if sortItem[1] > 1024 and sortItem[1] < 1024 * 1024:
	            ws.write(countM,2,'%.2fK' % (sortItem[1]/1024.0))
	        elif sortItem[1] < 1024:
	            ws.write(count,2,sortItem[1])
	        else:
	            ws.write(countM,2,'%.2fM' % (sortItem[1]/1024.0/1024.0))            
	        countM = countM + 1

	    # print sortListNew

	time2 = time.time()

	print '\033[1;34m' + ('耗时%.2fs' % (time2 - time1)) + '\033[0m'
	print '\033[1;34m' + ('app版本号:' + appversion ) + '\033[0m'
	print '\033[1;34m' + ('app的build号:' + buildversion ) + '\033[0m'

	filePath = os.environ['HOME'] + '/' + '.Trash/JDJR' + appversion + 'Analyse.xls'

	w.save(filePath)  #保存
	os.system('open ' + filePath)


