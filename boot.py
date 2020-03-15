# This file is executed on every boot (including wake-boot from deepsleep)
try:
  import machine
  import time
  import auto_connect
  #import uftpserver
  import ftp
  import _thread

  auto_connect.auto_connect()
  time.sleep(10)
  if(auto_connect.con_test()):
    print("WIFI OK")
  else:
    print("WIFI KO!")

  ftp_thread = _thread.start_new_thread(ftp.ftpserver, (True,))
except Exception as e:
  print("Unhandled exception:%s" % (str(e),))
  print("Boot encountered. Restarting in 10s")
  time.sleep(10.0)
  print("Restarting now!")
  machine.reset()
print("BOOT END")