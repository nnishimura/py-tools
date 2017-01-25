
#
# Example File sorting script
# 
# Usage :  
# FILE_NAME 40156-80-m-01-dl.jpg
# move to /40156/40156-80/40156-80-m-01-dl.jpg
# FILE_NAME 40156-m-01-dl.jpg
# move to /40156/40156-80-m-01-dl.jpg
#
# Author: Naoko Nishimura
#
# Date: 17/1/25
#


import os
import shutil


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

for folderName,subfolders,filenames in os.walk('./TEST_EPOI'):
	# print('The current folder is' + folderName)

	for subfolder in subfolders:
		print('subfolder of ' + folderName + ':' + subfolder)
        for filename in filenames:
                if(filename == ".DS_Store"):
                    continue
                fname,fext = os.path.splitext(filename)
                dirname = "./" +folderName +"/" + fname[0:3]
                dirname_sub = dirname + "/" + fname[0:7]
                dirname_sub_after = fname[0:7].split("-")[1]
                fullpath = folderName+"/"+filename

                if(not os.path.exists(dirname)):
                    os.mkdir(dirname)
                if(RepresentsInt(dirname_sub_after)):
                    if(not os.path.exists(dirname_sub)):
                        os.mkdir(dirname_sub)
                    shutil.move(fullpath, dirname_sub)
                else:
                    shutil.move(fullpath, dirname)
                
                print(fname[0:7].split("-"),RepresentsInt(dirname_sub_after))