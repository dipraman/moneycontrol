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
    

    center_home_pos=[-383.14251014184714, -92.57099367193219, 309.086942482576, -1.4061676912027903, 0.06385363046518754, -1.4204567349945747]
    pamphlet_pose=[-8.920101388843918, 397.16903105574954, 61.36833799527471, -2.845497469060157, -1.3153512090834774, -1.7783328419834974]
    
    
    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": pamphlet_pose, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByJoint", {"targetPos": pose1, "speed":20, "acc":50, "dec":50})
    print("pamphlet_pose", result)

    time.sleep(15)

    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": center_home_pos, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByJoint", {"targetPos": pose1, "speed":20, "acc":50, "dec":50})
    
    suc, result, id = sendCMD(sock, "get_tcp_pose")
    print(result)
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 1:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 0})

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
    

    center_pos=[-383.1437815674997, -92.56361689594564, 309.08819387324723, -1.4061644445282826, 0.0638615910115111, -1.4204852117698967]

    center_home_pos=[-375.38836926241555, -133.6076324715175, 375.26423458097554, -2.8339364224011874, -1.2619938616454145, -0.24565738007003432]
    pamphlet_pose=[-8.920101388843918, 397.16903105574954, 61.36833799527471, -2.845497469060157, -1.3153512090834774, -1.7783328419834974]
    
    pamphlet_mid=[-210.98760806371442, 332.94481486045487, 309.08494392030485, -1.4061508593213181, 0.06383799091371495, -2.6634927556272263]
    pamphlet_top=[-11.591597698040019, 407.30031204969924, 339.66204274412974, -2.843183107673523, -1.3100180676509057, -1.780557587316304]
    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": pamphlet_mid, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 400, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    time.sleep(6)

    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": pamphlet_pose, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 400, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    time.sleep(6)

    suc, result ,id=sendCMD(sock,"setOutput",{"addr":1,"status":1})
    time.sleep(1.5)


    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": pamphlet_top, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 400, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    time.sleep(6)


    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": center_home_pos, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 400, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    time.sleep(6)




    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": center_pos, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 600, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    suc, result ,id=sendCMD(sock,"setOutput",{"addr":1,"status":0})
    time.sleep(1.5)
    time.sleep(1)
    
    suc, result, id = sendCMD(sock, "get_tcp_pose")
    print(result)
     # If servo is on, turn it off
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 1:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 0})

