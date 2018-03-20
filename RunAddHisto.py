import sys
import os 
for imass in open("zpbaryonicMass_private.txt"):
#for imass in open("zpbaryonicMass_official.txt"):
    masses = imass.rstrip().split(" ")
    print masses[0], masses[1]
    torun = 'root -l -b -q AddRooDataHist.C\\(\\"'+masses[0]+'\\",\\"'+masses[1]+'\\"\\)'
    print torun
    os.system(torun)
