import psutil,wmi,pprint,time,string
print("Chinoumlo_soft-Psutil_time Ver0.1.0")
c=wmi.WMI()
CPU_con=c.Win32_Processor()
for cpu in CPU_con:
    print("CPU名称:"+cpu.Name)
print("CPU逻辑/物理核心数量:"+str(psutil.cpu_count())+"/"+str(psutil.cpu_count(logical=False)))
for diskpont in psutil.disk_partitions():
        print("Disk "+diskpont.device+" 使用率:"+"{}%".format(psutil.disk_usage(diskpont.device).percent))
while True:
    print("CPU使用率:"+"{:.1f}%".format(psutil.cpu_percent()*10))
    print("Memory使用率:"+"{:.1f}%".format(psutil.virtual_memory().percent))
    
    time.sleep(1)
