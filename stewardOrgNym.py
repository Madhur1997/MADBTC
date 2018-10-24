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

	steward_wallet_config = json.dumps({"id": "sovrin_steward_wallet"})
	steward_wallet_credentials = json.dumps({"key": "steward_wallet_key"})
	steward_wallet = await wallet.open_wallet(steward_wallet_config, steward_wallet_credentials)

	fname = "connectionRespOrgSteward.bin"
	with open(fname,'rb') as f:
		anoncrypted_connection_response = f.read()

	#print(anoncrypted_connection_response)

	logger.info("\"Steward\" -> Anondecrypt connection response from \"Organization\"")

	fname = "stewardOrgDIDPair.txt"
	with open(fname,'r') as f:
		steward_organization_did = f.readline()

	steward_organization_key = did.key_for_did(pool_handle, steward_wallet, steward_organization_did )
	decrypted_connection_response = \
        json.loads((await crypto.anon_decrypt(steward_wallet, steward_organization_key,
                                              anoncrypted_connection_response)).decode("utf-8"))

	fname = "connectionReqStewardOrganization.txt"
	with open(fname,'r') as f:
		connection_request = eval(f.readline())

	logger.info("\"Steward\" -> Authenticates \"Organization\" by comparision of Nonce")
	assert connection_request['nonce'] == decrypted_connection_response['nonce']

	fname = "stewardDID.txt"
	with open(fname,'r') as f:
		steward_did = f.readline()

	logger.info("\"Steward\" -> Send Nym to Ledger for \"Organization Steward\" DID")
	await send_nym(pool_handle, steward_wallet, steward_did, organization_steward_did, organization_steward_key, None)


async def send_nym(pool_handle, wallet_handle, _did, new_did, new_key, role):
	nym_request = await ledger.build_nym_request(_did, new_did, new_key, None, role)
	await ledger.sign_and_submit_request(pool_handle, wallet_handle, _did, nym_request)

if __name__ == '__main__':
	run_coroutine(run)
	time.sleep(1)  
