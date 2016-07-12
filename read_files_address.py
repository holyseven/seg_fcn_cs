
import sys
import os

def parsearg():
    result = {}
    if len(sys.argv) < 2:
        print "-----------no arguments followed. "
        print "-----------So this script will list all dir and files in this directory."
        print "-----------And it will not write in a file."
    num = len(sys.argv)/2
    if len(sys.argv) % 2 == 0 and len(sys.argv)>=2:
        print "-----------error parsing the arguments."
        print "-----------use '-help 1' for more information."
        return result

    for i in range(num):
        if sys.argv[i*2+1] == '-r':#readdir
            result['-r'] = sys.argv[i*2+2]
        if sys.argv[i*2+1] == '-o':#outputfile
            result['-o'] = sys.argv[i*2+2]

    return result

def readfileaddr(thedir):
    return os.listdir(thedir)

def printdir(otpt, dirlist):
    if otpt == '':
        print "--------print into screen."
        print dirlist
    else: 
        print "--------write into " + otpt
        fileopt = open(otpt, 'w')
        for name in dirlist:
            fileopt.write(name + '\n')
        print "--------Done."
        fileopt.flush()
        fileopt.close()




arg = parsearg()
thedir = arg.get('-r', './')
dirlist = readfileaddr(thedir)
output = arg.get('-o', '')
fileoutput = open(output, 'w')
printdir('', dirlist)
dirlist.sort()
printdir('', dirlist)

# for UCF-101
# n = 0
# for name in dirlist:
    # filedir = thedir + '/' + name
    # filelist = readfileaddr(filedir)
    # for video in filelist:
        # fileoutput.write(filedir + '/' + video + ' ' + str(n) + '\n')
        # fileoutput.flush()
    # n = n + 1

# for cityscape image
for name in dirlist:
    filedir = thedir + '/' + name
    filelist = readfileaddr(filedir)
    filelist.sort()
    for image in filelist:
        fileoutput.write(filedir + '/' + image + '\n')
        fileoutput.flush()

fileoutput.close()
