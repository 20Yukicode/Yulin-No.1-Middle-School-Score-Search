import datetime

from score_search.common.basic import GradeMap
from score_search.data.process import getExamTimes, DataProcess
from score_search.grade.schoolTerm import SchoolTerm
from score_search.grade.score import Score
from score_search.grade.student import Student

from score_search.store.excelStore import storeScores

Yulin_No_1_Middle_School_Establish_Date_Year = 1923


# 注意grade是1-3,schoolTerm的范围是1-6
def nowSchoolTerm(year: int) -> int:
    now = datetime.date.today()
    nowYear = now.year
    nowMonth = now.month
    # 当前年级
    nowGrade = nowYear - year + 1
    temp = 1
    if 3 <= nowMonth <= 7:
        temp = 0
    elif 1 <= nowMonth <= 2:
        nowGrade -= 1
    else:
        pass
    # 当前学期
    schoolTerm = nowGrade * 2 - temp
    return schoolTerm


# 比如2021010001 2  3   1(高二第三学期第二次月考)
# 比如2022010001 1  1   1 (高一第一学期第二次月考)
# 考号，年级，学期，第几次月考
# 只传考号就是要全部成绩
def getOneStuScore(examNumber: str, schoolTermSequence: int = -1, examTimes: int = None,
                   dataProcessType: int = DataProcess.Web):
    student = Student(examNumber=examNumber)
    enrollYear = student.enrollYear
    if schoolTermSequence == -1:
        schoolTermSequence = nowSchoolTerm(enrollYear)
    schoolTerm = SchoolTerm(enrollYear, schoolTermSequence)
    score = Score(student, schoolTerm, dataProcessType)

    data = score.scores
    if data is None or len(data) == 0:
        return None

    if examTimes is not None and examTimes >= 0:
        return data[examTimes]

    return data


# 某个学年入学整个年级某次月考的成绩(2022 1 1 1)2022年入学第一次月考的成绩
def getSomeStuScores(enrollYear: int, schoolTermSequence: int, classNumber: int = -1,dataProcessType: int = DataProcess.Web):
    schoolTerm = SchoolTerm(enrollYear, schoolTermSequence)
    examTimes = getExamTimes(schoolTerm)
    print(f"{enrollYear}入学，{schoolTermSequence}学期的月考次数为{examTimes}")
    GradeMap[enrollYear]["examTimes"] = examTimes
    if classNumber == -1:
        stuScores = Score.handleAllScores(schoolTerm,dataProcessType)
    else:
        stuScores = Score.handleClassScores(schoolTerm, classNumber,dataProcessType)
    storeScores(stuScores, schoolTerm, classNumber)


def initGradeInfo(enrollYear: int, totalClassCount: int = 40, seatCount: int = 80, examTimes: int = 4):
    now = datetime.date.today()
    nowYear = now.year

    if Yulin_No_1_Middle_School_Establish_Date_Year <= enrollYear <= nowYear:
        GradeMap[enrollYear] = {
            "totalClassCount": totalClassCount,
            "seatCount": seatCount,
            "examTimes": examTimes
        }
    else:
        raise ValueError(f"错误的入学年份。。。请输入{Yulin_No_1_Middle_School_Establish_Date_Year}~{nowYear}之间的年份")


__all__ = ['getSomeStuScores', 'getOneStuScore']
