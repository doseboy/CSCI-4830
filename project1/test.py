import sys
from pymd5 import md5, padding

m="Use HMAC, not hashes"
m2="Good advice"
complete_message="Use HMAC, not hashesGood advice"
complete_with_space="Use HMAC, not hashes Good advice"
complete_with_newline="Use HMAC, not hashes\nGood advice"

H=md5()
H2=md5()
H_complete_no_padding=md5()
H_complete_padding=md5()

H.update(m)
print('ORIGINAL MESSAGE: H.hexdigest()')
print('Function: "{0}" -> "{1}"'.format(m, H.hexdigest()))
print('END OF MESSAGE\n')

H.update(m2)
print('UPDATING MESSAGE: H.update(m2)')
print('Function: "{0}" -> "{1}"'.format("H.update(m2)", H.hexdigest()))
print('END OF MESSAGE\n')

# H2.update(m2)
# print('JUST m2 MESSAGE')
# print('Function: "{0}" -> "{1}"'.format('H2.update(m2)', H2.hexdigest()))
# print('END OF MESSAGE\n')

# H_complete_no_padding.update(complete_message)
# print('COMPLETE MESSAGE')
# print('Function: "{0}" -> "{1}"'.format('H_complete_message_no_padding.update(complete_message)', H2.hexdigest()))
# print('END OF MESSAGE\n')

print(m.encode()+padding(len(m)*8)+m2.encode())
