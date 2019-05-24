# !/usr/bin/python
# Richard Givens
# CPSC 62800
# onecore.py program
# Code modified from the original text

import hashlib
import time
import sys
import os
import itertools



lowerCase   = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
upperCase   = ['G','H','I', 'J','K','L']
numbers     = ['0','1','2','3']
special     = ['!','@','#','$']

allCharacters = []
allCharacters = lowerCase + upperCase + numbers + special

# Commented out, unnecessary
#DIR = 'C:\Users\Rick\Desktop\VMShare\Week_7'

SALT = "&45Bvx9"


PW_LOW  = 2

# Value of 6 generates passwords of no greater than 5 digits
PW_HIGH = 6

#print os.getcwd()
#print 'Password string: ', allCharacters
print 'Password Lenthts: ', str(PW_LOW), ' - ', str(PW_HIGH-1)

# Mark the start time
startTime = time.time()

# Open a File for writing the results

try:
# Modified the original value since the file will be created in the current
# directory that the program is running in.
# Appended + to the w to create the file if it does not already exist, moved to
# the top so the file is created before the passwords are generated

    fp = open('PW-all.txt', 'w+')
except:
    print 'File Processing Error'
    sys.exit(0)

pwCount = 0

for r in range(PW_LOW, PW_HIGH):

# Cut out some of the code to make the file more efficient
    for s in itertools.product(allCharacters, repeat=r):

# Code modified from original
        pw =''.join(s)

        try:
            md5Hash = hashlib.md5()
            md5Hash.update(SALT+pw)
            md5Digest = md5Hash.hexdigest()

            fp.write(md5Digest + ' ' + pw + '\n')
            pwCount += 1
            del md5Hash
        except:
            print 'File Processing Error'

# Need to close the file if the module below does not fire
fp.close()

# When complete calculate the elapsed time
elapsedTime = time.time() - startTime
print 'Rainbow Table Generated'
print 'Elapsed Time: ', elapsedTime
print 'Hashes Generated: ', pwCount
print

# Function below tests the hashfile against sample values, and also will serve
# a template for the crackfile functionality. The function is called at the
# very bottom
#
# Killing two birds with one stone, if the sample works then I can co-opt the
# design into the crackfile.py program, coding should be the same.
if __name__ == "__main__":
# Tried playing around with importing the script below into another module,
# couldn't get it right, and removing the if name == statement could cause
# me to lose track of my indentations, so leaving it

    if len(sys.argv) == 1:
        rainbowTable = 'PW-all.txt'
        hashFile = 'shadow.txt'
    elif len(sys.argv)>=2:
        rainbowTable = sys.argv[1]
        hashFile = sys.argv[2]
    def foundYou():
        sampleTime = time.time()

# Open the file as read only
        try:
            fp = open (rainbowTable,'r')

            db = open(hashFile,'r')
            dbDict = {}
            usrDict = {}
            pwDict = {}

            for line in fp:
# Code modification, split the line on a space, remove any special characters
# Maybe unnecessary, but the shadow.txt file had newline characters,
# Duplicating here just to be safe
                pairs = line.strip().split(" ")
                pwDict.update({pairs[0]:pairs[1]})


            for line in db:
# Removing the newline characters and creating a split
                dbpairs = line.strip().split(':')
                dbDict.update(({dbpairs[0]:dbpairs[1]}))
# Reversing the key/value pairs to make the list easier to search, one thing I
# tried when having problems, and just never removed it
# When I got to something that worked, I stopped
                usrDict = dict([(value, key) for key, value in dbDict.items()])

            count = 0
# Probably a better way of doing this, but this is the first solution I
# came up with that worked
            for k, v in usrDict.iteritems():

                    searchValue = k
                    searchUser = v

                    for k, v in pwDict.iteritems():
                        targetValue = k
                        targetPW = v

                        if searchValue == targetValue:
                            count += 1
# After four hours of trying to get this to work, you really would not have
# liked what I had for a print statement before...
                            print str(searchUser) + '  '+ str(targetPW)
                            timeElapsed = time.time() - sampleTime

        except:
            print 'File Processing Error'

        print "%s Passwords recovered in %d seconds" % (count, timeElapsed)
        fp.close()
#--------------------------End of Function-------------------------------------
foundYou()
