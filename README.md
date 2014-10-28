nse-generator
=====================

A very simple way to generate very simple nmap scripts that makes it very easy to do basic research or just poke around at the internet

Currently it will generate a script to scan for a chosen port, tcp or udp, and output a list of found ips open, closed or filtered, one per line, more customization to come. After generating the script you're offered to run the script straight away, on linux this will chmod the file.

Current usage is simple, with optional args below: python nse-generator.py (port) (protocol)  
-s (port state)  
-o (output name)  
-t/T (0-5, nmap timings/scan speed)  
-H (number of random hosts to scan)  
-w (generate a windows .bat file)  
  
##Examples:  
find servers with tcp port 80 open:

```
python nse-generator.py 80 tcp  
```

find servers with udp port 53 closed:  

```
python nse-generator.py 53 udp -s closed  
```

find servers with 443 open, scan slowly, call the script "ssl.nse" and generate a windows .bat file to run our script 

```
python nse-generator.py 443 tcp open -T2 -o ssl -w
```

##Planned:

- add much more customization options
- put the base scripts into their own files
- general improvements
