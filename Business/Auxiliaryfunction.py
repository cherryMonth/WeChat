#coding=utf-8
from DataProcess.DataProcess import DataProcess
import time
'''

此模块对　出勤情况历史统计　出勤成绩输出　出勤情况随堂（实时）统计　学生信息维护　请假认定 考勤规则的指定

'''

class Auxiliaryfunction(object):

    def addset(self,key):
        info={}
        info['TeacherID']=key
        print 'Please enter the distance to start the check on how long it is to be (Company ：(0-20)minute)！'
        info['autolate']=self.getresult()
        print 'Please enter the distance to start the check on how long it is to be absence (Company :(0-20)minute)!'
        info['autoabsence']=self.getresult()

        if info['autolate']<=info['autoabsence']:
            print '缺勤的等待时间必须大于迟到的等待时间'
            return None

        print 'Please enter the distance to start the random check on how long it is to be late (Company ：(0-20)minute)！'
        info['randomlate'] = self.getresult()
        print 'Please enter the distance to start the random check on how long it is to be absence (Company :(0-20)minute)!'
        info['randomabsence'] = self.getresult()
        if info['randomlate']<=info['randomabsence']:
            print '缺勤的等待时间必须大于迟到的等待时间'
            return None

        info['Type']='False'
        return DataProcess(target=DataProcess.update,args=('../InData/set.csv','w',[info])).run()

    def read(self,key):

        rule=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/set.csv',{'TeacherID':key,'Type':'True'})).run()
        if not rule:
            rule={'TeacherID':key,'autolate':'3','autoabsence':'3','randomlate':'3','randomabsence':'3','Type':'True'}
            print '您当前使用的是默认规则!'
        return rule

    def ruleset(self,key):

        rules = DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/set.csv', {'TeacherID': key})).run()
        if not rules:
            print '您当前没有创建自定义规则'
            return False
        print '请输入您需要选择的规则序号'
        for rule in rules:
            print rule

        index=input()
        if index<1 or index>len(rules):
            print '您输入的结果不合法'
            return False

        for rule in rules:
            if rule['TeacherID'] == rules[index-1]['TeacherID']:
                rule['Type']='True'
            else:
                rule['Type']='False'

        return DataProcess(targe=DataProcess.update,args=('../InData/set.csv','w',rules)).run()



    def getresult(self):
        while True:
            num=raw_input()
            try:
                num=float(num)
            except TypeError and ValueError:
                print 'You have entered an invalid format. Please enter a floating point number!'
                continue

            if num<=0 or num>20 :
                print 'Exceeded maximum accommodation !'
                time.sleep(1)
            else:
                return  num

if __name__=='__main__':
    #Auxiliaryfunction().addset('asdasd')
    Auxiliaryfunction().ruleset('asdasd')
    print Auxiliaryfunction().read('asdasd')