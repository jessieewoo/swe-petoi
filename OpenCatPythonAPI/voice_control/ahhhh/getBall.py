from PetoiRobot import *
import time, sys

if __name__ == '__main__':
    autoConnect()
    time.sleep(2)

    def pick_up_ball():
        if len(goodPorts) > 0:
            try:
                print("Setting robot to stand...")
                # 'kbalance' with 1 usually keeps the gyro active for stabilization
                # Start walking indefinitely
                #send(goodPorts, ['kcrL', 1])
                send(goodPorts, ['kwkF', 0])         
                time.sleep(4.0) 
                #send(goodPorts, ['kcrL', 1])

                send(goodPorts, ['kpickF', 0]) 

                
                # Stop and Lock
                send(goodPorts, ['kbalance', 1])     
                    
                print("Robot is standing. Press Ctrl+C to stop the program and close the port.")
                
                # This loop keeps the Python script alive indefinitely
                while True:
                    time.sleep(1) 
                    
            except KeyboardInterrupt:
                # This block runs when you press Ctrl+C
                print("\nShutting down safely...")
                # Optional: Relax the servos before closing so it doesn't stay stiff
                send(goodPorts, ['d', 0]) 
            
            finally:
                closePort()
                print("Port closed. Goodbye!")
                sys.exit(0)
        else:
            print("No robot connected. Check your cables/Bluetooth.")
