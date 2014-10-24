nse-generator
=====================

A very simple way to generate very simple nmap scripts that makes it very easy to do basic research or just poke around at the internet

Currently it will generate a script to scan for a chosen port, tcp or udp, and output a list of found ips open, closed or filtered, one per line, more customization to come.

Current usage is simple: python nse-generator.py (port) (protocol) [-s (port state)]

Examples:  
python nse-generator.py 80 tcp  >  find servers with tcp port 80 open  
python nse-generator.py 53 udp -s closed  >  find servers with udp port 53 closed  

TODO:

- add much more customiation options
- put the base script into another file
- general improvements
