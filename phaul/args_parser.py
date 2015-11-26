#
# p.haul command line arguments parsers
#

import argparse
import htype
import images
import criu_api
import iters


def parse_client_args():
	"""Parse p.haul command line arguments"""

	parser = argparse.ArgumentParser("Process HAULer")
	parser.set_defaults(pre_dump=iters.PRE_DUMP_AUTO_DETECT)

	parser.add_argument("type", choices=htype.get_haul_names(),
		help="Type of hat to haul, e.g. vz, lxc, or docker")
	parser.add_argument("id", help="ID of what to haul")
	parser.add_argument("--to", help="IP where to haul")
	parser.add_argument("--fdrpc", type=int, required=True, help="File descriptor of rpc socket")
	parser.add_argument("--fdmem", type=int, required=True, help="File descriptor of memory socket")
	parser.add_argument("--fdfs", type=int, required=True, help="File descriptor of fs socket")
	parser.add_argument("-v", default=criu_api.def_verb, type=int, dest="verbose", help="Verbosity level")
	parser.add_argument("--keep-images", default=False, action='store_true', help="Keep images after migration")
	parser.add_argument("--dst-rpid", default=None, help="Write pidfile on restore")
	parser.add_argument("--img-path", default=images.def_path,
		help="Directory where to put images")
	parser.add_argument("--pid-root", help="Path to tree's FS root")
	parser.add_argument("--force", default=False, action='store_true', help="Don't do any sanity (CPU compat) checks")
	parser.add_argument("--log-file", help="Write logging messages to specified file")
	parser.add_argument("-j", "--shell-job", default=False, action='store_true',
		help="Allow migration of shell jobs")
	parser.add_argument('--no-pre-dump', dest='pre_dump', action='store_const',
		const=iters.PRE_DUMP_DISABLE, help='Force disable pre-dumps')
	parser.add_argument('--pre-dump', dest='pre_dump', action='store_const',
		const=iters.PRE_DUMP_ENABLE, help='Force enable pre-dumps')

	return parser.parse_args()


def parse_service_args():
	"""Parse p.haul-service command line arguments"""

	parser = argparse.ArgumentParser("Process HAULer service server")

	parser.add_argument("--fdrpc", type=int, required=True, help="File descriptor of rpc socket")
	parser.add_argument("--fdmem", type=int, required=True, help="File descriptor of memory socket")
	parser.add_argument("--fdfs", type=int, required=True, help="File descriptor of fs socket")
	parser.add_argument("--log-file", help="Write logging messages to specified file")

	return parser.parse_args()