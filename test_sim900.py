# -*- coding: utf-8 -*-
import serial
import time

def waitresponse(port, accept, timeout):
    # 10ms 检查一次串口接收内容
    timetick = 0.01
    # 等待时间间隔
    timecount = (int)((timeout / 1000) / timetick)

    receive = ''
    for i in range(0, timecount) :
        # 延时10ms
        time.sleep(timetick)

        # 获得长度
        receivelen = port.inWaiting()
        if receivelen != 0 :
            # 读取并连接字符串
            receive += port.read(receivelen)
            # 查找到目标内容
            if receive.find(accept) >= 0 :
                break

    # 返回接收内容
    return receive

def sendatcmd(port, cmd, accept, timeout):
    # 发送AT指令
    port.write(cmd)

    # 等待期望内容
    response = ''
    response = waitresponse(port, accept, timeout)
    return response


# 打开串口3，请根据实际情况修改
port = "COM3"

serialport = serial.Serial(port, 9600)
# 必要的延时，产生的原因可能是SIM900的自适应串口
time.sleep(0.1)

print("=> send AT")
response = ''
atcmd = "AT\r"
response = sendatcmd(serialport, atcmd, "OK\r\n", 3000)
if len(response) != 0 :
    print(response)

print("=> send AT+CGATT?")
atcmd = "AT+CGATT?\r"
response = sendatcmd(serialport, atcmd, "OK\r\n", 5000)
# 需要进行一些判断 判断是否附着网络
if len(response) != 0 :
    print(response)
    if response.find("+CGATT: 1") > 0 :
        print("=> AT+CGATT Pass")

print("=> send CONNECT")

method = "TCP"
host = "api.yeelink.net"
port = "80"
atcmd = "AT+CIPSTART=\"%s\",\"%s\",\"%s\"\r" %(method, host, port)
print(atcmd)

# 最长等待时间为20S
# 记录开始时间
startTime = time.time()
response = sendatcmd(serialport, atcmd, "CONNECT OK\r\n", 20000)
# 需要进行一些判断 是否连接成功
if len(response) != 0 :
    stopTime = time.time();
    print("connect speed time %.2fs" %(stopTime - startTime))
    print(response)

# HTTP请求内容
httprequest = "GET /v1.0/device/1949/sensor/2511/datapoints HTTP/1.1\r\n"
httprequest += "Host: api.yeelink.net\r\n"
httprequest += "U-ApiKey:ffa3826972d6cc7ba5b17e104ec59fa3\r\n"
httprequest += "\r\n\r\n"

# 发送内容
print("=> send SEND")
atcmd = "AT+CIPSEND=%d\r" %(len(httprequest))
print(atcmd)
# 最长等待时间为5S
response = sendatcmd(serialport, atcmd, ">", 5000)
if len(response) != 0 :
    print(response)

# 发送请求
print("=> send Payload")
print(httprequest)
response = sendatcmd(serialport, httprequest, "SEND OK\r\n", 5000)
if len(response) != 0 :
    print(response)

# 等待一些时间 读取内容

# serialport.timeout = 5
time.sleep(0.5)
# 设置内部间隔时间
serialport.interCharTimeout = 0.05
httpresponse = serialport.read(1024)
if httpresponse != '':
    print("Http Response")
    print("--------------------")
    print(httpresponse)
    print("--------------------")

print("send close cmd")
atcmd = "AT+CIPSHUT\r"
print(atcmd)
response = sendatcmd(serialport, atcmd, "SHUT OK\r\n", 5000)
# 需要进行一些判断 是否连接成功
if len(response) != 0 :
    print(response)

# 关闭串口
print("close serialport")
serialport.close()
