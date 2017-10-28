#!/usr/bin/python

import sys, argparse, socket

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input", help="Input file")
    parser.add_argument("-t", help="TCP port sccaner range, i.e. -t 1-1024")
    parser.add_argument("-u", help="UDP port scanner range, i.e. -u 1-1024")
    parser.add_argument("-d", help="Destination to run scan, i.e. -d 192.168.1.1")
    parser.add_argument("-D", help="Range of IP's given by CIDR / i.ie -D 192.168.1.0/24")
    args = parser.parse_args()

# Given a list of IP address in a txt file
    if args.input:
        IPs = parseInputFile(args.input)
        
        if not args.t and not args.u:       # User did not specify either TCP or UDP
            for ip in IPs:
                for port in range(1,1024):         # Give standard port range
                    scanTCP(ip,port)
        else:     
            if args.t:          # TCP
                for ip in IPs:
                    tcpLoop(ip,args.t)
                    print ""
                        
            if args.u:          # UDP
                for ip in IPs:
                    udpLoop(ip,args.u)
                    print ""
# Range of IPs given by the /
    elif args.D:      
        if not args.t and not args.u:       # User did not specify either TCP or UDP
            for ip in IPs:
                for port in range(1,1024):         # Give standard port range
                    scanTCP(ip,port)
        else:     
            if args.t:          # TCP
                for ip in IPs:
                    tcpLoop(ip,args.t)
                    print ""
                        
            if args.u:          # UDP
                for ip in IPS:
                    udpLoop(ip,args.u)
                    print ""
# Just a single remote desination
    else:
        if args.d: 
            if not args.t and not args.u:       # User did not specify either TCP or UDP
                for port in range(1,1024):         # Give standard port range
                    scanTCP(args.d,port)
            else:     
                if args.t:          # TCP
                    tcpLoop(args.d,args.t)
                if args.u:          # UDP
                    udpLoop(args.d,args.u)




        else:
            print "Please provide a Remote host or a input file of hosts"
    
def tcpLoop(IP,ports):
    portRange = ports.split('-')   # Find the range of the tcp ports
    if len(portRange) > 1:
        for t in range(int(portRange[0]),int(portRange[1]) + 1):
            scanTCP(IP,int(t))
    else:
        scanTCP(IP,int(ports))

def udpLoop(IP,ports):
    uPortRange = ports.split('-')   # Find the range of the UDP ports)
    if len(uPortRange) > 1:
        for u in range(int(uPortRange[0]),int(uPortRange[1]) + 1):
            scanUDP(IP,int(u))
    else:
        scanUDP(IP,int(ports))

def subnetCalculator(IP):
    temp = IP.split('/')
    subnet = temp[1]            #Subnet CIDR
    IP = temp[0]                #IP Address
    ipPortions = IP.split('.')  #break up the IP into the octets

    exp = 32-int(subnet)        #Exponent
    numOfIPs = 2 ** exp         #Number of IPs

    start = ipPortions[3]       #find Starting address
    end = int(start) + numOfIPs

    IPs = []
    lastPortion = int(start)
    for i in range(0,numOfIPs):
        if lastPortion > 255:               # last portion reached max
            lastPortion = 0
            if ipPortions[2] == 255:        # 2nd to last octet reached max
                ipPortions[2] = 0
                if ipPortions[1] == 255:    # 3rd to last octet reached max
                    ipPortions[1] = int(ipPortions[1]) + 1
                    ipPortions[0] = int(ipPortions[0]) + 1
            else:
                ipPortions[2] = int(ipPortions[2]) + 1  # increment 2nd to last octet up 1
        
        tempIP = str(ipPortions[0]) + '.' + str(ipPortions[1]) + '.' + str(ipPortions[2]) + '.' + str(lastPortion)
        IPs.append(tempIP)

        lastPortion = lastPortion + 1
    return IPs

#Given a filepath or name this function will read line by line and create an array of IP addresses
def parseInputFile(fileName):
    with open(fileName,'r') as f:
        content = [line.strip() for line in f if line.strip()]  #   Remove blank space and new line
    return content;                                             #   Return list of IPs

#Given an IP address and Port this function will send a TCP packet to find if the port is listening
def scanTCP(IP,Port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((IP,Port))
    if result == 0:
        print "IP:{}    Port{}: Open".format(IP,Port)
    sock.close()

#Given an IP address and Port this function will send a packet using UDP to find if the port is listening
def scanUDP(IP,Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    try:
        s.sendto('ping'.encode(),(IP,Port))
        s.recvfrom(1024)
        print "IP:{}    Port{}: Open".format(IP,Port)
    except:
        s.close()
    s.close()
if __name__ == "__main__":
    main()