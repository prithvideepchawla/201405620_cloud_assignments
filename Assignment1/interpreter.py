import os
import sys

if __name__ == '__main__':
    asm_32 = sys.argv[1]

    content_32bit = []
    
    with open(asm_32, 'r') as f32:
        for line in f32.readlines():
            content_32bit.append(line.strip())
    
    content_64bit = []
    for line in content_32bit:
        if len(line.split())>1 and line.split()[0] == 'section':
            content_64bit.append(line)
        elif len(line.split())>1 and line.split()[0] == 'message':
            content_64bit.append(line)
        elif line == 'global main':
            content_64bit.append('global _start')
        elif line == 'main:':
            content_64bit.append('_start:')
        elif line == 'pushad':
            content_64bit.append('mov     rax, 1')
            content_64bit.append('mov     rdi, 1')
        elif len(line.split())>1 and line.split()[0]=='push' and line.split()[1]=='dword':
            content_64bit.append('mov     rsi, '+line.split()[2])
        elif line == 'call printf':
            content_64bit.append('mov     rdx, 13')
            content_64bit.append('syscall')
        elif line == 'add esp, 4':
            content_64bit.append('mov    rax, 60')
            content_64bit.append('mov    rdi, 0')
        elif line == 'ret':
            content_64bit.append('syscall')

    with open('64bit_'+asm_32, 'w') as f64:
        for line in content_64bit:
            f64.write(line+'\n')


