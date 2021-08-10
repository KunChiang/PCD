#!/bin/bash
echo "start container:"
echo " image: $1, mount: $2"
dkr -ti -p 5000:5000 -v $2:/app/datas/root/ $1
