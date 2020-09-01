 #!/bin/bash

for entry in "test"/*
do
    echo $entry
    python3 'cou.py' $entry
done
