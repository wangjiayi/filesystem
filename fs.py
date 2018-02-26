#here is the bianry fs object
import os,pickle
class Fsfile:

    def __init__(self,filename, onlyfilename, numberbyte):
        self.fullfilename = filename
        self.filename = onlyfilename
        self.numberbytes = numberbyte
        self.value = ""
        self.position = 0
        self.w_or_r = ""
        self.isopen = 0


class Dir:
    def __init__(self,dirname):
        self.dirname = dirname
        self.dirlist = []
        self.filelist = []
        self.parent = None


class Fs:

    def init(self,fsname):
        self.fsname = fsname
        self.nativefilesize = os.path.getsize(fsname)
        self.totalusedbyte = 0
        self.checknative = []
        for i in range(self.nativefilesize ):
            self.checknative.append(-1)
        self.root = Dir('root')
        self.position = self.root
        self.nativefile = open(fsname, 'r+b')
        self.isSuspend = 0
        self.openfnum = 0

    def mkdir(self, dirname):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        if len(dirname) == 0:
            print("wrong input")
        if dirname[0] == '/':
            self.position = self.root
            dirname = dirname[1:]
        targetDirList = dirname.split('/')
        for i in range(len(targetDirList)):
            if targetDirList[i] == '.':
                continue
            elif targetDirList[i] == '..':
                self.position = self.position.parent
            else:
                foundFlag = -1
                for j in range(len(self.position.dirlist)):
                    if targetDirList[i] == self.position.dirlist[j].dirname:
                        foundFlag = 1
                        self.position = self.position.dirlist[j]
                        if i == len(targetDirList) - 1:
                            print('path '+ dirname +" already exist")
                            self.position = curPos
                            return
                        break
                if foundFlag == -1:
                    if i == len(targetDirList) - 1:
                        self.position.dirlist.append(Dir(targetDirList[i]))
                        # add cur position object as parent dir
                        parent = self.position
                        self.position = self.position.dirlist[-1]
                        self.position.parent = parent
                    else:
                        print('path '+ targetDirList[i] +" is not exist under " + self.position.name)
                        self.position = curPos
                        return
        self.position = curPos

    def deldir(self,dirname):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        if len(dirname) == 0:
            print("can't find")
            return
        if dirname[0] == '/':
            self.position = self.root
            dirname = dirname[1:]
        if len(dirname) == 0:
            print("can't delete root")
            return
        targe = dirname.split('/')
        count = 0
        for i in range(len(targe)):
            if targe[i] == '.':
                continue
            elif targe[i] == '..':
                self.position = self.position.parent
            else:
                for j in range(len(self.position.dirlist)):
                    count += 1
                    if self.position.dirlist[j].dirname == targe[i]:
                        if i == len(targe)-1:
                            self.position.dirlist.remove(self.position.dirlist[j])
                            if curPos.dirname != targe[i]:
                                self.position = curPos
                            return
                        self.position = self.position.dirlist[j]
                        break

                if count == len(self.position.dirlist):
                    print("Dir " + targe[i] + " is not exist under /" + self.position.dirname)
                    return

    def isdir(self,dirname):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        if len(dirname) == 0:
            print("wrong input")
        if dirname[0] == '/':
            self.position = self.root
            dirname = dirname[1:]
        targetDirList = dirname.split('/')
        for i in range(len(targetDirList)):
            if targetDirList[i] == '.':
                continue
            elif targetDirList[i] == '..':
                self.position = self.position.parent
            else:
                foundFlag = -1
                for j in range(len(self.position.dirlist)):
                    if targetDirList[i] == self.position.dirlist[j].dirname:
                        foundFlag = 1
                        print("yes, this is dir")
                        self.position = self.position.dirlist[j]
                if foundFlag == -1:
                    print("no, this is not dir under the dir:" + self.position.dirname)
        self.position = curPos

    def chdir(self,dirname):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        if len(dirname) == 0:
            print("can't find")
            return
        if dirname[0] == '/':
            self.position = self.root
            dirname = dirname[1:]
        if len(dirname) == 0:
            return
        targe = dirname.split('/')
        count = 0
        for i in range(len(targe)):
            if targe[i] == '.':
                continue
            elif targe[i] == '..':
                self.position = self.position.parent
            else:
                for j in range(len(self.position.dirlist)):
                    count += 1
                    go = -1
                    if(self.position.dirlist[j].dirname == targe[i]):
                        self.position = self.position.dirlist[j]
                        go = 1
                        break
                if (count == len(self.position.dirlist) & go == -1):
                    print("Dir " + targe[i] + " is not exist under /" + self.position.dirname)
                    return
        print ('current location is ' + self.position.dirname)

    def listdir(self):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        result = ""
        while self.position.dirname != 'root':
            result = str(self.position.dirname) + '/' + result
            self.position = self.position.parent
        self.position = curPos
        return '/' + result

    def create(self,fullfilename,nbytes):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        filename = ''
        if '/' in fullfilename:
            pos = fullfilename.rfind('/')
            firstpos = fullfilename.find('/')
            if pos != firstpos:
                self.chdir(fullfilename[:pos])
                #becasue after the / is the file name not we want for the path of dir
            else:
                self.position = self.root
            filename = fullfilename[pos + 1:]
        if filename == '':
            filename = fullfilename
            fullfilename = '/' + filename

        if nbytes + self.totalusedbyte > self.nativefilesize:
            self.position = curPos
            print("no more space")
            return
        else:
            for i in range(len(self.position.filelist)):
                if(self.position.filelist[i].filename == filename):
                    self.position = curPos
                    print("the file "+filename+" is already exist under dir " + self.position.dirname)
                    return
            newfsFile = Fsfile(fullfilename, filename, nbytes)
            self.position.filelist.append(newfsFile)
            self.totalusedbyte += nbytes
            for i in range(self.nativefilesize):
                if self.checknative[i] == -1 and nbytes != 0:
                    self.checknative[i] = fullfilename
                    self.nativefile.seek(i)
                    self.nativefile.write(str.encode('\x00'))
                    nbytes -= 1
            #The bytes will be initialized to NULLs, i.e. all bits 0.
            print("the newly created file named "+filename+" is under dir " + self.position.dirname)
            self.position = curPos

    def open(self,fullfilename,mode):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        curPos = self.position
        filename = ''
        if '/' in fullfilename:
            pos = fullfilename.rfind('/')
            firstpos = fullfilename.find('/')
            if pos != firstpos:
                self.chdir(fullfilename[:pos])
            else:
                self.position = self.root
            filename = fullfilename[pos + 1:]
        if filename == '':
            filename = fullfilename

        for i in range(len(self.position.filelist)):
            if filename == str(self.position.filelist[i].filename):
                fd = self.position.filelist[i]
                if fd.isopen == 1:
                    self.position = curPos
                    print("file is opened, please close first")
                    return
                fd.isopen = 1
                fd.w_or_r = mode
                fd.position = 0
                self.position = curPos
                self.openfnum +=1
                return fd
        print("error, can't find the file")
        return

    def close(self,fd):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        fd.isopen = 0
        fd.r_or_w = ''
        self.openfnum -=1
        if self.openfnum < 0:
            self.openfnum =0
        print("closed")

    def length(self,fd):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        return len(fd.value)

    def pos(self,fd):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        return fd.position

    def seek(self,fd,pos):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        if pos < 0 or pos > len(fd.value):
            print("beyond the current length of the file")
            return
        fd.position = pos

    def read(self,fd,nbytes):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        if fd.w_or_r == 'r':
            endpos = fd.position + nbytes
            if endpos > len(fd.value):
                print("beyond the current length of the file")
                return
            result = fd.value[fd.position: endpos]
            fd.position = endpos
            return result
        else:
            print("Wrong mode, should be under read mode")
            return

    def write(self,fd,writebuf):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        if fd.w_or_r == 'w':
            if fd.value == '':
                fd.value = writebuf
                fd.position = len(writebuf) - 1
            else:
                preposvalue = fd.value[:fd.position]
                postposvalue = fd.value[fd.position:]
                fd.value = preposvalue + writebuf + postposvalue
                fd.position += len(writebuf)
            print("the value now in the file is:",fd.value)
            print("the pos is:", fd.position)
            if fd.value != '':
                j = 0
                for i in range(len(self.checknative)):
                    if self.checknative[i] == fd.fullfilename:
                        self.nativefile.seek(i)
                        writebuff = fd.value[j:j + 1]
                        if writebuff == "\\":
                            if fd.value[j:j + 2] == '\n':
                                writebuff = '\n'
                                j += 2
                        else:
                            j += 1
                        self.nativefile.write(str.encode(writebuff))
        else:
            print("Wrong mode, should be under write mode")
            return

    def readlines(self,fd):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        if fd.w_or_r == 'r':
            return fd.value.split('\n')
        else:
            print("Wrong mode, should be under read mode")
            return

    def delfile(self,filename):
        if self.isSuspend == 1:
            print("Currently suspend")
            return
        for i in range(len(self.position.filelist)):
            if filename == str(self.position.filelist[i].filename):
                self.position.filelist.pop(i)
                self.checknative[i] = -1 #change the checknaive to -1 then it can be wrriten agagin
        print("the file is delete")
        print("after delete, the filelist is :",self.position.filelist)

    def suspend(self):
        if self.isSuspend == 1:
            return
        if self.openfnum > 0:
            raise Exception("file is not closed")
        elif self.openfnum == 0:
            self.isSuspend = 1
            with open(self.fsname + '.fssave', 'wb') as output:
                pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)
            self = Fs()
            print ('suspension is complete')
        else:
            raise Exception("Negative open files")

    def resume(self):
        suspendFile = open(self.fsname + '.fssave', 'rb');
        tmp_dict = pickle.load(suspendFile).__dict__
        suspendFile.close()
        self.__dict__.update(tmp_dict)
        print ('resume is complete')
        self.isSuspend = 0

    def shutdown(self):
        self.nativefile.close()


fs = Fs()
fs.init('abc')
fs.mkdir('x')
fs.mkdir('x/xx')
fs.chdir('x/xx')
fs.mkdir('y')
# listdir = fs.listdir()
# print(listdir)
# fs.chdir('/x')
# fs.chdir('..')
# listdir = fs.listdir()
# print(listdir)



# fs.create('/x/a',3)
# fs.create('/b',3)
# fs.create('/c',10)
#
#
# writec = fs.open('/c', 'w')
# fs.write(writec, "kjv\ndefgh\n")
# fs.close(writec)
#
# readc = fs.open('/c', 'r')
# fs.seek(readc, 2)
# print(fs.read(readc, 5))
# print(fs.readlines(readc))
# fs.close(readc)
#
# fs.chdir('x')
# fs.mkdir('z')
# fs.chdir('z')
# fs.mkdir('z')
# fs.chdir('z')
# fs.deldir('../z')
# fs.mkdir('z')
# fs.chdir('z/z')
# fs.deldir('../../z')

# fs.suspend()
# fs.resume()
# fs.shutdown()