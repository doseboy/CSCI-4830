#Author: William Anderson
#Identikey: wian8678
#Assignment: Project 1
#Class: ECEN 4113

import sys
from pymd5 import md5, padding
try:
    from urllib import quote  # Python 2.X
except ImportError:
    from urllib.parse import quote  # Python 3+

url = sys.argv[1]

#Grab first part of url
first_part = url[:url.find("=") + 1]
#print("first part of url: " + first_part)

#What we know needs to be hashed by md5
second_part = url[url.find("=") + 1:url.find("&")]
#print("second part of url: " + second_part)

#compute message from url
m = url[url.find("&") + 1:]
#print("m = " + m)

#compute length of m plus 8 bits
mlen = len(m) + 8
#print("mlen = " + str(mlen))

#calculate bits
bits = (mlen + len(padding(mlen * 8))) * 8
#print("bits = " + str(bits))

#Calculate hash from md5
h = md5(state=bytes.fromhex(second_part), count=bits)
command = "&command=UnlockSafes"
#print("h = " + str(h))

#Append command to hash
h.update(command)
#print("updated h = " + str(h))

#generate new hash
newh = h.hexdigest()
#print("newh = " + str(newh))
padding = quote(padding(mlen * 8))
#print("padding = " + padding)

#generate message with padding
m = m + padding + command
#print("Full m = " + m)

#generate the new url with length extension + command
new_url = first_part + newh + "&" + m
print("New URL is: " + new_url)
