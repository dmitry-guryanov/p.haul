#
# CRIU API
# Includes class to work with CRIU service and helpers
#

import socket
import os
import subprocess
import logging
import util
import pycriu
import criu_req

criu_binary = "criu"

cpuinfo_img_name = "cpuinfo.img"

def_verb = 2

#
# Connection to CRIU service
#

class criu_conn:
	def __init__(self, mem_sk):
		self._iter = 0
		self.verb = def_verb
		css = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
		util.set_cloexec(css[1])
		logging.info("`- Passing (ctl:%d, data:%d) pair to CRIU", css[0].fileno(), mem_sk.fileno())
		self._swrk = subprocess.Popen([criu_binary, "swrk", "%d" % css[0].fileno()])
		css[0].close()
		self._cs = css[1]
		self._last_req = -1
		self._mem_fd = mem_sk.fileno()

	def close(self):
		self._cs.close()
		self._swrk.wait()

	def mem_sk_fileno(self):
		return self._mem_fd

	def verbose(self, level):
		self.verb = level

	def _recv_resp(self):
		resp = pycriu.rpc.criu_resp()
		resp.ParseFromString(self._cs.recv(1024))
		if not resp.type in (pycriu.rpc.NOTIFY, self._last_req):
			raise Exception("CRIU RPC error (%d/%d)" % (resp.type, self._last_req))

		return resp

	def send_req(self, req):
		req.opts.log_level = self.verb
		req.opts.log_file = self.get_log_name(req.type)
		self._cs.send(req.SerializeToString())
		self._iter += 1
		self._last_req = req.type

		return self._recv_resp()

	def ack_notify(self, success = True):
		req = pycriu.rpc.criu_req()
		req.type = pycriu.rpc.NOTIFY
		req.notify_success = True
		self._cs.send(req.SerializeToString())

		return self._recv_resp()

	def get_log_name(self, req_type):
		return "criu_%s.%d.log" % (criu_req.get_name(req_type), self._iter)

#
# Helper to read CRIU-generated statistics
#

def criu_get_stats(img, file_name):
	with open(os.path.join(img.work_dir(), file_name)) as f:
		stats_dict = pycriu.images.load(f)
		stats = pycriu.images.stats_pb2.stats_entry()
		pycriu.images.pb2dict.dict2pb(stats_dict['entries'][0], stats)
		return stats

def criu_get_dstats(img):
	stats = criu_get_stats(img, "stats-dump")
	return stats.dump

def criu_get_rstats(img):
	stats = criu_get_stats(img, "stats-restore")
	return stats.restore
