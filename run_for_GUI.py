from kivy.config import Config
from kivy.app import App
####设置窗口大小不变
Config.set('graphics','resizable',False) 
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.clock import Clock
Window.size = (1200,720)
import wmi,psutil,platform
from pynvml import *

cpu_p = "检测中"
mem_p = "检测中"
gpu_p = "检测中"


 
class LoginScreen(FloatLayout):
    ####运行__init__
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        ####在画布上添加图标
        with self.canvas:
            self.rect = Rectangle(pos=self.pos,size=(1200,750),source="photo/Background.png")
            self.rect = Rectangle(pos=self.pos,size=(888,750),source="photo/ban.png")
            self.rect = Rectangle(pos=(70,615),size=(100,100),source="photo/gdyjxx.png")
            self.rect = Rectangle(pos=(70,300),size=(100,100),source="photo/CPU.png")
            self.rect = Rectangle(pos=(370,300),size=(100,100),source="photo/MEM.png")
            self.rect = Rectangle(pos=(670,300),size=(100,100),source="photo/GPU.png")
            self.rect = Rectangle(pos=(70,115),size=(100,100),source="photo/NET.png")
            self.rect = Rectangle(pos=(370,115),size=(100,100),source="photo/DISK.png")
        #开始计时计划
        self.clocks()
    ####计时计划
    def clocks(self):
        ####每0.5秒运行一次self.update
        Clock.schedule_interval(self.update,0.5)
    ####标签和处理
    def update(self,a):
        global cpu_p
        global mem_p
        global gpu_p
        global net_send
        global net_rcvd
        global disk_read
        global disk_write
        cpu_p = "{:.1f}%".format(psutil.cpu_percent()*1)
        mem_p = "{:.1f}%".format(psutil.virtual_memory().percent)
        gpumeminfo = nvmlDeviceGetMemoryInfo(handle)
        gpu_p = "{:.1f}%".format(gpumeminfo.used / gpumeminfo.total * 100)
        self.clear_widgets()
        self.add_widget(Label(text='固定硬件信息',pos=(-200,305),font_name="fixsa",font_size=40,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='CPU型号 : '+cpu_name,pos=(-200,230),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='RAM数量 : '+str(round((float(psutil.virtual_memory().total) / 1024 / 1024 / 1024), 2))+" GB",pos=(-200,200),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='硬盘使用量 : '+str(diskpercent)+" %",pos=(-200,170),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='硬盘总量 : '+str(round(disktotal))+" GB",pos=(-200,140),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='GPU型号 : '+str(gpuname),pos=(-200,110),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='操作系统 : Windows '+str(platform.win32_ver()[1]),pos=(-200,80),font_name="fixsa",font_size=20,color=(.1,.1,.1,1)))

        cp=Label(text="CPU使用率:"+cpu_p,pos=(-480,-90),font_name="fixsa",font_size=25,color=(.1,.1,.1,1))
        mp=Label(text="Memory使用率:"+mem_p,pos=(-180,-90),font_name="fixsa",font_size=25,color=(.1,.1,.1,1))
        gp=Label(text='GPU(MEM)使用率: '+gpu_p,pos=(120,-90),font_name="fixsa",font_size=25,color=(.1,.1,.1,1))

        self.add_widget(cp)
        self.add_widget(mp)
        self.add_widget(gp)

        self.add_widget(Label(text='接收:'+'{0:.2f} Mb/s'.format((psutil.net_io_counters().bytes_recv - net_rcvd) / 1024 / 1024 *2),pos=(-470,-275),font_name="fixsa",font_size=25,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='发送:'+'{0:.2f} Mb/s'.format((psutil.net_io_counters().bytes_sent - net_send) / 1024 / 1024 *2),pos=(-470,-310),font_name="fixsa",font_size=25,color=(.1,.1,.1,1)))

        self.add_widget(Label(text='读取:'+'{0:.2f} Mb/s'.format((psutil.disk_io_counters().read_bytes - disk_read) / 1024 / 1024 *2),pos=(-180,-275),font_name="fixsa",font_size=25,color=(.1,.1,.1,1)))
        self.add_widget(Label(text='写入:'+'{0:.2f} Mb/s'.format((psutil.disk_io_counters().write_bytes - disk_write) / 1024 / 1024 *2),pos=(-180,-310),font_name="fixsa",font_size=25,color=(.1,.1,.1,1)))

        net_rcvd = psutil.net_io_counters().bytes_recv
        net_send = psutil.net_io_counters().bytes_sent

        disk_read = psutil.disk_io_counters().read_bytes
        disk_write = psutil.disk_io_counters().write_bytes
####根据Kivy的运行流程应该到这里
class Psutil_timeApp(App):
 
    def build(self):
        ####显示LoginScreen的内容
        return LoginScreen()
 
####从这里开始用刑
if __name__ == '__main__':
    c=wmi.WMI()
    CPU_con=c.Win32_Processor()

    ####获取最后一个CPU的名称
    for cpu in CPU_con:
        cpu_name=cpu.Name
    
    ####导入一个字体
    from kivy.core.text import LabelBase
    LabelBase.register(name='fixsa',
                    fn_regular='font/851.ttf',
                    fn_bold='font/851.ttf')

    ####计算全部分区的平均剩余百分率
    disktotle = 0
    for diskpont in psutil.disk_partitions():
        disktotle+=int(psutil.disk_usage(diskpont.device).percent)
    diskpercent = disktotle / 4
    ####计算全部硬盘空间
    disktotal = 0
    for diskpont in psutil.disk_partitions():
        disktotal+=int(psutil.disk_usage(diskpont.device).total)
    disktotal = disktotal/1024/1024/1024
    ####获得GPU名称
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    gpuname = nvmlDeviceGetName(handle)
    ####第一次获得网络IO
    net_rcvd = psutil.net_io_counters().bytes_recv
    net_send = psutil.net_io_counters().bytes_sent
    ####第一次获得硬盘IO
    disk_read = psutil.disk_io_counters().read_bytes
    disk_write = psutil.disk_io_counters().write_bytes
    ####用刑Kivy
    Psutil_timeApp().run()