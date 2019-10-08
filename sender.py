import boto3
import tkinter as tk
import time
from threading import Thread


class sender:

    def __init__(self):
        self.drawUI()
        self.init_conn()
        self.window.mainloop()

    def init_conn(self):
        self.sta = '0'
        self.msgBox.insert('end', '开始连接……\n', 'black')
        self.conn = SendConnect()
        result = self.conn.init('test1.fifo')
        if result == 0:
            self.msgBox.insert('end', '连接成功\n可以发送消息啦\n\n', 'black')
        else:
            self.msgBox.insert('end', '连接失败请重试\n', 'black')

    def send(self):
        msg = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n '   #返回本地时间 年月日 时分秒
        self.msgBox.insert("end", 'Sender{}:'.format(self.sta), "green") #发送人
        self.msgBox.insert("end", msg, "green")#时间
        self.msgBox.insert("end", self.sendBox.get('0.0', "end"))#发送信息
        msg += self.sendBox.get('0.0', "end")
        self.sendBox.delete('0.0', "end")#清空
        self.conn.send(msg, self.sta)

    def changeSend(self):  #发送频道切换
        self.sta = str((int(self.sta) + 1) % 3)   #三个频道012
        self.channelLabel.config(text='频道'+self.sta)

    def drawUI(self):
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False) #不可缩放
        self.window.title('发布消息窗口')
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        frame_top = tk.Frame(self.window, width=600, height=360, bg='white')
        frame_center = tk.Frame(self.window, width=600, height=200, bg='white')
        frame_bottom = tk.Frame(self.window, width=600, height=40)

        self.msgBox = tk.Text(frame_top)
        self.sendBox = tk.Text(frame_center)
        self.sendButton = tk.Button(frame_bottom, text='发送', command=self.send)
        self.changeButton = tk.Button(frame_bottom, text='更换消息频道', command=self.changeSend)
        self.channelLabel = tk.Label(frame_bottom, text='频道0')
        vbar = tk.Scrollbar(frame_top, orient=tk.VERTICAL)  #滚动窗口滑条

        self.msgBox['yscrollcommand'] = vbar.set
        vbar['command'] = self.msgBox.yview

        #grid 布局
        frame_top.grid(row=0, column=0, padx=3, pady=5)
        frame_center.grid(row=1, column=0, padx=3, pady=5)
        frame_bottom.grid(row=2, column=0, padx=3, pady=5)

        frame_top.grid_propagate(0)
        frame_center.grid_propagate(0)
        frame_bottom.grid_propagate(0)

        self.msgBox.tag_config('green', foreground='#008B00')
        self.msgBox.tag_config('red', foreground='#ff0000')

        self.msgBox.place(x=0,width=600,height=360)
        self.sendBox.grid()
        self.sendButton.grid(row=2,column=0)
        self.changeButton.grid(row=2,column=1)
        self.channelLabel.grid(row=2,column=2)
        vbar.place(x=580, width=20, height=360)

    def on_close(self):
        self.window.destroy()


class SendConnect:
    def init(self, QueueName):
        try:
            self.sqs = boto3.resource('sqs')
            self.queue = self.sqs.get_queue_by_name(QueueName=QueueName)
            return 0
        except Exception as e:
            print(e)
            return 2

    def send(self, msg, chan):
        t = Thread(target=self.conn, args=(msg, chan,))
        t.start()

    def conn(self, msg, chan):
        attributes = {
            'Channel': {
                'StringValue': chan,
                'DataType': 'String'
            }
        }
        self.queue.send_message(MessageBody=msg, MessageAttributes=attributes, MessageGroupId=chan)


if __name__ == '__main__':
    sender = sender()