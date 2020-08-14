
# PCB模块
class PCB(object):
    def __init__(self, PID, Parent, Priority):
        self.PID = PID # 名字
        self.Parent = Parent # 父进程
        self.Children = []  # 子进程数组
        self.Priority = Priority # 优先级 0,1,2

        # 状态相关
        self.Type = None  # 状态 0（ready）, 1（block）
        self.TypeNext = None  # 状态链表

        # 资源相关
        self.Resources = {"R1": 0, "R2": 0, "R3": 0, "R4": 0} # 资源字典
        self.WaitRID = None # 等待的资源的RID
        self.WaitRID_num = 0 # 等待的资源的数量
        self.RSNext = None # wait_list

# RCB模块
class RCB(object):
    def __init__(self, RID, n, Wait_list):
        self.RID = RID #
        self.K = n
        self.Status = n
        self.Wait_list = Wait_list

# 进程状态链表
class Process_List(object):
    def __init__(self):
        self.head = None
        self.length = 0

# 资源等待链表
class Wait_list(object):
    def __init__(self):
        self.head = None
        self.length = 0


class OS(object):
    # 初始化
    def __init__(self):
        self.ResourceList = ["R1","R2","R3","R4"]
        self.Run = None
        self.Init()

    # Init函数，
    def Init(self):
        # 初始化状态链表
        self.Process_0_List = Process_List()
        self.Process_1_RList = Process_List()
        self.Process_2_RList = Process_List()
        self.Process_1_BList = Process_List()
        self.Process_2_BList = Process_List()

        # 初始化资源等待链表
        R1_Wait_list = Wait_list()
        R2_Wait_list = Wait_list()
        R3_Wait_list = Wait_list()
        R4_Wait_list = Wait_list()

        # 初始化4种资源极其数量
        self.RCB_R1 = RCB("R1", 1, R1_Wait_list)
        self.RCB_R2 = RCB("R2", 2, R2_Wait_list)
        self.RCB_R3 = RCB("R3", 3, R3_Wait_list)
        self.RCB_R4 = RCB("R4", 4, R4_Wait_list)

    # 打印状态链表
    def PrintTypeList(self,List):
        cur = List.head
        while cur is not None:
            print(cur.PID," ",end="")
            cur = cur.TypeNext
        print()

    # 打印资源等待链表
    def PrintRSList(self,List):
        cur = List.head
        while cur is not None:
            print(cur.PID," ",end="")
            cur = cur.RSNext
        print()

    def list_ready(self):
        print("2:",end="")
        self.PrintTypeList(self.Process_2_RList)
        print("1:",end="")
        self.PrintTypeList(self.Process_1_RList)
        print("0:", end="")
        self.PrintTypeList(self.Process_0_List)

    def list_res(self):
        print("R1 ", self.RCB_R1.Status)
        print("R2 ", self.RCB_R2.Status)
        print("R3 ", self.RCB_R3.Status)
        print("R4 ", self.RCB_R4.Status)

    def list_block(self):
        print("R1 ",end="")
        self.PrintRSList(self.RCB_R1.Wait_list)
        print("R2 ", end="")
        self.PrintRSList(self.RCB_R2.Wait_list)
        print("R3 ", end="")
        self.PrintRSList(self.RCB_R3.Wait_list)
        print("R4 ", end="")
        self.PrintRSList(self.RCB_R4.Wait_list)

    # 根据PID查找进程并返回（遍历4个链表）
    def Find_PCB(self, PID):
        cur1 = self.Process_1_RList.head
        while cur1 is not None:
            if cur1.PID == PID:
                return cur1
            cur1 = cur1.TypeNext

        cur1 = self.Process_2_RList.head
        while cur1 is not None:
            if cur1.PID == PID:
                return cur1
            cur1 = cur1.TypeNext

        cur1 = self.Process_1_BList.head
        while cur1 is not None:
            if cur1.PID == PID:
                return cur1
            cur1 = cur1.TypeNext

        cur1 = self.Process_2_BList.head
        while cur1 is not None:
            if cur1.PID == PID:
                return cur1
            cur1 = cur1.TypeNext

        print("未找到",PID,"进程")
        return None

    # 根据RID获取RCB并返回
    def Get_RCB(self, RID):
        if RID == "R1":
            R = self.RCB_R1
            return R
        if RID == "R2":
            R = self.RCB_R2
            return R
        if RID == "R3":
            R = self.RCB_R3
            return R
        if RID == "R4":
            R = self.RCB_R4
            return R
        print("未找到",RID,"资源")
        return None

    # 撤销进程时，将进程从状态链表清除
    def Remove(self, Process, List):
        cur = List.head
        pre = None
        while cur is not None:
            if cur.PID == Process.PID:
                if cur == List.head:
                    List.head = cur.TypeNext
                else:
                    pre.TypeNext = cur.TypeNext
                # 链表长度减1
                List.length -= 1
                return
            pre = cur
            cur = cur.TypeNext

    # 撤销进程时，将进程从资源等待链表清除
    def RemoveWait(self, Process, List):
        cur = List.head
        pre = None
        while cur is not None:
            if cur.PID == Process.PID:
                if cur == List.head:
                    List.head = cur.RSNext
                else:
                    pre.RSNext = cur.RSNext
                # 链表长度减1
                List.length -= 1
                return
            pre = cur
            cur = cur.TypeNext

    # 撤销进程时，将进程占用的所有资源释放
    def FreeResource(self, Process):
        self.RCB_R1.Status += Process.Resources["R1"]
        self.RCB_R2.Status += Process.Resources["R2"]
        self.RCB_R3.Status += Process.Resources["R3"]
        self.RCB_R4.Status += Process.Resources["R4"]

    # 将进城插入资源等待进程链表队尾
    def InsertWait(self, Process, List):
        cur = List.head
        if cur is None:
            List.head = Process
            List.length += 1
        else:
            while cur.RSNext is not None:
                cur = cur.RSNext
            cur.RSNext = Process
            List.length += 1

    # 将进城插入进程状态链表队尾
    def Insert(self, Process, List):
        cur = List.head
        if cur is None:
            List.head = Process
            List.length += 1
        else:
            while cur.TypeNext is not None:
                cur = cur.TypeNext
            cur.TypeNext = Process
            List.length += 1

    # 撤销进程的子孙进程
    def Kill_Tree(self, Process):

        # 获取进程状态及优先级
        Type = Process.Type
        priority = Process.Priority

        # 根据进程状态及优先级，清理状态链表
        if Type == 0 and priority == 1:
            self.Remove(Process, self.Process_1_RList)
        elif Type == 0 and priority == 2:
            self.Remove(Process, self.Process_2_RList)
        elif Type == 1 and priority == 1:
            self.Remove(Process, self.Process_1_BList)
        elif Type == 1 and priority == 2:
            self.Remove(Process, self.Process_1_BList)

        # 资源链表清理
        self.RemoveWait(Process, self.RCB_R1.Wait_list)
        self.RemoveWait(Process, self.RCB_R2.Wait_list)
        self.RemoveWait(Process, self.RCB_R3.Wait_list)
        self.RemoveWait(Process, self.RCB_R4.Wait_list)

        for RID in Process.Resources:
            if Process.Resources[RID] != 0:
                self.Release(Process ,RID, Process.Resources[RID])


        for child in Process.Children:
            # 递归
            self.Kill_Tree(child)

        # 彻底删除进程
        del(Process)

    # 根据优先级，切换进程
    def Scheduler(self):
        if self.Process_2_RList.head is not None:
            self.Run = self.Process_2_RList.head
            return
        elif self.Process_1_RList.head is not None:
            self.Run = self.Process_1_RList.head
            return
        else:
            self.Run = self.Process_0_List.head

    # 创建init进程
    def Init_Process(self):
        init = PCB("init", None, 0)
        init.Type = 0
        self.Run = init
        print("init process is running")
        self.Process_0_List.head = init

    # 创建进程
    def Create(self, PID, Priority):
        # 获取正在运行模块
        RUN = self.Run
        # 创建进程模块
        P = PCB(PID, RUN, Priority)
        # 把进程加入父进程的子进程列表
        P.Parent.Children.append(P)
        # 初建进程状态默认为ready
        P.Type = 0

        # 如果新建进程优先级大于正在运行的进程
        if P.Priority > RUN.Priority:

            # 根据不同优先级插入不同readyList头部
            if P.Priority == 1:
                if self.Process_1_RList.head is not None:
                    P.TypeNext = self.Process_1_RList.head
                    self.Process_1_RList.head = P
                    self.Process_1_RList.length = self.Process_1_RList.length + 1
                else:
                    self.Process_1_RList.head = P
                    self.Process_1_RList.length = self.Process_1_RList.length + 1

            elif P.Priority == 2:
                if self.Process_2_RList.head is not None:
                    P.TypeNext = self.Process_2_RList.head
                    self.Process_2_RList.head = P
                    self.Process_2_RList.length = self.Process_2_RList.length + 1
                else:
                    self.Process_2_RList.head = P
                    self.Process_2_RList.length = self.Process_2_RList.length + 1
            else:
                print("优先级错误")
                return

                # 切换进程
            self.Run = P
            print("process ",self.Run.PID," is running")

        # 如果新建的进程优先级低于正在运行的进程，则根据进程优先级插入不同readyList的队尾
        else:
            if P.Priority == 1:
                self.Insert(P, self.Process_1_RList)
            elif P.Priority == 2:
                self.Insert(P, self.Process_2_RList)
            else:
                print("优先级错误")
                return
            print("process ", self.Run.PID, " is running")

    # 撤销进程
    def Distroy(self, PID):
        # 根据进程PID获取进程
        P = self.Find_PCB(PID)

        # 如果撤销的进程是正在运行的进程
        if self.Run == P:
            # 撤销进程及其子进程
            self.Kill_Tree(P)
            # 进程切换
            self.Scheduler()

        else:
            self.Kill_Tree(P)
            self.Scheduler()

    # 申请资源
    def Request(self, RID, n):
        # 获取RCB
        R = self.Get_RCB(RID)
        # 获取正在运行的Process
        RUN = self.Run

        # 如果资源剩余数量大于等于申请量，分配资源
        if R.Status >= n:
            RUN.Resources[RID] += n
            R.Status -= n
            print("process ",RUN.PID," requests ",n," ",RID)

        # 如果资源剩余数量大于资源总数，报错
        elif n > R.K:
            print("申请量超过资源总数")
            return

        # 如果资源剩余数量小于申请量，堵塞进程
        else:
            # 状态变成Block
            RUN.Type = 1
            # 记录进程等待资源的RID
            RUN.WaitRID = RID
            # 记录进程等待资源的数量
            RUN.WaitRID_num = n
            # 将进程插入R资源等待链表队尾
            self.InsertWait(RUN, R.Wait_list)
            # 记录PID
            RUN_PID = RUN.PID

            # 根据优先级将进程移出readyList队头，并插入blockList的队尾
            if RUN.Priority == 2:
                self.Process_2_RList.head = self.Process_2_RList.head.TypeNext
                RUN.TypeNext = None
                self.Insert(RUN, self.Process_2_BList)
            if RUN.Priority == 1:
                self.Process_1_RList.head = self.Process_1_RList.head.TypeNext
                RUN.TypeNext = None
                self.Insert(RUN, self.Process_1_BList)

            # 切换进程
            self.Scheduler()
            print("process ",self.Run.PID," is running.","process ",RUN_PID," is blocked.")

    # 释放资源
    def Release(self,Process,RID, n):
        # 获取RCB
        R = self.Get_RCB(RID)
        RUN = self.Run

        # 如果释放资源数量大于进程拥有量，报错
        if n > Process.Resources[RID]:
            print("释放资源总数大于拥有量")
            return
        else:
            # 释放资源
            R.Status += n
            Process.Resources[RID] -= n
            print("release ",RID,".",end="")

            # 检测是否有进程可以从Block态转换成Ready态
            if R.Wait_list.head is not None:
                # 只检测队头的进程
                P = R.Wait_list.head

                # 如果进程等待的资源数小于可用资源数
                if P.WaitRID_num <= R.Status:
                    # 分配资源
                    R.Status -= P.WaitRID_num
                    P.Resources[RID] += P.WaitRID_num
                    P.WaitRID = None
                    P.WaitRID_num = 0
                    P.Type = 0

                    # 将P从资源R的等待队列中移除
                    R.Wait_list.head = R.Wait_list.head.RSNext
                    P.RSNext = None

                    # 将进程从blockList移除，并加入readyList队尾
                    if P.Priority == 2:
                        self.Remove(P, self.Process_2_BList)
                        P.TypeNext = None
                        self.Insert(P, self.Process_2_RList)

                        # 高优先级抢占（被抢占的进程仍在队头）
                        if RUN.Priority == 1 and self.Process_2_RList.head == P:
                                self.Run = P

                    elif P.Priority == 1:
                            self.Remove(P, self.Process_1_BList)
                            P.TypeNext = None
                            self.Insert(P, self.Process_1_RList)
                    else:
                            print("init无资源释放，出错")
                            return
                    print(" wake up process",P.PID)

    # 中断
    def Time_out(self):
        # 获取正在运行的进程
        RUN = self.Run
        RUN_PID = RUN.PID
        # 根据优先级将进程插入readyList队尾
        if RUN.Priority == 2:
            self.Process_2_RList.head = self.Process_2_RList.head.TypeNext
            self.Process_2_RList.length -= 1
            print(self.Process_2_RList.head.PID)
            RUN.Type = 0
            RUN.TypeNext = None
            self.Insert(RUN, self.Process_2_RList)
        elif RUN.Priority == 1:
            self.Process_1_RList.head = self.Process_1_RList.head.TypeNext
            self.Process_1_RList.length -= 1
            RUN.Type = 0
            RUN.TypeNext = None
            self.Insert(RUN, self.Process_1_RList)
        else:
            print("无可用进程")
            return

        # 切换进程
        self.Scheduler()
        if(self.Run.PID == RUN_PID):
            print("process ",self.Run.PID," is running.")
        else:
            print("process ",self.Run.PID," is running.","process ",RUN_PID," is ready.")

# 读取指令并运行
OS = OS()
fr = open("/Users/gong/Desktop/test.txt")
for line in fr:
    s = line.split()
    if s[0] == "init":
        OS.Init_Process()
    elif s[0] == "cr":
        PID = s[1]
        priority = int(s[2])
        OS.Create(PID,priority)
    elif s[0] == "list":
        if s[1] == "ready":
            OS.list_ready()
        elif s[1] == "res":
            OS.list_res()
        elif s[1] == "block":
            OS.list_block()
    elif s[0] == "req":
        RID = s[1]
        n = int(s[2])
        OS.Request(RID, n)
    elif s[0] == "de":
        PID = s[1]
        OS.Distroy(PID)
    elif s[0] == "to":
        OS.Time_out()
    else:
        print("指令出错")

