#!/bin/bash

export PATH=${PWD}/../bin:${PWD}:$PATH
export FABRIC_CFG_PATH=${PWD}

which cryptogen
if [ "$?" -ne 0 ]; then
  echo "cryptogen tool not found. exiting"
  exit 1
fi
echo
echo "##########################################################"
echo "##### Generate certificates using cryptogen tool #########"
echo "##########################################################"

if [ -d "crypto-config" ]; then
  rm -rf crypto-config
fi
cryptogen generate --config=./crypto-config.yaml
if [ "$?" -ne 0 ]; then
  echo "Failed to generate certificates..."
  exit 1
fi
echo
