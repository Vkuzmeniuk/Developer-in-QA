import subprocess, psutil, datetime, time
import xml.etree.ElementTree as ET
def grab_logs(program,inter_logs):
    open_program = subprocess.Popen(program)
    pid = open_program.pid
    process = psutil.Process(pid)
    pname = process.name()
    root = ET.Element(str(pname))
    while psutil.pid_exists(pid):
        dt_now = datetime.datetime.now()
        subroot = ET.Element("Timestamp", name=str(dt_now))
        root.append(subroot)
        ET.SubElement(subroot,"pid", name="PPID").text = str(pid)
        ET.SubElement(subroot,"cpu_percent", name="CPU load").text = str(process.cpu_percent())
        ET.SubElement(subroot,"wset", name="Working set").text = str(process.memory_info().wset)
        ET.SubElement(subroot,"private", name="Private bytes").text = str(process.memory_info().private)
        ET.SubElement(subroot,"handles", name="Open handles").text = str(process.num_handles())
        # log = f"Time stamp: {dt_now}; Process name: {pname} PPID: {pid};  CPU load: {process.cpu_percent()}; Working Set: {process.memory_info().wset}; Private Bytes: {process.memory_info().private}; Open handles: {process.num_handles()};"
        # print(log)
        time.sleep(inter_logs)
    tree = ET.ElementTree(root)
    tree.write("logs.xml")
program = input("Enter file name with full path: ")
inter_logs = int(input("Time interval for logging(in sec): "))
grab_logs(program, inter_logs)