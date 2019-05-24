# !/usr/bin/python

# Richard Givens
# 05/24/2019

# This program will read the contents of two files into seperate dictionaries,
# search for the keys that exist in both dictionaries, and return the
# corresponding values.

# The original intent of this program is to use an exfiltrated user database
# file containing usernames and hashed passwords, and comparing them to a
# pregenerated rainbow table.
import time, sys, itertools

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
