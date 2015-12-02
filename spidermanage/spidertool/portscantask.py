#!/usr/bin/python
#coding:utf-8
from ThreadTool import ThreadTool
import datetime
import time
import connectpool
import portscantool
import SQLTool,config
from TaskTool import TaskTool
portscantskinstance=None
def getObject():
    global portscantskinstance
    if portscantskinstance is None:
        portscantskinstance=PortscanTask(0)
    return portscantskinstance
class PortscanTask(TaskTool):
    def __init__(self,isThread=1,deamon=True):
        TaskTool.__init__(self,isThread,deamon=deamon)
        self.sqlTool=SQLTool.DBmanager()
        self.connectpool=connectpool.getObject()
        self.portscan=portscantool.Portscantool()
        self.config=config.Config
        self.set_deal_num(5)
    def task(self,req,threadname):
        print threadname+'执行任务中'+str(datetime.datetime.now())

        print req[0],req[1],req[2],req[3]
        if req[3]!='open':
            return ''
        ip=req[1]
        port=req[2]
        print '尝试连接'
        if req[0]=='http' or req[0]=='https':
            if ip[0]=='h':
                address=ip+':'+port
            else:
                address=req[0]+'://'+ip+':'+port
            print address
            ans = self.connectpool.getConnect(address)
        else:
            ans=self.portscan.do_scan(ip,port)
        print ans
        self.sqlTool.connectdb()
        print '尝试插入'
        localtime=str(time.strftime("%Y-%m-%d %X", time.localtime()))
        insertdata=[]
#         insertdata.append((str(ip),port,localtime,str(ans),str(ans),localtime))
        insertdata.append(('str(ip)','port','localtime','str(ans)','str(ans)','str(ans)'))
#         self.sqlTool.inserttableinfo_byparams(self.config.porttable,['ip','port','timesearch','detail' ],insertdata)
                                              
        
        self.sqlTool.inserttableinfo_byparams(self.config.porttable,['ip','port','timesearch','detail'],insertdata,updatevalue=['detail','timesearch'])
        print '插入成功'
        self.sqlTool.closedb()
        print threadname+'任务结束'+str(datetime.datetime.now())
        
        
        
        
        
        return ans

if __name__ == "__main__":
    links = [ 'http://www.bunz.edu.com','http://www.baidu.com','http://www.hao123.com','http://www.cctv.com','http://www.vip.com']
    
    f = searchTask()
    f.set_deal_num(2)
    f.add_work(links)

    #f.start_task()
    while f.has_work_left():
        v,b=f.get_finish_work()
        
    while True:
        pass



