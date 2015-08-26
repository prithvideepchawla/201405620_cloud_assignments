import os
import sys
import subprocess

if __name__ == '__main__':
    asm_32 = sys.argv[1]
    
    content_32bit = []
    
    with open(asm_32, 'r') as f32:
        for line in f32.readlines():
            content_32bit.append(line.strip())
   
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print ">>>>32bit ASM code :"
    for line in content_32bit:
        print line

    asm_32_out = asm_32.split('.')[0]+'.o'
    
    command1 = 'nasm -f elf32 '+asm_32 
    command2 = 'gcc -m32 '+asm_32_out+' -o 32bit_run'
    command3 = os.getcwd()+'/32bit_run'
    process = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(command3, shell=True, stdout=subprocess.PIPE)
    
    print ">>>>32bit executable's output :"
    print process.communicate()[0]
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

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
    
    print ">>>>64bit ASM code :"
    for line in content_64bit:
        print line

    asm_64_out = '64bit_'+asm_32_out

    command1 = 'nasm -f elf64 64bit_'+asm_32 
    command2 = 'ld '+asm_64_out+' -o 64bit_run'
    command3 = os.getcwd()+'/64bit_run'
    process = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(command3, shell=True, stdout=subprocess.PIPE)
    
    print ">>>>64bit executable's output :"
    print process.communicate()[0]
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
