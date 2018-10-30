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

	logger.info("==============================")
	logger.info("== NSUT creates a wallet  ==")
	logger.info("------------------------------")

	NSUT_wallet_config = json.dumps({"id": "NSUT_wallet"})
	NSUT_wallet_credentials = json.dumps({"key": "NSUT_wallet_key"})

	try:
		await wallet.create_wallet(NSUT_wallet_config, NSUT_wallet_credentials)
	except IndyError as ex:
		if ex.error_code == ErrorCode.WalletAlreadyExistsError:
	    		pass
	NSUT_wallet = await wallet.open_wallet(NSUT_wallet_config, NSUT_wallet_credentials)

	logger.info("\"NSUT\" -> Create and store in Wallet \"NSUT-Steward DID\" ")
	(NSUT_steward_did, NSUT_steward_key) = await did.create_and_store_my_did(NSUT_wallet, "{}")

	logger.info("\"NSUT\" -> Get key for did from \"Steward\" connection request")

	fname = "connectionReqStewardNSUT.txt"
	with open(fname,'r') as f:
		connection_request = eval(f.readline())
	
	steward_NSUT_verkey = await did.key_for_did(pool_handle, NSUT_wallet, connection_request['did'])

	logger.info("\"NSUT\" -> Anoncrypt connection response for \"Steward\" with \"NSUT-Steward\" DID, verkey and nonce")

	'''connection_response = json.dumps({
	'did': NSUT_steward_did,
	'verkey': NSUT_steward_key,
	'nonce': connection_request['nonce']
	})'''


	anoncrypted_connection_response = {
	'did': NSUT_steward_did,
	'verkey': NSUT_steward_key,
	'nonce': connection_request['nonce']
	}

	#anoncrypted_connection_response = await crypto.anon_crypt(steward_NSUT_verkey, connection_response.encode('utf-8'))

	logger.info("\"NSUT\" -> Send anoncrypted connection response to \"Steward")
	fname = "connectionRespNSUTSteward.txt"
	with open(fname,'w') as f:
		f.write(str(anoncrypted_connection_response))
if __name__ == '__main__':
	run_coroutine(run)
	time.sleep(1)  
