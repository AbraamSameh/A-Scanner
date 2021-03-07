# Script Written by Abraam Sameh
import socket
from IPy import IP
import datetime
import os
from colorama import Fore
from colorama import Style

IP_Scans={}
temp_scan=[]

def check_port_range(start_port,end_port):
    try:
        if 1<= int(start_port)  < (int(end_port)+1) <= 65535:
            return 1
        else:
            return 0
    except:
        return 0

def check_port(PortNumber):
    try:
        if 1 <= int(PortNumber) <= 65535:
            return 1
    except:
        print(Fore.RED + str(PortNumber) + ' is NOT a valid port number' + Style.RESET_ALL)
        return 0

def scan_target_one_port(target,port, time):
    IP_Address = Get_IP(target)
    if IP_Address ==0:
        return
    if check_port(port) == 0:
        exit()
    print('\n' + Fore.BLUE + '-> scanning target : ' + str(IP_Address) + Style.RESET_ALL)
    scan_port(target, int(port), time)

def scan_target_port_range(target,start_port,end_port, time):
    IP_Address = Get_IP(target)
    if IP_Address == 0:
        return
    print('\n' +  Fore.BLUE + '-> scanning target : ' + str(IP_Address))
    if check_port_range(start_port,end_port) ==0:
        print(Fore.RED + str(start_port)+' - ' + str(end_port)+' Invalid Port Range'+Style.RESET_ALL)
        exit()
    for port in range(int(start_port),int(end_port)+1):
        scan_port(target, port, time)

def scan_target_port_list(target,ports,time):
    IP_Address = Get_IP(target)
    if IP_Address == 0:
        return
    print('\n' + Fore.BLUE + '-> scanning target : ' + str(IP_Address) + Style.RESET_ALL)
    for port in ports:
        if check_port(port.strip(' ')) == 0:
            continue
        scan_port(target, int(port), time)


def Get_IP(target):
    try:
        ipaddress = IP(target)
        return ipaddress

    except:
        # print("Invalid IP\n")
        try:
            ipaddress = socket.gethostbyname(target)
            return ipaddress
        except:
            print( Fore.RED + target + " -> is Innvalid Target\n"+ Style.RESET_ALL)
            return 0


def scan_port(ipaddress, port, time):
    try:
        sock = socket.socket()
        sock.settimeout(int(time))
        sock.connect((ipaddress, port))
        try:
            banner = sock.recv(1024).decode().strip('\n').strip('\r')
            service=str(socket.getservbyport(port, 'tcp'))
            print( Fore.LIGHTCYAN_EX + '[+] Port ' + str(port) + '/tcp - ' + service + ' is open : ' + str(banner) + Style.RESET_ALL)
            temp_scan.append(str(str(port) + '/tcp - ' + service +' : '+ str(banner)))
            IP_Scans[ipaddress]=temp_scan.copy()
            sock.close()
        except:
            service=str(socket.getservbyport(port, 'tcp'))
            print(Fore.LIGHTCYAN_EX + '[+] Port ' + str(port) + ' ' + service + ' is open' +Style.RESET_ALL)
            temp_scan.append(str(str(port) + '/tcp - ' + service))
            IP_Scans[ipaddress]=temp_scan.copy()
            sock.close()
    except:
        print(Fore.LIGHTRED_EX + '[-] Port ' + str(port) + ' is closed' + Style.RESET_ALL)
        pass

def writing_date():
    if not os.path.exists('Scans'):
        os.makedirs('Scans')
    os.chdir('./Scans')
    for key in IP_Scans.keys():
        path=str(key)+".txt"
        file = open(path, "w")
        file.writelines(str(key) + ' scan at: '+str(datetime.datetime.now())+'\n')
        # print(str(datetime.datetime.now()))
        for value in IP_Scans[key]:
            #print(value)
            file.writelines(value+'\n')
        #print(IP_Scans[key])
        file.close()

IP_Flag=0
R_Port_Flag=0




print(Fore.LIGHTCYAN_EX+'|-----    -----|  | ---- \          |------\  |-|---------   | ---- \     /-------\\')
print(Fore.LIGHTCYAN_EX+'| |-- \  / --| |  | |  |  |         | |--|  | | |--------/   | |  |  |   / /     \\ \\')
print(Fore.LIGHTCYAN_EX+'| |  \ \/ /  | |  | ---- /          |______/  | |-----|      | ---- /   / /       \\ \\')
print(Fore.LIGHTCYAN_EX+'| |   ----   | |  | |  | |   --     |      \  | |-----|      | |  | |   \ \       / /')
print(Fore.LIGHTCYAN_EX+'| |          | |  | |  | |  |  |    | |--|  | | |-------\    | |  | |    \ \     / /')
print(Fore.LIGHTCYAN_EX+'| |          | |  | |  | |   --     |------/  |-|---------   | |  | |     \-------/')
print()
print()
print()

Target_Input = input(Fore.LIGHTWHITE_EX + '[+] Please Enter Target/s put "," as delimeter: '+ Style.RESET_ALL)
Ports_Input= input(Fore.LIGHTWHITE_EX + '[+] Please Enter port/s put "-" as delimeter: ' + Style.RESET_ALL)

if '-' in Ports_Input:
    Ports_Input=Ports_Input.split('-')
    R_Port_Flag=1
elif ',' in Ports_Input:
    Ports_Input=str(Ports_Input).split(',')
    R_Port_Flag=2




try:
    Timing = int(input(Fore.LIGHTWHITE_EX + '[+] Please input timing speed [1->5]:' +Style.RESET_ALL))
    if not 1<= Timing <=5:
        exit()
except:
    print(Fore.RED + "Invalid Timing Input" + Style.RESET_ALL)
    exit()

if R_Port_Flag==0:
    if ',' in Target_Input:
        for target in Target_Input.split(','):
            #print(target)
            scan_target_one_port(target.strip(' '),Ports_Input,Timing)

    else:
        scan_target_one_port(Target_Input.strip(' '),Ports_Input,Timing)
    # print(IP_Scans)
    writing_date()

elif R_Port_Flag==1:
    if ',' in Target_Input:
        for target in Target_Input.split(','):
            scan_target_port_range(target.strip(' '),str(Ports_Input[0]).strip(' '),str(Ports_Input[1]).strip(' '),Timing)
            temp_scan.clear()
    else:
        scan_target_port_range(Target_Input.strip(' '),str(Ports_Input[0]).strip(' '),str(Ports_Input[1]).strip(' '),Timing)
    # print(IP_Scans)
    writing_date()

elif R_Port_Flag==2:
    if ',' in Target_Input:
        for target in Target_Input.split(','):
            scan_target_port_list(target.strip(' '),Ports_Input,Timing)
            temp_scan.clear()
    else:
        scan_target_port_list(Target_Input.strip(' '),Ports_Input,Timing)
    # print(IP_Scans)
    writing_date()


