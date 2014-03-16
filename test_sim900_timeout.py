# -*- coding: utf-8 -*-
import time
import serial

def sim900sendat(port, timeout):
    port.write("AT\r")
    port.timeout = (int)(timeout / 1000)
    port.interCharTimeout = 0.02

    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))
    if response.find("OK\r\n") != -1 :
        return True
    else :
        print("sim900 fail to connect")
        return False

def sim900sendcgatt(port, timeout) :
    port.write("AT+CGATT?\r")
    port.timeout = (int)(timeout / 1000)
    port.interCharTimeout = 0.02

    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))

    if response.find("OK\r\n") != -1 :
        # 存在响应，并进行处理
        if response.find("+CGATT: 1") != -1 :
            return True
        else:
            return False
    else :
        print("sim900 fail to connect")
        return False

def sim900sendconnect(port, timeout) :

    method = "TCP"
    host = "api.yeelink.net"
    ipport = "80"
    atcmd = "AT+CIPSTART=\"%s\",\"%s\",\"%s\"\r" %(method, host, ipport)

    print(atcmd)        # 打印命令
    port.write(atcmd)
    port.timeout = 2    # 固定时间
    port.interCharTimeout = 0.02

    # 等待OK
    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))

    if response.find("OK\r\n") != -1 :
        # 存在响应，并进行处理
        # print(response)
        pass
    else :
        print("sim900 fail to connect")
        return False

    # 等待CONNECT OK
    port.timeout = timeout / 1000
    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))

    if response.find("CONNECT OK\r\n") != -1 :
        return True
    else :
        print("Connect Error")
        return False

def sim900sendhttprequest(port, timeout) :
    # 请求内容
    httprequest = "GET /v1.0/device/1949/sensor/2511/datapoints HTTP/1.1\r\n"
    httprequest += "Host: api.yeelink.net\r\n"
    httprequest += "U-ApiKey:ffa3826972d6cc7ba5b17e104ec59fa3\r\n"
    httprequest += "\r\n\r\n"

    atcmd = "AT+CIPSEND=%d\r" %(len(httprequest))

    print(atcmd)        # 打印命令
    port.write(atcmd)
    port.timeout = timeout / 1000
    port.interCharTimeout = 0.02

    # 等待>
    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))

    if response.find(">") != -1 :
        pass
    else :
        print("cmd Error")
        return False

    port.write(httprequest)
    # 等待send OK
    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))

    if response.find("SEND OK\r\n") != -1 :
        pass
    else :
        print("Send Fail")
        return False

    time.sleep(0.5)

    httpresponse = ""
    port.interCharTimeout = 0.05
    httpresponse = port.read(1024)
    print("----------")
    print(httpresponse)
    print("----------")

def sim900sendshut(port, timeout) :
    port.write("AT+CIPSHUT\r")
    port.timeout = (int)(timeout / 1000)
    port.interCharTimeout = 0.02

    response = ""
    starttick = time.time()
    response = port.read(64)
    finishtick = time.time()
    print(response)
    print("speed time %.2fs" %(finishtick - starttick))
    if response.find("SHUT OK\r\n") != -1 :
        return True
    else :
        print("sim900 fail to connect")
        return False


def main():
    # 打开串口3，请根据实际情况修改
    port = "COM3"

    # 试图打开串口
    print("open serial port")
    try:
        serialport = serial.Serial(port, 9600)
    except:
        print("serial port open fail")
        print("try to close the program")
        exit()
    # 必要的延时，产生的原因可能是SIM900的自适应串口
    time.sleep(0.1)

    sim900sendat(serialport, 2000)
    sim900sendcgatt(serialport, 2000)
    sim900sendconnect(serialport, 20000)
    sim900sendhttprequest(serialport, 5000)
    sim900sendshut(serialport, 5000)

    # 关闭串口
    print("close serialport")
    serialport.close()

if __name__ == '__main__':
    main()
