from typing import List

from score_search.data.process import DataProcess
from score_search.grade.schoolTerm import SchoolTerm
from score_search.grade.student import Student


class Score:
    def __init__(self, student: Student, schoolTerm: SchoolTerm, dataProcessType: int = DataProcess.Web):
        self.student: Student = student
        self.schoolTerm: SchoolTerm = schoolTerm
        self.dataProcessType = dataProcessType
        self.scores: List[List[str]] = self.handleScores()

    # 得到某个学生某个学期的成绩(包括班别，姓名，考号）
    def handleScores(self) -> List[List[str]]:
        dataProcess = DataProcess \
            .constructDataProcess(self.student.examNumber, self.schoolTerm, self.dataProcessType)
        basicInfo, cleanData = dataProcess.handleData()
        oneStuScores = []
        for examTimes in range(len(cleanData)):
            anExamData = cleanData[examTimes]
            termScores = self.schoolTerm.specificScores(anExamData, self.dataProcessType)
            # print(f"第{examTimes + 1}次月考")
            # print(termScores)
            if not termScores:
                continue
            oneStuScores.append(basicInfo + termScores)
        return oneStuScores

    @staticmethod
    # 四次月考一个班级的每个学生考试成绩
    def handleClassScores(schoolTerm: SchoolTerm, classNumber: int, dataProcessType: int = DataProcess.Web) -> List[
        List[List]]:
        totalExamTimes = schoolTerm.totalExamTimes
        classScores = [[] for _ in range(totalExamTimes)]
        for j in range(1, schoolTerm.seatCount):
            try:
                student = Student(schoolTerm.enrollYear, classNumber, j)
                stuScore = Score(student, schoolTerm, dataProcessType)
                for i in range(totalExamTimes):
                    classScores[i].append(stuScore.scores[i])
            except Exception as e:
                print(f'出现异常{e}')
                # print(f'{classNumber}班{j}学号的同学有错误')
                # writeError(f'http://116.11.184.151:3288/cjcx%5E&/daochu.asp?tb=studinfo{grade.year}{grade.schoolTerm}'
                #            f'&kaohao={score.examNumber}')
                continue
        print(f'{classNumber}班已经完成')
        return classScores

    @staticmethod
    # 这里经过处理也分文理科了
    def handleAllScores(schoolTerm: SchoolTerm, dataProcessType: int = DataProcess.Web) -> List[List[List[List]]]:
        totalExamTimes = schoolTerm.totalExamTimes
        allStuScores = [[] for _ in range(totalExamTimes)]
        for i in range(schoolTerm.totalClassCount):
            data = Score.handleClassScores(schoolTerm, i + 1)
            for j in range(totalExamTimes):
                allStuScores[j] += data[j]

        finalData = []
        for i in range(totalExamTimes):
            finalData.append(schoolTerm.postProcessScore(allStuScores[i], dataProcessType))

        return finalData
