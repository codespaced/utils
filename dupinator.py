## {{{ http://code.activestate.com/recipes/362459/ (r1)
#! /usr/bin/python

import os
import sys
import stat
import hashlib
import time
from send2trash import send2trash
# send2trash('some_file')

filesBySize = {}
txt = ""

def walker(arg, dirname, fnames):
    d = os.getcwd()
    os.chdir(dirname)
    try:
        fnames.remove('Thumbs')
#        send2trash('Thumbs')
    except ValueError:
        pass
    for f in fnames:
        if not os.path.isfile(f) or "$" in f or "recycle" in f.lower():
            continue
        size = os.stat(f)[stat.ST_SIZE]
        if size < 100:
            continue
        if filesBySize.has_key(size):
            a = filesBySize[size]
        else:
            a = []
            filesBySize[size] = a
        a.append(os.path.join(dirname, f))
    os.chdir(d)

if len(sys.argv) < 2:
    args = ["."]
else:
    args = sys.argv[1:]
for x in args:
    print 'Scanning directory "%s"' % x
    #txt += 'Scanning directory "%s"....\n' % x
    os.path.walk(x, walker, filesBySize)

print 'Finding potential dupes...'
txt += 'Finding potential dupes...\n'
potentialDupes = []
potentialCount = 0
trueType = type(True)
sizes = filesBySize.keys()
sizes.sort()
for k in sizes:
    inFiles = filesBySize[k]
    outFiles = []
    hashes = {}
    if len(inFiles) is 1: continue
    #print 'Testing %d files of size %d...' % (len(inFiles), k)
    #txt += 'Testing %d files of size %d...\n' % (len(inFiles), k)
    print ".",
    for fileName in inFiles:
        if not os.path.isfile(fileName):
            continue
        try:
            aFile = file(fileName, 'r')
        except:
            print "Unable to open %s" % fileName
            continue
        hasher = hashlib.md5(aFile.read(1024))
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            x = hashes[hashValue]
            if type(x) is not trueType:
                outFiles.append(hashes[hashValue])
                hashes[hashValue] = True
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
        aFile.close()
    if len(outFiles):
        potentialDupes.append(outFiles)
        potentialCount = potentialCount + len(outFiles)
print ""
del filesBySize

if potentialCount == 0:
    print 'No potential dupes.'
    #txt += 'No potential dupes.\n'
else:
    print 'Found %d sets of potential dupes...' % potentialCount
    #txt += 'Found %d sets of potential dupes...\n' % potentialCount
    print 'Scanning for real dupes...'
    #txt += 'Scanning for real dupes...\n'

dupes = []
for aSet in potentialDupes:
    outFiles = []
    hashes = {}
    for fileName in aSet:
        #print 'Scanning file "%s"...' % fileName
        #txt += 'Scanning file "%s"...\n' % fileName
        #print ".",
        aFile = file(fileName, 'r')
        hasher = hashlib.md5()
        while True:
            r = aFile.read(4096)
            if not len(r):
                break
            hasher.update(r)
        aFile.close()
        hashValue = hasher.digest()
        if hashes.has_key(hashValue):
            if not len(outFiles):
                outFiles.append(hashes[hashValue])
            outFiles.append(fileName)
        else:
            hashes[hashValue] = fileName
    if len(outFiles):
        dupes.append(outFiles)

i = 0

cmp=(lambda x,y: int(os.path.getmtime(x)-os.path.getmtime(y)))

for d in dupes:
    #print "last modified: %s" % time.ctime(os.path.getmtime(file))
    #print "created: %s" % time.ctime(os.path.getctime(file))

    d.sort(cmp=cmp)

    print 'Original: %s (%s)' % (d[0], time.ctime(os.path.getmtime(d[0])))
    txt += '\nOriginal: %s (%s)\n' % (d[0], time.ctime(os.path.getmtime(d[0])))
    print "Deleting ..."
    for f in d[1:]:
        i = i + 1
        txt += '%s (%s)\n' % (f, time.ctime(os.path.getmtime(f)))
        print  '%s (%s)' % (f, time.ctime(os.path.getmtime(f)))
        send2trash(f)
#        os.remove(f)
    print
    txt += '\n'

with open("deletionlog.txt", 'a') as delog:
    delog.write(txt)
## end of http://code.activestate.com/recipes/362459/ }}}
