import os, signal, sys

def interrupt(obj0, obj1):
    print("lkdjfdlkjfldkjflkdjflkdjflkdjflkdjflkdjflkdjlkfjdlkfjdlkfjlkdjflkdjflkdjflkdjflkdjfk")
    sys.exit()
nfiles = 5 #number of files per job
#get name of .jdl files
cwd = os.getcwd()
print("cwd: %s"%cwd)
words = cwd.split("/")
name = words[len(words)-1]
#get rid of the year at the end of the directory name
#words = name.split("_")
#name = "_".join(words[:len(words)-1])
print("name: %s"%(name))
#for i in range(1, 1210, 5):
i = 1
signal.signal(signal.SIGINT, interrupt)
while True:
    s = str(i).zfill(3)
    print("file: %s_%s.jdl"%(name, s))
    if not os.path.exists("%s_%s.jdl"%(name, s)):
        lastj = i - nfiles
        print("last job: %d"%(lastj))
        break
    #print(s)
    #print("condor_submit SingleMuon_Run2017F_31Mar2018_v1_NanoAODv5_%s.jdl"%(s))
    os.system("condor_submit %s_%s.jdl"%(name, s))
    i += nfiles
