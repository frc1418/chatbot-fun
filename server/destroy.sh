#!/bin/bash

docker stop openfire
docker rm openfire

# destroys your data too, on OSX
#docker rm openfire-volume