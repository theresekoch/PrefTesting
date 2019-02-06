
#TO EDIT-- 

#here, set what you want the stimuli to be

stimSetFolderA = '/home/pi/Desktop/ZF_testSongs/'
stimSetFolderB = '/home/pi/Desktop/ZF_test2/'

#set the ID of the bird being tested
testingBird = 'guineaPig'
#be sure you have created a folder called 'birdID' in home/pi.
#That folder is where all data will save. 

hoursUntilEnd = 8

#That's it! Please don't edit the rest of the code.
#
#
#
#
#
#
#
#
#
#
#
# import all necessary packages 
import os
import random
import time
from gpiozero import Button
import pygame
from datetime import datetime
from datetime import date
import sys

endOfDay = time.time()+ hoursUntilEnd*60*60
#this creates a file that will record all key pecks and their time stamps for this testing day
#it will do this in a new file called 'birdID_date'.
destinationFolder ='/home/pi/'+ testingBird + '/'
fileName = destinationFolder + testingBird + '_' + str(date.today()) 
fileVersion=0
fileNameWVersion = fileName + '.txt'

#this will check if the file already exists, and if it does, it will change the
    #name of the file to be created by adding a version number, so that no files
    #get overwritten if the program is run multiple times in the same day
while os.path.exists(fileNameWVersion):
    fileVersion= fileVersion+1
    fileNameWVersion = fileName + '_' + str(fileVersion) + '.txt'
dailyFile=open(fileNameWVersion, "w+")
dailyFile.write('version4  ' + str(datetime.now().time()) +'\n')

#This will create or add a new line to a file which lists which stimuli sets were tested each day.
stimuliFile = open(destinationFolder+ testingBird + '_ListofStimuli.txt', "a+")
stimuliFile.write(str(datetime.now()) + "   Stim set A = " + stimSetFolderA +
                  " Stim set B = " + stimSetFolderB + "\n")
stimuliFile.close()

#creates or opens an existing file to record the total number of string pulls
    #per stimulus set across the entire testing day, and initializes the counters. 
totalPullsFile = open(destinationFolder+testingBird+'_TotalStringPulls', 'a+')
stimSetACounter = 0
stimSetBCounter = 0



#this function dictates what will happen everytime a switch is pressed.
#it takes as input the folder for that switch and the corresponding list of songs
def keyPress(folder, songs, dailyFile):
    randSong = folder + random.choice(songs)
    print(randSong)
    s=pygame.mixer.Sound(randSong)
    s.play()
    dailyFile.write(str(datetime.now().time()) + '   ' + randSong + '\n')
        #This will get the song duration and pause the program for the duration
            ## of the song so that it can't play two at once
    songDuration= s.get_length()
    time.sleep(songDuration)
    return randSong;

def checkEnd(endOfDay, dailyFile, totalPullsFile):
    if time.time() > endOfDay:
        if not dailyFile.closed:
            dailyFile.write("The session could not be completed before lights out")
            dailyFile.close()  
        if not totalPullsFile.closed:
            totalPullsFile.close()
        sys.exit()
        

# This tell the pi which pins correspond to which switch
switch1 = Button(2)
switch2 = Button(4)



#this sets the initial folders which correspond to each button
stimSet1 = os.listdir(stimSetFolderA)
stimSet2 = os.listdir(stimSetFolderB)

#initialize sound mixer module
pygame.mixer.init()

side1= 0
side2 = 0
while side1<3 or side2<3:
    if switch1.is_pressed:
        keyPress(folder=stimSetFolderA, songs = stimSet1, dailyFile=dailyFile)
        side1=side1+1
        switch1.wait_for_release()
    if switch2.is_pressed:
        playedSong = keyPress(folder=stimSetFolderB, songs = stimSet2, dailyFile=dailyFile)
        side2=side2+1
        switch2.wait_for_release()
    checkEnd(endOfDay, dailyFile, totalPullsFile)
        

dailyFile.write('Min 3 per side reached  ' + str(datetime.now().time()) + '\n')

#this generates a time for when the sides should be automatically swapped by adding a
    #certain number of seconds to the current time when the program starts running.
    #for a 2 hour window, add 2*60*60
swapTime = time.time()+10

while time.time()< swapTime:
    if switch1.is_pressed:
        playedSong = keyPress(folder=stimSetFolderA, songs = stimSet1, dailyFile=dailyFile)
        stimSetACounter = stimSetACounter+1
        switch1.wait_for_release()
    if switch2.is_pressed:
        playedSong = keyPress(folder=stimSetFolderB, songs = stimSet2, dailyFile=dailyFile)
        stimSetBCounter = stimSetBCounter+1
        switch2.wait_for_release()
    checkEnd(endOfDay, dailyFile, totalPullsFile)
# After the swap, this sets the time when the program should end.


dailyFile.write("SIDE SWAP    " + str(datetime.now().time())+ '\n')

side1= 0
side2 = 0
while side1<3 or side2<3:
    if switch1.is_pressed:
        playedSong = keyPress(folder=stimSetFolderB, songs = stimSet2, dailyFile=dailyFile)
        side1=side1+1
        switch1.wait_for_release()
    if switch2.is_pressed:
        playedSong = keyPress(folder=stimSetFolderA, songs = stimSet1, dailyFile = dailyFile)
        side2=side2+1
        switch2.wait_for_release()
    checkEnd(endOfDay, dailyFile, totalPullsFile)

    
dailyFile.write('Min 3 per side reached  ' + str(datetime.now().time()) + '\n')

endTime = time.time()+10

while time.time() < endTime: 
    if switch1.is_pressed:
        playedSong=keyPress(folder=stimSetFolderB, songs = stimSet2, dailyFile = dailyFile)
        stimSetBCounter=stimSetBCounter+1
        switch1.wait_for_release()

    if switch2.is_pressed:
        playedSong=keyPress(folder= stimSetFolderA, songs = stimSet1, dailyFile = dailyFile)
        stimSetACounter = stimSetACounter+1
        switch2.wait_for_release()
    checkEnd(endOfDay, dailyFile, totalPullsFile)
         
totalPullsFile.write(str(datetime.now()) +' '+ stimSetFolderA + ': ' + str(stimSetACounter)
                     + '  ' + stimSetFolderB + ': ' + str(stimSetBCounter) +' \n')

totalPullsFile.close()

if not dailyFile.closed:
    dailyFile.close()  



