import argparse
import platform
import subprocess
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('--path', help='Path to where to save the data')
parser.add_argument('--name', help='Name of configuration')
parser.add_argument('--setup-server', help='server', action='store_true')
parser.add_argument('--download', help='Use the tool to download repos', action='store_true')
args = parser.parse_args()



repo_ids = []


def get_repo_ids():
    result = subprocess.check_output(["yum", "repolist"])
    result = result.decode().splitlines()
    for i in range(1, len(result)):
        repo_ids.append((result[i].split()[0]))


if (not args.download and not args.setup_server) or (args.download and args.setup_server):
    parser.error("Use either --download or --setup-server but not both")

if args.download and (args.name is None or args.path is None):
    parser.error("--download requires --name and --path.")

if platform.linux_distribution()[0] != "CentOS Linux":
    raise Exception("This tool only works for CentOS/RHEL/Fedora 7/8")



print(args)