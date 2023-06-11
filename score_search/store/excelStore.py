# 最终需要的数据
from typing import List

import xlwt

from score_search.grade.schoolTerm import SchoolTerm
from score_search.utils.util import generatorScoreFilePath

SubjectExcel = {
    1: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "文科总分", "文科排名", "理科总分", "理科排名", "总分"],
    2: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "总分"],
    3: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "总分"],
    4: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "总分"],
    5: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "总分"],
    6: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "班级排名", "总分"],
}

SubjectWeb = {
    1: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
    2: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
    3: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
    4: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
    5: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
    6: ["班别", "姓名", "考号", "语文", "数学", "英语", "物理", "化学", "生物", "政治", "历史", "地理",
        "总分"],
}


# 四次考试,然后分文理科,每次考试的每个学生的成绩
def storeScores(scores: List[List[List[List]]], schoolTerm: SchoolTerm, classNum: int, dataProcessType: int):
    pathList = []
    for i in range(schoolTerm.totalExamTimes):
        path = generatorScoreFilePath(schoolTerm.enrollYear, schoolTerm.grade, i, schoolTerm.sequenceNum, classNum)
        pathList.append(path)
        excelScores = ExcelScores.constructExcelGrade(schoolTerm, examTimes=i, path=path,
                                                      dataProcessType=dataProcessType)
        excelScores.storeGrades(scores[i])
    return pathList


class ExcelScores:
    def __init__(self, schoolTerm: SchoolTerm, examTimes: int, path: str, dataProcessType: int):
        self.schoolTerm: SchoolTerm = schoolTerm
        self.examTimes: int = examTimes
        self.path: str = path
        self.dataProcessType: int = dataProcessType

        self.workBook = None
        self.workSheets = []

    @staticmethod
    def wordStyle():
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = "宋体"
        font.height = 20 * 11
        style.font = font
        return style

    @staticmethod
    def constructExcelGrade(schoolTerm: SchoolTerm, examTimes: int, path: str, dataProcessType: int):
        if schoolTerm.uniformRank and not schoolTerm.branch:
            return UniformRankExcelScores(schoolTerm, examTimes, path, dataProcessType)
        else:
            return NewExcelScores(schoolTerm, examTimes, path, dataProcessType)

    def initExcel(self, workSheetNames):
        self.workBook = xlwt.Workbook(encoding='utf-8')
        for name in workSheetNames:
            self.workSheets.append(self.workBook.add_sheet(name))
        if self.dataProcessType == 1:
            col = SubjectExcel.get(self.schoolTerm.sequenceNum)
        else:
            col = SubjectWeb.get(self.schoolTerm.sequenceNum)

        for sheet in self.workSheets:
            for i, item in enumerate(col):
                sheet.write(0, i, item, ExcelScores.wordStyle())

        self.workBook.save(self.path)

    def storeGrades(self, scores: List[List[List]]):
        for i, score0 in enumerate(scores):
            for j, score1 in enumerate(score0):
                for k, score2 in enumerate(score1):
                    if k == 1:
                        self.workSheets[i].write(j + 1, k, score2, ExcelScores.wordStyle())
                    else:
                        self.workSheets[i].write(j + 1, k, score2)

        self.workBook.save(self.path)


class UniformRankExcelScores(ExcelScores):
    def __init__(self, schoolTerm: SchoolTerm, examTimes: int, path: str, dataProcessType: int):
        super().__init__(schoolTerm, examTimes, path, dataProcessType)
        workSheetNames = ['成绩']
        super().initExcel(workSheetNames)


class NewExcelScores(ExcelScores):
    def __init__(self, schoolTerm: SchoolTerm, examTimes: int, path: str, dataProcessType):
        super().__init__(schoolTerm, examTimes, path, dataProcessType)
        workSheetNames = ['理科成绩', '文科成绩']
        super().initExcel(workSheetNames)
