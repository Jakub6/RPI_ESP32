# Main application file
import machine

print("MAIN START")

def main():
  print("Type your code here!")

try:
  #run main app here to reset on unhandled exceptions
  main()
except Exception as e:
  print("Unhandled exception:%s" % (str(e),))
  print("Runtime error encountered. Restarting in 10s")
  time.sleep(60.0)
  print("Restarting now!")
  machine.reset()
print("MAIN END")