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
	logger.info("Getting started -> started")

	pool_name = 'pool1'
	logger.info("Open Pool Ledger: {}".format(pool_name))
	pool_genesis_txn_path = get_pool_genesis_txn_path(pool_name)
	#print(pool_genesis_txn_path)
	pool_config = json.dumps({"genesis_txn": str(pool_genesis_txn_path)})
	#print(pool_config)


	# Set protocol version 2 organization work with Indy Node 1.4
	await pool.set_protocol_version(PROTOCOL_VERSION)

	try:
		await pool.create_pool_ledger_config(pool_name, pool_config)
	except IndyError as ex:
		if ex.error_code == ErrorCode.PoolLedgerConfigAlreadyExistsError:
	    		pass
	pool_handle = await pool.open_pool_ledger(pool_name, None)

	logger.info("==============================")
	logger.info("== Organization gets the wallet  ==")
	logger.info("------------------------------")

	organization_wallet_config = json.dumps({"id": "organization_wallet"})
	organization_wallet_credentials = json.dumps({"key": "organization_wallet_key"})

	try:
		await wallet.create_wallet(organization_wallet_config, organization_wallet_credentials)
	except IndyError as ex:
		if ex.error_code == ErrorCode.WalletAlreadyExistsError:
	    		pass
	organization_wallet = await wallet.open_wallet(organization_wallet_config, organization_wallet_credentials)

	logger.info("\"Organization\" -> Create and store in Wallet \"Organization Steward\" ")
	(organization_steward_did, organization_steward_key) = await did.create_and_store_my_did(organization_wallet, "{}")

	logger.info("\"Organization\" -> Get key for did from \"Steward\" connection request")

	fname = "connectionReqStewardOrg.txt"
	with open(fname,'r') as f:
		connection_request = eval(f.readline())
	print(connection_request)
	steward_organization_verkey = await did.key_for_did(pool_handle, organization_wallet, connection_request['did'])

	logger.info("\"Organization\" -> Anoncrypt connection response for \"Steward\" with \"Organization Steward\" DID, verkey and nonce")

	connection_response = json.dumps({
	'did': organization_steward_did,
	'verkey': organization_steward_key,
	'nonce': connection_request['nonce']
	})

	anoncrypted_connection_response = await crypto.anon_crypt(steward_organization_verkey, connection_response.encode('utf-8'))

	logger.info("\"Organization\" -> Send anoncrypted connection response to \"Steward")
	fname = "connectionRespOrgSteward.bin"
	#print(anoncrypted_connection_response)
	with open(fname,'wb') as f:
		f.write(anoncrypted_connection_response)
if __name__ == '__main__':
	run_coroutine(run)
	time.sleep(1)  
