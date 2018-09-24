#!/bin/bash

# generate the certificates for the organizations using cryptogen
/bin/bash ./generateKeys.sh

# copy the necessary keys into the correct folders
/bin/bash ./insertKeys.sh

# generate channel artifacts
# genesis block
# channel configuration transaction
# anchor peer transactions
/bin/bash ./generateChannelArtifacts.sh

# start the containers by spinning up docker-cli container which establishes the network
/bin/bash ./setupchannel.sh
