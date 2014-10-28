#!/usr/bin/python

import argparse
import sys
import textwrap

parser = argparse.ArgumentParser(
    description='Simple NSE Generator: ',
    epilog='Generate a script for port 80/tcp: python nse-generator.py 80 tcp')

parser.add_argument('port',
                    help='port number we want nmap to scan',
                    type=int)
parser.add_argument('protocol',
                    help='TCP or UDP', type=str,
                    action='store')
parser.add_argument('-s', '--state',
                    help='port state, default is open (open, closed or filtered)', type=str,
                    action='store', default='open')
parser.add_argument('-o', '--output',
                    help='set the name for the generated NSE file, don\'t include .nse, default is myscan', type=str,
                    action='store', default='myscan')
parser.add_argument('-t', '--timing',
                    help='timing or scan speed, same as nmap, default is 4', type=int,
                    action='store', default='4')
parser.add_argument('-H', '--hosts',
                    help='amount of random hosts to scan through, default is unlimited', type=int,
                    action='store', default='0')
parser.add_argument('-w', '--windows',
                    help='if you give us -w, output a windows .bat file instead of the default linux .sh',
                    action='store_true')
args = parser.parse_args()

# Get some of our vars ready for easier use
if args.protocol in ['tcp', 'TCP', 'Tcp', 'tCP']:
    myproto = '"tcp"'
elif args.protocol in ['udp', 'UDP', 'Udp', 'UDP']:
    myproto = '"udp"'
else:
    sys.exit('I need a real protocol, tcp or udp!')

filename = args.output+'.nse'
filewin = 'run-'+filename+'.bat'
filelinux = 'run-'+filename+'.sh'
myportstate = '"'+str(args.state)+'"'

# all our outputs
output = textwrap.dedent("""\
local shortport = require "shortport"
local nmap = require "nmap"

description=[[
Basic script with easy configuration to output a list of IPs that meet
certain simple criteria, outputs to IP list, seperated by new lines.
]]

author = "Original: ROleg, Updates by smt"
license = "Same as Nmap--See http://nmap.org/book/man-legal.html"

categories = {{"default", "discovery", "external", "intrusive"}}
portrule = shortport.portnumber({0}, {1}, {2})
action = function(host, port)
	file = io.open ("results.txt","a+")
	file:write (host.ip.."\\n")
	file:flush()
	file:close()
end
""").format(args.port,myproto,myportstate)

runfilelinux = textwrap.dedent("""\
#!/bin/bash
nmap -n -Pn -p T:{0} -T{3} -v --script {5} -iR {4} --max-hostgroup 512
""").format(args.port, myproto, myportstate, args.timing, args.hosts, filename)

runfilewin = textwrap.dedent("""\
@echo off
nmap -n -Pn -p T:{0} -T{3} -v --script {5} -iR {4} --max-hostgroup 512
exit
""").format(args.port, myproto, myportstate, args.timing, args.hosts, filename)

with open(filename, 'w') as f:
    f.write(output)

# by default make a .sh file for easily running the script, -w for windows .bat
if args.windows:
    with open(filewin, 'w') as f:
        f.write(runfilewin)
else:
    with open(filelinux, 'w') as f:
        f.write(runfilelinux)
# just makes reading the final confirmation easier to read
if args.hosts == 0:
    args.hosts = "Unlimited"

print("Generating {5}, it scans {4} hosts on port {0}/{1}'s that are {2} at speed T{3}!".format(
    args.port, args.protocol, args.state, args.timing, args.hosts, filename))

# ask the user if we want to jump straight into a scan
runnmap = input("Start the scan now? (y/N) ")
yes = ['yes', 'y', 'ye']
no = ['no', 'n', '']

from subprocess import call
if runnmap.lower() in yes and args.windows:
    try:
        print("Starting, press Ctrl-C to exit")
        call(filewin, shell=True)
    except KeyboardInterrupt:
        exit("Ctrl-C received, closing")
elif runnmap.lower() in yes and not args.windows:
    try:
        print("Starting, press Ctrl-C to exit")
        call(filelinux, shell=True)
    except KeyboardInterrupt:
        exit("Ctrl-C received, closing")
