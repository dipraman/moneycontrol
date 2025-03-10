import socket
import json
import time
import sys
import copy

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

    robot_ip = "192.168.1.200"
    conSuc, sock = connectETController(robot_ip)

    P000 = [0, -90, 90, -90, 90, 0]
    jbi_filename="rt"

    # If servo is off, turn servo on
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 0:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 1})
        print("servo on")


    suc, result, id = sendCMD(sock, "setSpeed", {"value": 20})
    

    suc, result, id = sendCMD(sock, "get_tcp_pose")
    print(result)

    botle1_postion=[235.01141305661722, -252.91280417450878, 77.94909674217257, -1.5203197776779127, 0.08026867099989163, 0.24848573699502394]
    botle2_postion=copy.deepcopy(botle1_postion)
    botle2_postion[0]-=130
    
    botle2_postion_top=copy.deepcopy(botle2_postion)
    botle2_postion_top[2]+=100
    

    home_pos=[92.77712697939901, -333.21414338121645, 295.4368253751115, -1.5324794176884242, 0.10238945100503777, 0.25035378560372745] 
    
    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": home_pos, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByJoint", {"targetPos": pose1, "speed":20, "acc":50, "dec":50})
    print("home position",result)
    time.sleep(15)

    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": botle2_postion_top, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByJoint", {"targetPos": pose1, "speed":20, "acc":70, "dec":50})
    print("bottle 2 position top",result)
    time.sleep(10)
    
    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": botle2_postion, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 200, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    print("bottle 2 position",result)
    print(botle2_postion)
    time.sleep(10)
    

    suc, result ,id=sendCMD(sock,"setOutput",{"addr":0,"status":1})
    print ( result )
    time.sleep(1.5)


    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": botle2_postion_top, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 200, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    print("bottle 2 position top", result)
    time.sleep(7)
    

    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": home_pos, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByJoint", {"targetPos": pose1, "speed":20, "acc":50, "dec":50})
    print("home position",result)
    time.sleep(7)



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


    suc, result ,id=sendCMD(sock,"setOutput",{"addr":0,"status":0})
    
    time.sleep(1.5)
    print ( result )
    # If servo is on, turn it off
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 1:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 0})
