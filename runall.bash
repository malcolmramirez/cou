 #!/bin/bash

for entry in "programs"/*
do
    echo $entry
    python3 'cou.py' $entry
done
