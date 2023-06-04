import os.path

import score_search
from environment import BASE_PATH
from score_search.common.basic import GradeMap
from score_search.data.process import DataProcess
from util import readJsonFile

if __name__ == '__main__':
    configPath = os.path.join(BASE_PATH, "config", "grade_info.json")
    info = readJsonFile(configPath)
    enrollYear = info["enrollYear"]
    GradeMap[enrollYear] = info["basicInfo"]
    print("请选择查询的内容")
    choice = int(input("输入要查询的内容(1-查询年级成绩，2-查询个人成绩，3-退出操作):\n"))
    while True:
        searchInfo = info["searchInfo"]
        studentInfo = info["studentInfo"]
        schoolTermSequence = searchInfo.get("schoolTermSequence")
        classNumber = searchInfo.get("classNumber")
        if choice == 1:
            try:
                storePath = score_search.getSomeStuScores(enrollYear, schoolTermSequence, classNumber, DataProcess.Web)
                print(f"考试成绩已存入{storePath}")
            except ValueError as e:
                storePath = score_search.getSomeStuScores(enrollYear, schoolTermSequence, classNumber,DataProcess.Excel)
                print(f"考试成绩已存入{storePath}")
            finally:
                break
        elif choice == 2:
            try:
                scores = score_search.getOneStuScore(studentInfo["examNumber"], schoolTermSequence,
                                                     studentInfo["examSequence"], DataProcess.Web)
                print(scores)
            except ValueError as e:
                scores = score_search.getOneStuScore(studentInfo["examNumber"], schoolTermSequence,
                                                     studentInfo["examSequence"], DataProcess.Excel)
                print(scores)
            finally:
                break
        elif choice == 3:
            print("查询系统退出...")
            break
        else:
            print("输入错误，请重新输入")
