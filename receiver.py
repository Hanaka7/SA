import boto3
from threading import Thread
import tkinter as tk


class receiver:
    def __init__(self):
        self.drawUI()
        self.init_conn()
        self.register_timer()
        self.window.mainloop()

    def init_conn(self):
        self.sta = '0'
        self.msgBox.insert('end', '开始连接……\n', 'black')
        self.conn = RecvConn()
        result = self.conn.init('test1.fifo')
        if result == 0:
            self.msgBox.insert('end', '连接成功\n将显示接受的消息\n\n', 'black')
        else:
            self.msgBox.insert('end', '连接失败请关闭重试\n', 'black')

    def change_send(self):
        self.sta = str((int(self.sta) + 1) % 3)
        self.channelLabel.config(text='频道' + self.sta)

    def register_timer(self): #500ms调用一次 刷新接受信息
        self.conn.recv(self.sta, self.msgBox)
        self.window.after(500, self.register_timer)

    def drawUI(self):
        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.title('接收者')
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        frame_top = tk.Frame(self.window, width=600, height=560, bg='white')
        frame_bottom = tk.Frame(self.window, width=600, height=40)

        self.msgBox = tk.Text(frame_top)
        self.changeButton = tk.Button(frame_bottom, text='更换消息频道',command=self.change_send)
        self.channelLabel = tk.Label(frame_bottom, text='频道0')
        vbar = tk.Scrollbar(frame_top, orient=tk.VERTICAL)

        self.msgBox['yscrollcommand'] = vbar.set
        vbar['command'] = self.msgBox.yview

        frame_top.grid(row=0, column=0, padx=3, pady=5)
        frame_bottom.grid(row=2, column=0, padx=3, pady=5)

        frame_top.grid_propagate(0)
        frame_bottom.grid_propagate(0)

        self.msgBox.tag_config('green', foreground='#008B00')
        self.msgBox.tag_config('red', foreground='#ff0000')

        self.msgBox.place(x=0,width=600,height=560)
        self.changeButton.grid(row=2, column=1)
        self.channelLabel.grid(row=2, column=2)
        vbar.place(x=580, width=20, height=560)

    def on_close(self):
        self.window.destroy()


class RecvConn:
    def init(self, QueueName):
        try:
            self.sqs = boto3.resource('sqs')
            self.queue = self.sqs.get_queue_by_name(QueueName=QueueName)
            return 0
        except Exception as e:
            print(e)
            return 2

    def recv(self, chan, box):
        t = Thread(target=self.conn, args=(chan, box,))
        t.start()

    def conn(self, chan, box):
        for msg in self.queue.receive_messages(MessageAttributeNames=['Channel']):
            if msg.message_attributes is not None:
                chan_id = msg.message_attributes.get('Channel').get('StringValue')
                if chan_id == chan:
                    msgbody = msg.body.split('\n')#对字符串切片变成字符数组
                    box.insert('end', 'Receiver{}:'.format(chan), 'blue') #接收者
                    #因为用range从1到尾，数组中第一个元素单独打印然后进入range循环
                    box.insert('end', msgbody[0]+'\n', 'blue')
                    for i in range(1, len(msgbody)):
                        box.insert('end', msgbody[i]+'\n')

                    msg.delete()


if __name__ == '__main__':
    receiver = receiver()