import nmap # type: ignore

nm = nmap.PortScanner()
# nm.scan('10.5.0.2', '12000') # To be used after when scanning server

nm.scan('127.0.0.1', '20-1024') # 127.0.0.1 is always localhost
nm.command_line() #Actually will perform the nmap scan
nm.scaninfo() # shows nmap scan  information
nm.all_hosts() # all the hosts in the scan
nm['127.0.0.1'].hostname() # hostname for the ip
nm['127.0.0.1'].state() # shows the state of host
nm['127.0.0.1'].all_protocols() # list of protocols
nm['127.0.0.1']['tcp'].keys() # all port numbers found for tcp

for host in nm.all_hosts():
    print('\n--------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state())
    
    for proto in nm[host].all_protocols():
        print('--------------------------------')
        print('Protocol : %s' % proto)

        lport = nm[host][proto].keys() # gets the port keys and converts to a list
        for port in lport: # for loop showing the state of each port
            print ('port: %s\tstate : %s' % (port, nm[host][proto][port]['state'])) 
