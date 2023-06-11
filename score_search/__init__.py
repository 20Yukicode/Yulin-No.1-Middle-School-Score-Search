import datetime

import numpy as np

from score_search.common.basic import GradeMap
from score_search.data.process import getExamTimes, DataProcess
from score_search.exception.apiError import ApiException
from score_search.grade.schoolTerm import SchoolTerm
from score_search.grade.score import Score
from score_search.grade.student import Student

from score_search.store.excelStore import storeScores, SubjectWeb, SubjectExcel
from score_search.utils.util import nowSchoolTerm

Yulin_No_1_Middle_School_Establish_Date_Year = 1923


# 比如2021010001 2  3   2(高二第三学期第二次月考)
# 比如2022010001 1  1   2 (高一第一学期第二次月考)
# 考号，年级，学期，第几次月考
# 只传考号就是要全部成绩
def getOneStuScore(examNumber: str,
                   schoolTermSequence: int = None,
                   examTimes: int = None,
                   dataProcessType: int = DataProcess.Web):
    if dataProcessType == DataProcess.Web:
        queryMethod = "网页查询"
    else:
        queryMethod = "Excel查询"
    print(f"通过{queryMethod}")
    student = Student(examNumber=examNumber)
    enrollYear = student.enrollYear
    if schoolTermSequence is None or schoolTermSequence <= 0:
        schoolTermSequence = nowSchoolTerm(enrollYear)
    schoolTerm = SchoolTerm(enrollYear, schoolTermSequence)
    score = Score(student, schoolTerm, dataProcessType)

    data = score.scores
    if data is None or len(data) == 0:
        raise ApiException(
            f"{queryMethod}:第{schoolTermSequence}学期的考生{examNumber}第{examTimes}次考试数据不存在，请检查配置文件...")

    if dataProcessType == DataProcess.Web:
        print(SubjectWeb[schoolTermSequence])
    else:
        print(SubjectExcel[schoolTermSequence])
    if examTimes is not None and examTimes >= 1:
        return data[examTimes - 1]
    return data


# 某个学年入学整个年级某次月考的成绩(2022 1 1 1)2022年入学第一次月考的成绩
def getSomeStuScores(enrollYear: int,
                     schoolTermSequence: int,
                     classNumber: int = None,
                     dataProcessType: int = DataProcess.Web):
    schoolTerm = SchoolTerm(enrollYear, schoolTermSequence)
    if dataProcessType == DataProcess.Web:
        queryMethod = "网页查询"
    else:
        queryMethod = "Excel查询"

    print(f"通过{queryMethod}")
    examTimes = getExamTimes(schoolTerm, dataProcessType)
    if examTimes is None:
        raise ApiException(f"{queryMethod}:第{schoolTermSequence}学期的考试数据不存在，请检查配置文件...")
    print(f"{enrollYear}入学，{schoolTermSequence}学期的月考次数为{examTimes}")
    GradeMap[enrollYear]["examTimes"] = examTimes

    if classNumber is None:
        stuScores = Score.handleAllScores(schoolTerm, dataProcessType)
    else:
        stuScores = Score.handleClassScores(schoolTerm, classNumber, dataProcessType)

    storePathList = storeScores(stuScores, schoolTerm, classNumber, dataProcessType)
    return storePathList


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
        raise ApiException(f"错误的入学年份。。。请输入{Yulin_No_1_Middle_School_Establish_Date_Year}~{nowYear}之间的年份")


__all__ = ['getSomeStuScores', 'getOneStuScore']
