#!/usr/bin/python

import argparse
import sys
import textwrap

parser = argparse.ArgumentParser(
    description='Simple NSE Generator: ',
    epilog='Generate a script for port 80/tcp: python nse-generator.py 80 tcp')

parser.add_argument('port', help='port number we want nmap to scan',
                    type=int)
parser.add_argument('protocol', help='TCP or UDP', type=str,
                    action='store')
parser.add_argument('-s', '--state', help='port state, default is open (open, closed or filtered)', type=str,
                    action='store', default='open')
args = parser.parse_args()

print(args.port)
if args.protocol in ['tcp', 'TCP', 'Tcp', 'tCP']:
    myproto = '"tcp"'
elif args.protocol in ['udp', 'UDP', 'Udp', 'UDP']:
    myproto = '"udp"'
else:
    sys.exit('I need a real protocol, tcp or udp!')

print("Generating script to scan: port {0}/{1}'s that are {2}!".format(args.port,args.protocol,args.state))

# probably moving this to file later
output = textwrap.dedent("""\
local shortport = require "shortport"
local nmap = require "nmap"

description=[[
Basic script with easy configuration to output a list of IPs that meet
certain simple criteria, outputs to IP list, seperated by new lines.
]]

author = "Original: ROleg, Updates by smt"
license = "Same as Nmap--See http://nmap.org/book/man-legal.html"

--Can be edited manually, or with the generator
local myport 	= {0}
local myproto 	= {1}
local mystate	= {2}

categories = {{"default", "discovery", "external", "intrusive"}}
portrule = shortport.portnumber(myport, myproto, mystate)
action = function(host, port)
	file = io.open ("results.txt","a+")
	file:write (host.ip.."\\n")
	file:flush()
	file:close()
end
""").format(args.port,myproto,'"'+str(args.state)+'"')

# maybe add a .sh generate for linux users? but they probably know how to use nmap
runfile = textwrap.dedent("""\
@echo off
nmap -n -Pn -p T:{0} -T5 -v --script myscan.nse -iR 0 --max-hostgroup 512
exit
""").format(args.port,myproto,'"'+str(args.state)+'"')

with open('myscan.nse', 'w') as f:
    f.write(output)

with open('run-myscan.bat', 'w') as f:
    f.write(runfile)
