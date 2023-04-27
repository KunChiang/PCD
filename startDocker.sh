#!/bin/bash
echo "start container:"
echo " image: $1, mount: $2"
docker run -d -p 5000:5000 --name pcd --restart always -v $2:/app/data/root/ $1
