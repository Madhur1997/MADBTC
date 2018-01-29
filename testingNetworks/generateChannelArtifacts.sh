#!/bin/bash

CHANNEL_NAME="mychannel"

which configtxgen
if [ "$?" -ne 0 ]; then
  echo "configtxgen tool not found. exiting"
  exit 1
fi

echo "##########################################################"
echo "#########  Generating Orderer Genesis block ##############"
echo "##########################################################"
configtxgen -profile ThreeOrgsOrdererGenesis -outputBlock ./channel-artifacts/genesis.block
if [ "$?" -ne 0 ]; then
  echo "Failed to generate orderer genesis block..."
  exit 1
fi
echo
echo "#################################################################"
echo "### Generating channel configuration transaction 'channel.tx' ###"
echo "#################################################################"
configtxgen -profile ThreeOrgsChannel -outputCreateChannelTx ./channel-artifacts/channel.tx -channelID $CHANNEL_NAME
if [ "$?" -ne 0 ]; then
  echo "Failed to generate channel configuration transaction..."
  exit 1
fi

echo
echo "#################################################################"
echo "#######    Generating anchor peer update for arjunMSP   #########"
echo "#################################################################"
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/arjunMSPanchors.tx -channelID $CHANNEL_NAME -asOrg arjunMSP
if [ "$?" -ne 0 ]; then
  echo "Failed to generate anchor peer update for arjunMSP..."
  exit 1
fi

echo
echo "#################################################################"
echo "#######    Generating anchor peer update for dharmeshMSP   ######"
echo "#################################################################"
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/dharmeshMSPanchors.tx -channelID $CHANNEL_NAME -asOrg dharmeshMSP
if [ "$?" -ne 0 ]; then
  echo "Failed to generate anchor peer update for dharmeshMSP..."
  exit 1
fi

echo
echo "#################################################################"
echo "#######    Generating anchor peer update for madhurMSP   ########"
echo "#################################################################"
configtxgen -profile ThreeOrgsChannel -outputAnchorPeersUpdate ./channel-artifacts/madhurMSPanchors.tx -channelID $CHANNEL_NAME -asOrg madhurMSP
if [ "$?" -ne 0 ]; then
  echo "Failed to generate anchor peer update for madhurMSP..."
  exit 1
fi
echo
