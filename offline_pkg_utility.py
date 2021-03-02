import argparse
import platform
import subprocess
from subprocess import PIPE
import os
import getpass




class OfflinePkgUtility:
    _repo_ids = []
    _callback = None
    _sudo_password = ""
    _supported = ["centos", "fedora", "red hat"]
    def __init__(self, sudo_password=None, callback=None): 
        dist = (platform.linux_distribution()[0]).lower()
        for s in self._supported:
            if s in dist:
                return
        raise Exception("This tool only works for CentOS/RHEL/Fedora 7/8")
        
        if callback is not None:
            self._callback = callback
        if sudo_password is not None:
            self._sudo_password = sudo_password
    
    def _send_message(self, message):
        if self._callback is not None:
            self._callback(message)

    def _execute_root_command(self, command):
            p = subprocess.Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
            sudo_prompt = p.communicate(self._sudo_password + '\n')[1]
            p.terminate()

    def _get_repo_ids(self, callback=None):
        self._send_message("Retrieving repo names...")
        result = subprocess.check_output(["yum", "repolist"])
        result = result.decode().splitlines()
        for i in range(1, len(result)):
            self._repo_ids.append((result[i].split()[0]))
        self._send_message("Found: " + ', '.join(map(str, self._repo_ids)))
    
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

    def download_repos(self, name, path):
        self._repo_ids = []
        final_path = f"{path}/{name}/repos"
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        self._check_yum_utils_installed()
        self._download_required_server_pkgs(path=path, name=name)
        self._get_repo_ids()
        for id in self._repo_ids:
            self._send_message(f"Downloading packages from {id}...this may take a while...")
            command = f"reposync -m --repoid={id} --newest-only --download-metadata --download-path={final_path}".split()
            self._execute_root_command(command)
            self._send_message(f"Packages from {id} downloaded successfully.")
    def _download_required_server_pkgs(self, path, name):
        packages = ["httpd", "yum-utils", "python3-tkinter, createrepo"]
        for package in packages:
            self._send_message(f"Downloading {package}...")
            command = f"yum install -y --installroot={os.path.dirname(os.path.realpath(__file__))}/tmp --downloadonly --releasever=/ --downloaddir={path}/{name}/{package} {package}".split()
            self._execute_root_command(command)
            self._send_message(f"{package} download complete.")

    def setup_pm_server(self, path):
        self._check_yum_utils_installed()
        command = f"createrepo /var/www/html".split()
        self._execute_root_command(command)
        self._send_message(f"Setting up {package}...")
        command = f"mkdir -p /var/www/html/repos/".split()
        self._execute_root_command(command)
        command = f"cp -r {path}/repos/* /var/www/html/repos/".split()
        self._execute_root_command(command)
        command = f"systemctl restart httpd".split()
        self._execute_root_command(command)
    def setup_client(self, ip):
        command = "tee".split()
        self._execute_root_command(command)
        p = subprocess.Popen(['sudo', 'tee', '-a', '/tmp/test.txt'], stdin=PIPE, stderr=PIPE,
            universal_newlines=True)
        p.stdin.write(f'[remote] \n name=LocalNetwork \n baseurl=http://{ip} \n gpgcheck=0 \n enabled=1 \n')
        p.stdin.close()
        p.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--path', help='Path to where to save the data')
    parser.add_argument('--name', help='Name of configuration')
    parser.add_argument('--ip', help='YUM offline server IP used by client')
    parser.add_argument('--setup-server', help='server', action='store_true')
    parser.add_argument('--download', help='Use the tool to download repos', action='store_true')
    parser.add_argument('--setup-client', help='Setup the current machine as client to a specific package manager server', action='store_true')
    parser.add_argument('--sudo-password', help='Sudo password if current user has such access', action='store_true')
    args = parser.parse_args()
    pswd = None
    if (not args.download and not args.setup_server and not args.setup_client) or (args.download and args.setup_server and args.setup_client) or (args.download and args.setup_server) or (args.setup_server and args.setup_client) or (args.download and args.setup_client): 
        parser.error("Use one: [--download], [--setup-server], or [--setup-client]")
    if args.download and (args.name is None or args.path is None):
        parser.error("--download requires --name and --path.")
    elif args.setup_server and (args.path is None):
        parser.error("--setup-server requires --path.")
    elif args.setup_client and (args.ip is None):
        parser.error("--setup-server requires --ip.")
    if args.sudo_password:
        pswd = getpass.getpass('Sudo Password:')
    offline_package_util = OfflinePkgUtility(sudo_password=pswd)
    if args.download:
        offline_package_util.download_repos(name=args.name, path=args.path)
    elif args.setup_server:
        offline_package_util.setup_pm_server(path=args.path)
    elif args.setup_client:
        offline_package_util.setup_client(ip=args.ip)
