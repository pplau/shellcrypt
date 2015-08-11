# coding: utf-8

'''
Created on 2015.7.22

NOTE:
1. 使用Python3运行
2. Package Path 为部署文件
3. Main Shell 为初始化脚本名称，必须位于部署文件的一级目录
4. Libs 为脚本文件夹名称（非路径），可以有子目录，但是所有脚本必须位于该路径下
5. Output Path 为新生成的加密脚本后部署文件的路径

@author: liuyb
'''

import os
import os.path


def CopyFiles(sourceDir,  targetDir):        
    for file in os.listdir(sourceDir): 
        sourceFile = os.path.join(sourceDir,  file) 
        targetFile = os.path.join(targetDir,  file) 
        if os.path.isfile(sourceFile): 
            if not os.path.exists(targetDir):  
                os.makedirs(targetDir)  
            if not os.path.exists(targetFile) or(os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):  
                 open(targetFile, "wb").write(open(sourceFile, "rb").read()) 
        if os.path.isdir(sourceFile): 
            CopyFiles(sourceFile, targetFile)

            
def ModifyMainShell(mainshellDir):
    input = open(mainshellDir)  
    lines = input.readlines()  
    input.close()    
    output = open(mainshellDir,'w'); 
    for line in lines:           
        if not line:      
            break  
        if 'bash' in line and "#!/bin/bash" not in line:  
            temp = line.split("bash")  
            temp1 = temp[0] + temp[1]  
            output.write(temp1)  
        else:    
            output.write(line)  
    output.close()  
    os.environ['MDIR']=str(mainshellDir)
    os.environ['MCDIR']=str(mainshellDir+".x.c")
    os.system('CFLAGS=-static shc -r -f $MDIR')
    os.system('rm $MDIR')
    os.system('rm $MCDIR')


def EncryptLibs(libsDir):
    for file in os.listdir(libsDir):
        sourceFile = os.path.join(libsDir,  file)
        if os.path.isfile(sourceFile):
            if sourceFile.find(".sh") > 0:
                os.environ['LDIR']=str(sourceFile)
                os.environ['CDIR']=str(sourceFile+'.x.c')
                os.system("CFLAGS=-static shc -r -f $LDIR")
                os.system('rm $LDIR')
                os.system('rm $CDIR')

        if os.path.isdir(sourceFile): 
            EncryptLibs(sourceFile)


def Rename(Dir, libsDir):
    os.environ['RDIR']=str(Dir)
    os.system("cd $RDIR && rename 's/\.sh.x/\.sh/' *")
    for file in os.listdir(Dir):
        sourceFile = os.path.join(Dir,  file)
        if os.path.isfile(sourceFile):
            pass
        if os.path.isdir(sourceFile) and sourceFile is libsDir:
            Rename(sourceFile)


def Shc():
    pass


def BuildDeb(mainshellDir):
    pass




if  __name__ =="__main__": 
    
    PKG_PATH = input("Package Path (eg:/home/vinzor/all) :")
    MAINSHELL = input("Main Shell (eg:run.sh) :")
    LIBS = input("Libs (eg:libs) :")
    OPT_PATH = input("Output Path (eg:/home/vinzor/temp) :")
    MAINSHELL_PATH = OPT_PATH+'/'+MAINSHELL  
    LIBS_PATH = OPT_PATH+'/'+LIBS
    
    print("Copying...")
    CopyFiles(PKG_PATH, OPT_PATH)
    print("Encrypting...")
    ModifyMainShell(MAINSHELL_PATH)
    EncryptLibs(LIBS_PATH)
    Rename(OPT_PATH, LIBS_PATH)
    print("Finish")


