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
    
    home_pose=[248.13134267944235, 123.35672500105281, 482.4273547512055, -1.5599759750211084, 0.10674175774610391, 1.8027490775570378]
    
    marker_offset=[-78.71182382887204, 355.7145066304951, 175.31454179311427, -1.5262821715724835, 0.1008142513315282, -2.849923059903276]
    marker_pose=[-78.71119240260512, 344.2796008406667, 106.36114181676753, -1.5262808067506395, 0.10082542703500089, -2.849920806507598]
    marker_picked=copy.deepcopy(marker_pose)
    marker_picked[2]+=200
    suc, pose1, id = sendCMD(sock, "inverseKinematic", {"targetPose": home_pose, "referencePos": P000})
    suc, result, id = sendCMD(sock, "moveByLine", {"targetPos": pose1, "speed_type":0, "speed": 900, "cond_type": 0, "cond_num": 7, "cond_value": 1})
    print("home position",result)
     

    
    suc, result, id = sendCMD(sock, "get_tcp_pose")
    print(result)
     # If servo is on, turn it off
    suc, result, id = sendCMD(sock, "getServoStatus")
    if result == 1:
        suc, result, id = sendCMD(sock, "set_servo_status", {"status": 0})

