import socket
import json
import time
import sys
import copy
import subprocess

def connectETController(ip, port=8055):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        return (True, sock)
    except Exception as e:
        sock.close()
        return (False, sock)  # Return the socket even in case of failure

def disconnectETController(sock):
    if sock:
        sock.close()
        sock = None
    else:
        sock = None

def sendCMD(sock, cmd, params=None, id=1):
    if not params:
        params = []
    else:
        params = json.dumps(params)
    sendStr = "{{\"method\":\"{0}\",\"params\":{1},\"jsonrpc\":\"2.0\",\"id\":{2}}}".format(cmd, params, id) + "\n"
    try:
        sock.sendall(bytes(sendStr, "utf-8"))
        ret = sock.recv(1024)
        jdata = json.loads(str(ret, "utf-8"))
        if "result" in jdata.keys():
            return (True, json.loads(jdata["result"]), jdata["id"])
        elif "error" in jdata.keys():
            return (False, jdata["error"], jdata["id"])
        else:
            return (False, None, None)
    except Exception as e:
        return (False, None, None)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        try:
            counter = int(sys.argv[1])
            print(f"Counter value received: {counter}")
        except ValueError:
            print("Invalid counter value provided")
            sys.exit(1)
    else:
        print("No counter value provided")
        sys.exit(1)
    counter_rem=counter%2

    


    

    robot_ip = "192.168.1.200"
    conSuc, sock = connectETController(robot_ip)

    # If servo is off, turn servo on
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 0:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 1})

    # Set robot speed
    suc, result, id = sendCMD(sock, "setSpeed", {"value": 50})

    jbi_filename="cocktail"
    if conSuc:
        suc, result, id = sendCMD(sock, "checkJbiExist", {"filename": jbi_filename})
        if suc and result == 1:
            print("jbi file found")

            # Run jbi file
            suc, result, id = sendCMD(sock, "runJbi", {"filename": jbi_filename})
            print("command sent")
            print(result)

            if suc and result:
                checkRunning = 3
                while checkRunning == 3:
                    # Get jbi file running status
                    suc, result, id = sendCMD(sock, "getJbiState")
                    checkRunning = result["runState"]
                    time.sleep(0.1)
                    print(result)

    suc, result, id = sendCMD(sock, "get_tcp_pose")
    print(result)

    suc, result ,id=sendCMD(sock,"setOutput",{"addr":0,"status":0})
    
    time.sleep(1.5)
    print ( result )

    # If servo is on, turn it off
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 1:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 0})


         
         
