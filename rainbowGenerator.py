# !/usr/bin/python
# Richard Givens
# 05/24/2019
# Code modified from Python Forensics by Chet Hosmer, Chapter 10, pages 280 - 283

import hashlib
import time
import sys
import os
import itertools


# Modify these values as necessary to create larger, and more complex tables

lowerCase   = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
upperCase   = ['G','H','I', 'J','K','L']
numbers     = ['0','1','2','3']
special     = ['!','@','#','$']

allCharacters = []
allCharacters = lowerCase + upperCase + numbers + special
# Hard coded salt utilized in the PW-all file provied, change as necessary
SALT = "&45Bvx9"

# Modify these values to suit your use case
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

# This is the original function for the crackfile.py program.
if __name__ == "__main__":

# Reads sys args and sets the variables if present, if sys args are not entered
# the application will rely on hardcoded values for the variables
    if len(sys.argv) == 1:
# the rainbowTable file represents a pregenerated file in which the hash value
# is listed first, and the password second
# Example: 1f5b6d6065ab46634ba71e8f656f4f3d He#a0

        rainbowTable = 'PW-all.txt'
# the hashFile represents an exfiltrated user database file
# in which the username is listed first, and the hashed password second
# Example: plato:73cd7520e0d5ab04fb196ba97a499de3
        hashFile = 'shadow.txt'

    elif len(sys.argv)>=2:
        rainbowTable = sys.argv[1]
        hashFile = sys.argv[2]

    def foundYou():
        sampleTime = time.time()

        try:
            fp = open (rainbowTable,'r')
            db = open(hashFile,'r')
            dbDict = {}
            usrDict = {}
            pwDict = {}

            for line in fp:
# The rainbowTable file is split and stripped on all newline and non-printable
# characters, the contents are then read into a dictionary
                pairs = line.strip().split(" ")
                pwDict.update({pairs[0]:pairs[1]})

            for line in db:
# Same split and strip operations as rainbowTable, contents then read into a
# dictionary
                dbpairs = line.strip().split(':')
                dbDict.update(({dbpairs[0]:dbpairs[1]}))
# The key value pairs in dbDict are swapped, creating the usrDict in which the
# hashed password is the key and the user is the value.
# This allows the two dictonaries to be compared key for key
                usrDict = dict([(value, key) for key, value in dbDict.items()])

# Setting the counter for benchmarking purposes
            count = 0
# The function searches pwDict for the key in usrDict, and if found returns the
# values for both dictionaries.
# Idea for code improvement is to create a new file and append the results
            for k,v in usrDict.iteritems():
                searchValue = k
                searchUser = v
                if pwDict.has_key(k):
                    targetPW = pwDict.get(k)
                    count += 1
                    print searchUser + '  '+ str(targetPW)
                    timeElapsed = time.time() - sampleTime

        except:
            print 'File Processing Error'

        print "%s Passwords recovered in %d seconds" % (count, timeElapsed)
        fp.close()
#--------------------------End of Function-------------------------------------
foundYou()
