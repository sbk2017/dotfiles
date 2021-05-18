#! /usr/bin/env python3

from subprocess import Popen, PIPE

def vpn():
    result = Popen(['expressvpn', 'status'], stdout=PIPE, stdin=PIPE).communicate()
    result = result[0].decode('utf-8').split('\n')[0]
    result = result.strip('\n')
    if 'Not connected' in result:
        return f'{result}'
    else :
        result =result.split()[2].strip()
        #print(result)
        return f'{result}'

if __name__ == '__main__':
    print(vpn())