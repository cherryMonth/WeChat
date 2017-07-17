#coding=utf-8
from DataProcess.DataProcess import DataProcess
from DataProcess.DataProcess import DataProcess

class maintain(object):

    '''
    手动修改
    手动考勤
    手动设置个人考勤规则
    '''

    def is_can(self,key):
        list=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',key)).run()
        if list or len(list)!=0:
            return False
        return True


    def mainTain_stu(self,key): #手动维护学生信息
        classinfo=DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv',{'TeacherID':key['TeacherID']})).run()
        classlist=set()
        for line in classinfo:
            classlist.add(line['ClassName'])
        classlist=list(classlist)
        stuinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',)).run()

        for stu in stuinfo:
            if stu['ClassID'] not in classlist:
                stuinfo.remove(stu)

        stuID=raw_input('请输入您需要修改学生的学号!')
        info={}
        for stu in stuinfo:
            if stu['StuID']==stuID:
                info=stu
                break
        if not info:
            print '该学生不在你的修改范围之内无法修改!'
            return False


        info=self.get_result(classlist,info)

        error=DataProcess(target=DataProcess.formatcheck,args=([info],{"StuID":'^[\d]{12}$',
                           "StuName":'^[\x80-\xff]{6,18}$',
                           "WeChatID":'^[a-zA-Z0-9_]+$',
                           "ClassID":'[\x80-\xff]+\d{4}$'})).run()

        if DataProcess(target=DataProcess.getresult,args=(error,)).run():
            print error
            print '您输入的格式错误无法修改学生信息!'
            return False

        DataProcess(target=DataProcess.update, args=('../InData/studentInfo.csv','dl',[info])).run()
        print '修改学生信息成功!'
        return DataProcess(target=DataProcess.update, args=('../InData/studentInfo.csv','w',[info])).run()


    def get_result(self,classlist,data):

        sel=raw_input('是否修改学号? (yes or other)')
        if sel=='yes':
            stuID=raw_input('请输入学号!')
            if self.is_can({'StuID':stuID}):
                data['StuID']=stuID
            else:
                print '该学号不唯一无法修改成为此学号!'

        sel = raw_input('是否修改姓名? (yes or other)')
        if sel == 'yes':
            stuName = raw_input('请输入姓名!')
            data['StuName'] = stuName

        sel = raw_input('是否修改微信号? (yes or other)')
        if sel == 'yes':
            WeChatID = raw_input('请输入微信号!')
            if self.is_can({'WeChatID': WeChatID}):
                data['WeChatID'] = WeChatID
            else:
                print '该微信号不唯一无法修改成为此微信号!'

        sel = raw_input('是否修改班级? (yes or other)')
        if sel == 'yes':
            ClassID = raw_input('请输入班级!')
            if ClassID in classlist:
                data['ClassID'] = ClassID
            else:
                print '您输入的班级不在您的维护范围之内无法修改!'

        sel = raw_input('是否修改个人信息特征? (yes or other)')
        if sel == 'yes':
            path = raw_input('请输入特征路径!')
            if self.is_can({'FeaturePath': path}):
                data['FeaturePath'] = path
            else:
                print '该特征不唯一无法修改成为此特征!'

        return data




    def mainTain_info(self,key):#手动维护考勤信息
        seqnum=raw_input('请输入您需要修改哪一次的记录！')
        filename='../InData/'+key['TeacherID']+'_'+key['ClassID']+'_Sum.csv'
        stuinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,)).run()


        if not stuinfo or 'checkin'+seqnum not in stuinfo[0].keys():
            print '该次考勤不存在请检查您的输入!'
            return False

        print '该次学生考勤状态如下:'
        for stu in stuinfo:
            print stu['StuID'] +' : '+stu['checkin'+seqnum]

        stuID=raw_input("请输入你要修改学生的学号!")
        count=0
        stu_info={}
        for stu in stuinfo:
            if stu['StuID']==stuID:
                stu_info=stu
                count=1
                break
        if count==0:
            print '该学生不存在请检查您的输入!'
            return False

        print '该学生的该次的考勤状态 : %s' %(stu_info['checkin'+seqnum])
        stu_info['checkin'+seqnum]=raw_input('请输入你希望修改的值!')
        return DataProcess(target=DataProcess.update,args=(filename,'w',[stu_info],['StuID'])).run()

    def rultSet(self):
        pass

    def readRult(self):
        pass

if __name__=='__main__':
    #maintain({'TeacherID':'2004633','ClassID':'软件工程1401'}).mainTain_info()
    maintain({'TeacherID': '2004633', 'ClassID': '软件工程1401'}).mainTain_stu()