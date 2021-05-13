#! /usr/bin/env python3

from subprocess import Popen, PIPE

result = Popen(['expressvpn', 'status'], stdout=PIPE, stdin=PIPE).communicate()
result = result[0].decode('utf-8').split('\n')[0]
result = result.strip('\n')
if 'Not connected' in result:
    print(f'{result}')
else :
    result =result.split()[2].strip()
    #print(result)
    print(f'{result}')
