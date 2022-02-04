#!/usr/bin/bash 

year=2017
#get name of current directory (will be same name for eos).
name=${PWD##*/}
echo $name
for f in `ls *.root`
do
    eos root://cmseos.fnal.gov ls /store/user/bgreenbe/haa_4tau_${year}/$name/$f
    #if ls was successful then the file is already there.
    if [ $? == 0 ]
    then
        echo "$f is there my dude. Removing it from here."
        rm $f
    else
        echo "Copying $f"
        xrdcp $f root://cmseos.fnal.gov//store/user/bgreenbe/haa_4tau_${year}/$name/
        if [ $? == 0 ]
        then
            echo "Success! Removing $f."
            rm $f
        fi
    fi
done
