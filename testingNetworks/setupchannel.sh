#!/bin/bash

# /bin/bash -c './scripts/script.sh ${CHANNEL_NAME} ${DELAY} ${LANG}; sleep $TIMEOUT'
# /bin/bash -c './scripts/script.sh TESTCHANNEL 3 golang;


COMPOSE_FILE=docker-compose-cli.yaml
COMPOSE_FILE_COUCH=docker-compose-couch.yaml

docker-compose -f $COMPOSE_FILE up -d 2>&1

if [ $? -ne 0 ]; then
  echo "ERROR !!!! Unable to start network"
  docker logs -f cli
  exit 1
fi
docker logs -f cli
