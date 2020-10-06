#!/bin/bash
# Say you have a command that fails rarely. In order to debug it you need to capture its output but it can be time 
# consuming to get a failure run. Write a bash script that runs the following script until it fails and captures its 
# standard output and error streams to files and prints everything at the end. Bonus points if you can also report 
# how many runs it took for the script to fail.

count=0
while true; do
    bash "./ex3_script.sh" >>"output.txt" 2>>"erros.txt"

    if [[ $? -ne 0 ]]; then
        echo "*** Results ***"
        cat "output.txt"
        echo "*** Error ***"
        cat "erros.txt"
        echo "*** Took $count times ***"
        break
    fi

    count=$((count + 1))
done
