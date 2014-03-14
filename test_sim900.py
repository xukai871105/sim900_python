# -*- coding: utf-8 -*-

import serial
import time

def waitResponse(port, responseStr, timeout):
    # 10ms 检查一次串口接收内容
    timeTick = 0.01
    # 等待时间间隔
    timeCount= (int)((timeout / 1000) / timeTick)
    # print("timeCount：%d" %(timeCount))

    receiveStr = ''
    for i in range(0, timeCount):
        time.sleep(timeTick)
        # print(i)
        # 获得长度
        receiveLen = port.inWaiting()

        if receiveLen != 0 :
            # 读取并连接字符串
            receiveStr += port.read(receiveLen)
            # print(receiveStr)
            # 查看是否包含字符串
            '''
            if cmp(receiveStr, responseStr) == 0 :
                retVal = 1
                # 跳出循环
                print("response OK")
                break
            '''
            if receiveStr.find(responseStr) >= 0 :
                # 查找到目标内容
                return receiveStr
    # print("response Fail")   
    return receiveStr

def sendAtCmd(port, cmd, responseStr, timeout):
    # retVal = 0
    # 发送AT指令
    retStr = ''
    port.write(cmd)
    '''
    # 等待一些时间
    time.sleep(10)

    len = port.inWaiting()
    print("len:%d" %(len))
    if len != 0:
        receiveStr = port.read(len)
        print(receiveStr)
        if cmp(receiveStr, responseStr)== 0:
            print("Response OK")
            retVal = 1
        else:
            print("Response Fail")
            retVal = 0
    '''
    retStr = waitResponse(port, responseStr, timeout)
    return retStr


# 打开串口2，串口2和串口3通过虚拟串口相连
port = "COM9"

serialport = serial.Serial(port, 9600)
# 必要的延时
time.sleep(0.5)
# serialport.flushInput()

print("send at cmd")
retStr = ''
cmdStr = "AT\r"
retStr = sendAtCmd(serialport, cmdStr, "OK\r\n", 3000)

if len(retStr) != 0 :
    print(retStr)
    
print("send cgatt cmd")
cmdStr = "AT+CGATT?\r"
retStr = sendAtCmd(serialport, cmdStr, "OK\r\n", 5000)
# 需要进行一些判断 判断是否附着网络
if len(retStr) != 0 :
    print(retStr)
    
print("send connect cmd")
startTime = time.time()
cmdStr = "AT+CIPSTART=\"TCP\",\"api.yeelink.net\",\"80\"\r"
print(cmdStr)
# 最长等待时间为20S
retStr = sendAtCmd(serialport, cmdStr, "CONNECT OK\r\n", 20000)
# 需要进行一些判断 是否连接成功
if len(retStr) != 0 :
    stopTime = time.time();
    print("connect speed time %.2f" %(stopTime - startTime))
    print(retStr)

requestStr = "GET /v1.0/device/1949/sensor/2511/datapoints HTTP/1.1\r\n"
requestStr += "Host: api.yeelink.net\r\n"
requestStr += "U-ApiKey:ffa3826972d6cc7ba5b17e104ec59fa3\r\n"
requestStr += "\r\n\r\n"

# 发送内容
print("send send cmd")
cmdStr = "AT+CIPSEND={0}\r".format(len(requestStr))
print(cmdStr)
# 最长等待时间为5S
retStr = sendAtCmd(serialport, cmdStr, ">", 5000)
if len(retStr) != 0 :
    print(retStr)

# 发送请求
print("send send payload")
print(requestStr)
retStr = sendAtCmd(serialport, requestStr, "SEND OK\r\n", 5000)
if len(retStr) != 0 :
    print(retStr)

# 等待一些时间 读取内容
'''
time.sleep(5)
responseStr = ''
responseLen = serialport.inWaiting()
if responseLen != 0:
    responseStr = serialport.read(responseLen)
    print(responseStr)
'''
# serialport.timeout = 5
time.sleep(0.5)
# 设置内部间隔时间
serialport.interCharTimeout = 0.05
responseStr = serialport.read(1024)
if responseStr != '':
    print("response")
    print("--------------------")
    print(responseStr)
    print("--------------------")
    print(responseStr.split("\r\n\r\n"))

print("send close cmd")
cmdStr = "AT+CIPSHUT\r"
print(cmdStr)
retStr = sendAtCmd(serialport, cmdStr, "SHUT OK\r\n", 5000)
# 需要进行一些判断 是否连接成功
if len(retStr) != 0 :
    print(retStr)


# 关闭串口
print("close serialport")
serialport.close()



