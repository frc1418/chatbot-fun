#!/bin/bash

case "$OSTYPE" in
    darwin*)

        # Volume container, don't destroy this or your data goes away
        # - Only necessary on OSX
        docker create --name openfire-volume --entrypoint=/bin/true -v /var/lib/openfire sameersbn/openfire

        VOL="--volumes-from openfire-volume"

        ;;

    *)
        HERE=`pwd`
        VOL="--volume $HERE/config:/var/lib/openfire"
        ;;
esac

docker run --name openfire -d --restart=always \
  -h `hostname` $VOL \
  --publish 9090:9090 --publish 5222:5222 --publish 7777:7777 \
  sameersbn/openfire
