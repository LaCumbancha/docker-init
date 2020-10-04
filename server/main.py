#!/usr/bin/env python3

import os
import time
import yaml
import logging
from common.server import Server


def parse_config_params():
	""" Parse env variables to find program config params

	Function that search and parse program configuration parameters in the
	program environment variables. If at least one of the config parameters
	is not found a KeyError exception is thrown. If a parameter could not
	be parsed, a ValueError is thrown. If parsing succeeded, the function
	returns a map with the env variables
	"""

	config_params = {}
	if "SERVER_CONFIG_FILE" in os.environ:
		try:
			config_file_name = os.environ["SERVER_CONFIG_FILE"]

			config_file = open(config_file_name)
			config_params = yaml.load(config_file, Loader=yaml.FullLoader)
		except FileNotFoundError as e:
			raise Exception(f"Config file {config_file_name} not found. Aborting server.")
		except yaml.MarkedYAMLError as e:
			raise Exception(f"Couldn't load config file {config_file_name}. Aborting server.")

	if "SERVER_PORT" in os.environ:
		config_params["port"] = int(os.environ["SERVER_PORT"])

	if "SERVER_LISTEN_BACKLOG" in os.environ:
		config_params["listen_backlog"] = int(os.environ["SERVER_LISTEN_BACKLOG"])

	"""Checking for missing variables."""
	if "port" not in config_params:
		raise Exception("Missing variable SERVER_PORT. Aborting server.")

	if "listen_backlog" not in config_params:
		raise Exception("Missing variable SERVER_LISTEN_BACKLOG. Aborting server.")

	return config_params

def main():
	initialize_log()
	config_params = parse_config_params()

	# Initialize server and start server loop
	server = Server(config_params["port"], config_params["listen_backlog"])
	server.run()

def initialize_log():
	"""
	Python custom logging initialization

	Current timestamp is added to be able to identify in docker
	compose logs the date when the log has arrived
	"""
	logging.basicConfig(
		format='%(asctime)s %(levelname)-8s %(message)s',
		level=logging.INFO,
		datefmt='%Y-%m-%d %H:%M:%S',
	)


if __name__== "__main__":
	main()
