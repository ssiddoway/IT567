Python Port Scanner

I wrote this port scanner using python and the sockets and argparse libraries.

I allow the user to scan a host or list of hosts through 3 options
1. A single host: �d 192.168.207.41 
2. A file with IP�s separated by new line: --input targets.txt
3. And a range: -D 192.168.207.0/24
Allow Multiple ports to be specified. The User may run scans using TCP, or UDP
* Tcp: -t 1-250, or �t 22
* UDP �u 1-1024 or �u 53

