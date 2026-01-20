import nmap # type: ignore

try: 
    nm = nmap.PortScanner()
    # nm.scan('127.0.0.1') # For testing the most common ports, will use 1-65535 once code is good enough to save time
    # nm.scan('127.0.0.1', '1-65535') # All the ports, not just small range or most common

    
    try:
        print("\nAdmin Scan has started\n")
        nm.scan('127.0.0.1', '1-65535', timeout=300) # Will timeout if scan takes longer than 5 minutes
    except:
         print("There was a permission error or timeout, trying the permissionless version")
         nm.scan('127.0.0.1', '1-65535', arguments='-sT', timeout=150) # -sT will allow non admin users to run the command, if scan takes longer than 2.5 minutes it times out

    nm.command_line() #Actually will perform the nmap scan
    nm.scaninfo() # shows nmap scan  information
    nm.all_hosts() # all the hosts in the scan
    nm['127.0.0.1'].hostname() # hostname for the ip
    nm['127.0.0.1'].state() # shows the state of host
    nm['127.0.0.1'].all_protocols() # list of protocols


    if not nm.all_hosts:
        print('\n--------------------------------')
        print("Error")
        print("No host was discovered / Host is unreachable")
        print('\n--------------------------------')
    else:
        for host in nm.all_hosts():
                print('\n--------------------------------')
                print('Host : %s (%s)' % (host, nm[host].hostname()))
                print('State : %s' % nm[host].state())
                
                for proto in nm[host].all_protocols():
                    print('--------------------------------')
                    print('Protocol : %s' % proto)
                    lport = nm[host][proto].keys() # gets the port keys and converts to a list

                    for port in lport: # for loop showing the state of each port
                        print ('port: %s\tstate : %s' % (port, nm[host][proto][port]['state']),'|', (nm[host][proto][port]['name'])) # 'state' and 'name' are on the same level in the port dictionary so the statement must be made twice

except nmap.PortScannerError as e:
     print(f"Nmap Error: {e}") # Error handling if nmap isn't installed or accessible
except Exception as e:
     print(f"An unexpected error occurred: {e}") # Other error handling
