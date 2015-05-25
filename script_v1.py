#!/usr/bin/python2
import tempfile
import shutil
import re
import sys
import os,sys, subprocess

def SilentKiller(inputFSObj):
    try:
        os.remove(inputFSObj)
    except OSError:
        pass

def main():

    inputFile = sys.argv[1]
    inputVid = sys.argv[1]
    #inputFrameNum = str(sys.argv[2])
    inputNumFrames = "1"
    
    def ExtractFrame(inputMovie,inputFrameNum):    
    #'''  in -->  inputMovie, inputFrame
    #    returns >>  pathToJPG 
    #''' 
 
        def GetFramerate(inputMovie):
            pattern = re.compile(r'(\d{2}.\d{3}) fps')
            mplayerOutput = subprocess.Popen(["mplayer", "-identify", "-frames", "0", "o-ao", "null", inputMovie], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            fps = pattern.search(mplayerOutput).groups()[0]
            return fps 
        
        
        def CalculateFrameSec(inputFrameNumber,inputFPS):
            sec = float(inputFrameNumber)/float(inputFPS)
            return sec
        #
        #ffmpeg -ss 00:03:00 -i Underworld.Awakening.avi -frames:v 1 out1.jpg
        #newfile = tempfile.mkstemp(suffix=".jpg",dir='.')
        
        
        inputFPS = GetFramerate(inputMovie)
        inputSecond = CalculateFrameSec(inputFrameNum,inputFPS)
        #print inputSecond
        
        fileName, fileExtension = os.path.splitext(inputMovie)
        outputJPGName = fileName+"_"+str(inputFrameNum)+".jpg"
        
        SilentKiller(outputJPGName)
        
        output = subprocess.check_call(["ffmpeg","-ss",str(inputSecond),"-i",inputMovie,"-frames:v",str(inputNumFrames),outputJPGName])
        
        return outputJPGName
    #output = subprocess.check_output(["ffmpeg", "-i", inputFile, ], shell=True)
    
    inputFromALPR = os.path.splitext(inputFile)[0]+".txt"
    #inputFile = "day3_20150509"+".txt"
	
    iF = open(inputFromALPR,"r")
    iF.seek(0)
    next = 0
    oldLines = ""
    for lines in iF:
        if len(lines)> 465:
            frameNumber = oldLines.split(" ")
            print str(oldLines),frameNumber[1]
            print frameNumber[1]
            num = frameNumber[1].strip()
            #print num.isdigit()
            intFrameNum = int(num)
            ExtractFrame(inputVid, intFrameNum) 
            #print "     "+lines[10:30]
        else:
            oldLines = lines
        #if next == 1: 
        #    print lines
        #    next = 0
        #elif '''{"version":2,''' in lines:
        #    print lines
        #    next = 1
     
    
    #ExtractFrame(inputFile,inputFrameNum)    

if __name__ == '__main__':
    main()