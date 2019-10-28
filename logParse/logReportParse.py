#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import json
import websocket
try:
    import thread
except ImportError:
    import _thread as thread




# infolist=socket.getaddrinfo('gogogo.wemomo.com', 'www')
# pprint(infolist)
# info = infolist[1]  # per standard recommendation, try the first one
# socket_args = info[0:3]
# address = info[4]
#
# print(socket_args)
# print(address)

# 使用库：https://pypi.org/project/websocket_client/
# 参考1： https://juejin.im/post/5c80b768f265da2dae514d4f

# 设置默认的账号
accountString = "663221001"
list = []


def parseResponse(data):
    if(data['domain'] == "live-log.immomo.com"):
        # print("live-log: "+json.dumps(data))
        try:
            print(data['time'] + " ====== " + data['domain'] +", " + data['request']['publisherType'] +", " + data['request']['type'])
            list.append(time.mktime(time.strptime(data['time'], '%Y-%m-%d %H:%M:%S')))

            if(len(list) == 10):
                print("10个触发计算========：")
                for i in range(10):
                    if ((i + 1) >= 10):
                        break;
                    print("时间差："+ str(list[i + 1] - list[i]))
                print("========10个触发计算结束")
                list[:] = []
        except Exception as e:
            # print("error:" + str(e))
            pass

    if("/v3/room/p/querypub" in data['url']):
        # print("querypub: "+json.dumps(data))
        print("queryPub下发推流类型：" + str(data['response']['data']['pub']['agora']['push_type']))


def on_message(ws, message):
    # print(str(message))
    data = json.loads(message)
    # print(data['domain'])
    parseResponse(data)


def on_error(ws, error):
    print(str(error))

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(1):
            time.sleep(1)
            ws.send(accountString)
        time.sleep(1)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    try:
        accountString = str(sys.argv[1])
    except Exception as e:
        pass

    print("您设置的抓取的账号为： "+ accountString)

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://gogogo.wemomo.com/api/websocket/tunnel",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close);

    ws.on_open = on_open
    ws.run_forever()
