import argparse
import platform
import subprocess
from subprocess import PIPE
import os
from enum import Enum
import shutil


class UseType(Enum):
    DOWNLOAD = 1
    SETUP = 2

class OfflinePkgUtility:
    repo_ids = []
    def __init__(self, use_type): 
        if platform.linux_distribution()[0] != "CentOS Linux":
            raise Exception("This tool only works for CentOS/RHEL/Fedora 7/8")
        if use_type.value == 1:
            self.download_repos(name=name, path=path)
    
    def _get_repo_ids(self):
        result = subprocess.check_output(["yum", "repolist"])
        result = result.decode().splitlines()
        for i in range(1, len(result)):
            self.repo_ids.append((result[i].split()[0]))
    
    def _check_yum_utils_installed(self):
        command = "reposync --version".split()
        try:
            p = subprocess.Popen(command, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
            stdout, stderr = p.communicate()
            if stderr:
                raise Exception("yum-utils is not installed.")
        except FileNotFoundError as e:
            raise Exception("yum-utils is not installed.")


    def sudo_test(self):
        command = "yum install httpd".split()
        p = subprocess.Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
        sudo_prompt = p.communicate(os.getenv("SUDO_PASSWORD") + '\n')[1]
        p.terminate()
    def download_repos(self, name, path):
        final_path = f"{path}/{name}/repos"
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        self._check_yum_utils_installed()
        self._download_required_server_pkgs(path=path, name=name)
        self.get_repo_ids()
        for id in self.repo_ids:
            command = f"sudo reposync -m --repoid={id} --newest-only --download-metadata --download-path={final_path}".split()
            p = subprocess.Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
            sudo_prompt = p.communicate(os.getenv("SUDO_PASSWORD") + '\n')[1]
            p.terminate()
    def _download_required_server_pkgs(self, path, name):
        packages = ["httpd", "yum-utils"]
        for package in packages:
            command = f"yum install -y --installroot={os.path.dirname(os.path.realpath(__file__))}/tmp --downloadonly --releasever=/ --downloaddir={path}/{name}/{package} {package}".split()
            p = subprocess.Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
            sudo_prompt = p.communicate(os.getenv("SUDO_PASSWORD") + '\n')[1]
            p.terminate()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--path', help='Path to where to save the data')
    parser.add_argument('--name', help='Name of configuration')
    parser.add_argument('--setup-server', help='server', action='store_true')
    parser.add_argument('--download', help='Use the tool to download repos', action='store_true')
    args = parser.parse_args()
    if (not args.download and not args.setup_server) or (args.download and args.setup_server):
        parser.error("Use either --download or --setup-server but not both")

    if args.download and (args.name is None or args.path is None):
        parser.error("--download requires --name and --path.")
    if args.download:
        use_type = UseType.DOWNLOAD

    offline_package_util = OfflinePkgUtility(use_type, path=args.path, name=args.name)
    