#!/usr/bin/env python
#
# Python Installer
#
import subprocess
import sys
import os
import platform

# if nix then run installer
if platform.system() == "Linux":
    # give installer a null value
    installer = False

    # Check user ID
    if os.getuid() != 0:
	print("Are you root? Please execute as root")
	exit()

    try:
	# if our command option is true then install dependencies
	if sys.argv[1] == "install":
	    installer = True

    # if index is out of range then flag options
    except IndexError:
	print("** Auto SSH Dependency Installer by Facerecog Asia **")
	print("** Written by: Muhammad Amrullah (Facerecog Asia) **")
	print("** Visit: https://github.com/facerecog **")
	print("\nTo install: setup.py install")

    # if user specified install then lets proceed to the installation
    if installer is True:

	# if we trigger on sources.list then we know its ubuntu
	if os.path.isfile("/etc/apt/sources.list"):

	    # force install of debian packages
	    subprocess.Popen("apt-get --force-yes -y install openssh-server", shell=True).wait()
	 
	    if 'ServerAliveInterval' not in open('/etc/ssh/ssh_config').read():
    		writetoSSH = open('/etc/ssh/ssh_config','a')
    		writetoSSH.write("    ServerAliveInterval 30\n    ServerAliveCountMax 4")
    		writetoSSH.close()

	    if 'ClientAliveInterval' not in open('/etc/ssh/sshd_config').read():
	        writetoSSH = open('/etc/ssh/sshd_config','a')
    		writetoSSH.write("ClientAliveInterval 30\nClientAliveCountMax 4")
    		writetoSSH.close()

	# if sources.list is not available then we're running something offset
	else: 
	    print("[!] You're not running a Debian variant. Installer not finished for this type of Linux distro.")
	    print("[!] Install open-ssh server manually for all of autossh dependencies.")
	    sys.exit()
	
	# if installation is done on client, the autossh automatically kicks in the daemon
	try:
	    rootname = raw_input("What is the server's rootname@ipaddress?: ")
	    print("[*] Moving autossh client into the /usr/local/bin/ directory...")
	    subprocess.Popen("yes | cp Client/connect.sh /usr/local/bin/", shell=True).wait()
	    print("[*] Installing autossh client...")
	    subprocess.Popen("chmod +x /usr/local/bin/connect.sh", shell=True).wait()
	    print("[*] Installing autossh as startup application...")
	    subprocess.Popen("yes | cp Client/connect.sh /etc/init.d/", shell=True).wait()
            subprocess.Popen("chmod +x /etc/init.d/connect.sh", shell=True).wait()
            subprocess.call("printf 'server\n\n' | ssh-keygen -t rsa -b 2048 -v", shell=True)
	    print("[*] Copying SSH-Keys file over to server...")
	    subprocess.call(['ssh-copy-id', '-i', 'server.pub', rootname])
            print("[*] Installing private keys inside protected folder...")		
	except subprocess.CalledProcessError as e:
	    pass
	
	# if the installation has been successful
	if os.path.isfile("/usr/local/bin/connect.sh"):
	    print("[*] We are now finished! Restart the client to complete the installation. To run autossh, input connect.sh on the terminal")
	    subprocess.Popen("connect.sh", shell=True)
	else:
	    print("[!] Installation has failed. Please ensure that connect.sh and .pub file is installed")

# if the platform is running on a MAC, a version will be ready soon
if platform.system() == 'Darwin':
    print("[!] A version for Mac will be ready soon")

if platform.system() != "Linux":
   if platform.system() != "Darwin":
	print("[!] Sorry this installer is not designed for any other system other than Linux or Mac. Please install the python dependencies manually.")
