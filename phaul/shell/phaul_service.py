#!/usr/bin/env python

import logging
import signal
import sys

import phaul.args_parser
import phaul.connection
import phaul.service
import phaul.util
import phaul.xem_rpc


class Fin(object):

	def __init__(self, stop_fd):
		self.stop_fd = stop_fd

	def __call__(self, signum, frame):
		logging.info("Stop by %d", signum)
		self.stop_fd.close()


def main():
	# Parse arguments
	args = phaul.args_parser.parse_service_args()

	# Configure logging
	logging.basicConfig(filename=args.log_file, filemode="a", level=logging.INFO,
		format="%(asctime)s.%(msecs)03d: %(process)d: %(message)s",
		datefmt="%H:%M:%S")

	# Setup hook to log uncaught exceptions
	sys.excepthook = phaul.util.log_uncaught_exception

	phaul.util.log_header()
	logging.info("Starting p.haul service")

	# Establish connection
	connection = phaul.connection.establish(args.fdrpc, args.fdmem, args.fdfs)

	t = phaul.xem_rpc.rpc_threaded_srv(phaul.service.phaul_service, connection)

	# FIXME: Setup stop handlers
	stop_fd = t.init_stop_fd()
	fin = Fin(stop_fd)
	signal.signal(signal.SIGTERM, fin)
	signal.signal(signal.SIGINT, fin)

	t.start()
	signal.pause()
	t.join()
	logging.info("Bye!")

	# Close connection
	connection.close()

if __name__ == "__main__":
	main()
