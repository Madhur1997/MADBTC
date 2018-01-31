#!/bin/bash

CHANNEL_NAME="mychannel"

# setting up a channel
peer channel create -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/channel.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Environment variables for PEER0 arjun: needed for joining the channel
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/arjun.example.com/users/Admin@arjun.example.com/msp
CORE_PEER_ADDRESS=peer0.arjun.example.com:7051
CORE_PEER_LOCALMSPID="arjunMSP"
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/arjun.example.com/peers/peer0.arjun.example.com/tls/ca.crt

# command to make a peer join a channel
peer channel join -b mychannel.block

# updating the channel
peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/arjunMSPanchors.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# Environment variables for PEER0 dharmesh : needed for joining the channel
CORE_PEER_MSPCONFIGPATH=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/dharmesh.example.com/users/Admin@dharmesh.example.com/msp
CORE_PEER_ADDRESS=peer0.dharmesh.example.com:7051
CORE_PEER_LOCALMSPID="dharmeshMSP"
CORE_PEER_TLS_ROOTCERT_FILE=/opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/peerOrganizations/dharmesh.example.com/peers/peer0.dharmesh.example.com/tls/ca.crt

# command to make a peer join a channel
peer channel join -b mychannel.block

# updating the channel
peer channel update -o orderer.example.com:7050 -c $CHANNEL_NAME -f ./channel-artifacts/dharmeshMSPanchors.tx --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem

# install the Go chaincode
# peer chaincode install -n mycc -v 1.0 -p github.com/chaincode/chaincode_example02/go/

# instantiate the chaincode
# peer chaincode instantiate -o orderer.example.com:7050 --tls --cafile /opt/gopath/src/github.com/hyperledger/fabric/peer/crypto/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C $CHANNEL_NAME -n mycc -l node -v 1.0 -c '{"Args":["init","a", "100", "b","200"]}' -P "OR ('arjunMSP.member','dharmeshMSP.member')"

# query the chaincode
# peer chaincode query -C $CHANNEL_NAME -n mycc -c '{"Args":["query","a"]}'
