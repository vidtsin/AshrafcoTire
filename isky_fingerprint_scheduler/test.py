# -*- coding: utf-8 -*-
import sys

from zk3 import ZK, const

sys.path.append("zk")

conn = None
zk = ZK('192.168.0.75', port=4370, timeout=10 , password=0, force_udp=False, verbose=False)
print('Connecting to device ...')
conn = zk.connect()
print('Disabling device ...')
conn.disable_device()
print( 'Firmware Version: : {}'.format(conn.get_firmware_version()))
conn.enable_device()
attend =  conn.get_attendance()
for at in attend :
   print( "id" , at.user_id)
   print( "time" , at.timestamp)
   print( "status", at.status)

# print('::::::::::: clearing attendance data in the device :::::::::::: ')
# conn.clear_attendance()
# print('::::::::::: clearing attendance data Done :::::::::::: ')
if conn:
   conn.disconnect()
