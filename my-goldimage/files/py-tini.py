#!/bin/env python3

import datetime
import hashlib
import json
import logging
import os
import re
import sys
import time

import dotenv
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def obfs_val(data):
    try:
        result = hashlib.sha256(data.encode('utf-8')).hexdigest()
    except AttributeError:
        result = None
    else:
        result = result[:8]

    return result


def json_dump(data):
    return json.dumps(data, sort_keys=True,
                            default=lambda obj: obj.isoformat() if isinstance(obj, (datetime.datetime, datetime.date)) else str(obj))


def sync_env(endpoint=None, token=None, block=None, ssl_verify=None):
    dotenv_file = dotenv.find_dotenv(usecwd=True)

    if dotenv_file:
        # Local .env file overrides global env
        if dotenv.load_dotenv(dotenv_path=dotenv_file, override=True):
            logger.debug(f"Updated env from '{dotenv_file}'")
        else:
            logger.warning(f"Could not update env from '{dotenv_file}'")
    else:
        logger.warning("Couldn't find or parse a dotenv file, but I was asked to read one")

    new_env = dict(os.environ)

    if endpoint and token:
        if block is None:
            block = False

        if ssl_verify is None:
            ssl_verify = True

        while True:
            try:
                remote_env_request = requests.get(f"{endpoint}/v1/env", params={"token": token}, timeout=5, verify=ssl_verify)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                if block:
                    logger.warning("Request timed out, or refused. Retrying.")
            else:
                if remote_env_request.ok:
                    remote_env = remote_env_request.json()
                    obfuscated_vals = {key: obfs_val(val) for key, val in remote_env.items()}

                    logger.info(f"Remote env received. Updating environment. Contents (obfuscated): {json_dump(obfuscated_vals)}")

                    new_env.update(remote_env)

                    break
                else:
                    if block:
                        logger.warning(f"Remote endpoint {endpoint} returned a problem: {remote_env_request.reason}. Retrying.")
                    else:
                        break

            time.sleep(5)

    return new_env


if __name__ == "__main__":
    cmdargs = list()
    cmdargs.append("--")
    cmdargs.extend([sys.argv[1], '--'])
    cmdargs.extend(sys.argv[2:])

    env_endpoint = os.environ.get("ENV_ENDPOINT")
    env_token = os.environ.get("ENV_TOKEN")
    env_block = os.environ.get("ENV_BLOCK", "").lower() == "true"
    env_ssl_verify = os.environ.get("ENV_SSL_VERIFY", "").lower() == "true"

    env = sync_env(endpoint=env_endpoint, token=env_token, block=env_block, ssl_verify=env_ssl_verify)

    logger.info(f"Running '/usr/bin/tini' with args: {cmdargs}")
    os.execvpe("/usr/bin/tini", args=cmdargs, env=env)

