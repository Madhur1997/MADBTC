import time

from indy import anoncreds, crypto, did, ledger, pool, wallet

import json
import logging
import ast
from typing import Optional

from indy.error import ErrorCode, IndyError

from src.utils import get_pool_genesis_txn_path, run_coroutine, PROTOCOL_VERSION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def run():
    print("\n")
    logger.info(" Getting Started\n")
    

    logger.info(" \"Sovrin Steward\" -> Connecting to the started indy pool \n")
    pool_name = 'pool1'
    logger.info(" Open Pool Ledger: {}".format(pool_name))
    pool_genesis_txn_path = get_pool_genesis_txn_path(pool_name)
    pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})
    

    # Set protocol version 2 to work with Indy Node 1.4
    await pool.set_protocol_version(PROTOCOL_VERSION)

    try:
        await pool.create_pool_ledger_config(pool_name, pool_config)
    except IndyError as ex:
        if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
            pass
    pool_handle = await pool.open_pool_ledger(pool_name, None)


    logger.info(" \"Sovrin Steward\" -> Creating wallet to store its credentials\n")
    steward_wallet_config = json.dumps({"id": "sovrin_steward_wallet"})
    steward_wallet_credentials = json.dumps({"key": "steward_wallet_key"})
    try:
        await wallet.create_wallet(steward_wallet_config, steward_wallet_credentials)
    except IndyError as ex:
        if ex.error_code == ErrorCode.WalletAlreadyExistsError:
            pass

    logger.info(" \"Sovrin Steward\" -> Opening Steward wallet \n")
    steward_wallet = await wallet.open_wallet(steward_wallet_config, steward_wallet_credentials)

    logger.info(" \"Sovrin Steward\" -> Creates and stores the DID in the wallet using the intital seed values\n\n")
    steward_did_info = {'seed': '000000000000000000000000Steward1'}
    (steward_did, steward_key) = await did.create_and_store_my_did(steward_wallet, json.dumps(steward_did_info))
    

    fname = "stewardDID.txt"
    with open(fname, 'w') as f:
    	f.write(steward_did)
    
       
	

if __name__ == '__main__':
    run_coroutine(run)
    time.sleep(1)  
