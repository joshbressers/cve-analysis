#!/bin/sh

FILES=`find data -name 'nvdcve*' -print`

# Load the NVD files
for i in $FILES
do
	echo "Loading JSON $i"
        ./json-parse.py $i
done

