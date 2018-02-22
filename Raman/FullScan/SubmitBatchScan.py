import os
from ROOT import *


os.system('rm limits_2hdm.txt')

def SubmitJobfunc(mzp, ma0):
    mzp_ = str(mzp)
    ma0_ = str(ma0)
    postname=str(mzp_)+'_'+str(ma0_)
    shellfilename = 'temporary_Res_submit_'+postname+'.sh'
    os.system('rm '+shellfilename)

    
    fileshell = open(shellfilename,'a')
    for linesh in open('Template_submit_batch.sh','r'):
        linesh = linesh.replace('XXX',mzp_)
        linesh = linesh.replace('YYY',ma0_)
        fileshell.write(linesh)
    fileshell.close()
    os.system('chmod 777 '+shellfilename)
    tmpcmnd = 'bsub  -q 1nh '+' '+shellfilename+';'
    command =  tmpcmnd
    
    print command
    os.system(command)
    return 0



time=0
for mzp in range(800, 900, 50):
    for ma0 in range(300,1025,25):
        SubmitJobfunc( mzp, ma0)
        time = time + 1 
        #if (time%58) == 0:
            #os.system('sleep 600')
#SubmitJobfunc( 1000,300)
