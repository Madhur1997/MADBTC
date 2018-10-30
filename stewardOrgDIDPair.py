import time

from indy import anoncreds, crypto, did, ledger, pool, wallet

import json
import logging
from typing import Optional

from indy.error import ErrorCode, IndyError

from src.utils import get_pool_genesis_txn_path, run_coroutine, PROTOCOL_VERSION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def run():

	pool_name = 'pool1'
	pool_genesis_txn_path = get_pool_genesis_txn_path(pool_name)
	pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})


	# Set protocol version 2 NSUT work with Indy Node 1.4
	await pool.set_protocol_version(PROTOCOL_VERSION)

	try:
		await pool.create_pool_ledger_config(pool_name, pool_config)
	except IndyError as ex:
		if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
	    		pass
	pool_handle = await pool.open_pool_ledger(pool_name, None)

	steward_wallet_config = json.dumps({"id": "sovrin_steward_wallet"})
	steward_wallet_credentials = json.dumps({"key": "steward_wallet_key"})

	steward_wallet = await wallet.open_wallet(steward_wallet_config, steward_wallet_credentials)

	fname = "stewardDID.txt"
	with open(fname,'r') as f:
		steward_did = f.readline()

	logger.info("\"Steward\" -> Create and store in Wallet \"Steward-NSUT\" DID")
	(steward_NSUT_did, steward_NSUT_key) = await did.create_and_store_my_did(steward_wallet, "{}")

	logger.info("\"Steward\" -> Send Nym to Ledger for \"Steward-NSUT\" DID")
	await send_nym(pool_handle, steward_wallet, steward_did, steward_NSUT_did, steward_NSUT_key, None)

	logger.info("\"Steward\" -> Send connection request to NSUT with \"Steward-NSUT\" DID and nonce")
	connection_request = {
	'did': steward_NSUT_did,
	'nonce': 123456789
	} 

	fname = "connectionReqStewardNSUT.txt"
	with open(fname,'w') as f:
		f.write(str(connection_request))
	fname = "stewardNSUTDIDPair.txt" 
	with open(fname,'w') as f:
		f.write(steward_NSUT_did)


async def send_nym(pool_handle, wallet_handle, _did, new_did, new_key, role):
    	nym_request = await ledger.build_nym_request(_did, new_did, new_key, None, role)
    	await ledger.sign_and_submit_request(pool_handle, wallet_handle, _did, nym_request)

if __name__ == '__main__':
	run_coroutine(run)
	time.sleep(1)  # FIXME waiting for libindy thread complete
