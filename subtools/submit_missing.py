import sys, os

#the errfiles.txt should be the result of this command:
# grep "Error" */*.err >errfiles.txt
inname = "errfiles.txt" #"missing_files.txt"

infile = open(inname, "r")

old_jdl = ""
for line in infile:
    words = line.strip().split("/")
    direc = words[0]
    parts = words[1].split(".")[0].split("_")

    num = parts[-1]
    name = ""
    i = 0
    while i < len(parts)-1:
        name += parts[i]
        if i != len(parts)-2:
            name += "_"
        i += 1
    

    jdl = "{0:s}_{1:s}.jdl".format(name, num)
#    print(name)
    #don't submit the job a 2nd time if it had 2 lines of errors.
    if jdl == old_jdl:
        continue
    print(jdl)
    os.system("cd {0:s}; condor_submit {1:s}; cd ..".format(name, jdl))
    old_jdl = jdl


