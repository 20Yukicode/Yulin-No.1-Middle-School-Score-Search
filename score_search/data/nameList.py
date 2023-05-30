import os.path
from typing import List

import xlrd
import xlwt

from score_search.grade.schoolTerm import SchoolTerm

PathPrefix = '../../resources'


def generatorNameListPath(enrollYear: int, grade: str, schoolTerm: int) -> str:
    path = f'{PathPrefix}/{enrollYear}级/高{grade}/{schoolTerm}学期'
    return f'{path}/名单.xls'


class NameList:

    def __init__(self, schoolTerm: SchoolTerm):
        self.schoolTerm: SchoolTerm = schoolTerm
        self.path = generatorNameListPath(schoolTerm.enrollYear, schoolTerm.grade, schoolTerm.sequenceNum)
        self.workSheetsName: List[str] = []
        self.workBook = None
        self.workSheets = []
        # 考号，班别，姓名
        # {
        #   "2016220044":(1622,'nzh')
        # }
        self.basicInfos = []

    @staticmethod
    def wordStyle():
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = "宋体"
        font.height = 20 * 11
        style.font = font
        return style

    @staticmethod
    def constructNameList(schoolTerm: SchoolTerm):
        if schoolTerm.uniformRank:
            return UniformRankNameList(schoolTerm)
        else:
            return NewNameList(schoolTerm)

    def initExcel(self):
        self.workBook = xlwt.Workbook()
        for name in self.workSheetsName:
            self.workSheets.append(self.workBook.add_sheet(name))

        self.workBook.save(self.path)

    def storeExcel(self, names: List[List[List[str]]]):
        for i, item in enumerate(names):
            for j, item0 in enumerate(item):
                for k, item1 in enumerate(item0):
                    self.workSheets[i].write(j, k, item1)

        self.workBook.save(self.path)

    def readExcel(self):
        workBook = xlrd.open_workbook(self.path)
        sheets = workBook.sheets()
        self.basicInfos = [[] for _ in range(len(sheets))]
        for i, sheet in enumerate(sheets):
            rows = sheet.nrows
            for row in range(rows):
                basicInfo = sheet.row_values(row)
                self.basicInfos[i].append(basicInfo)

    def getInfoByExamNum(self, examNum: str) -> List[str]:
        for i in self.basicInfos:
            for j in i:
                if j[2] == examNum:
                    return j

    def storeNameList(self):
        if not os.path.exists(self.path):
            self.initExcel()
            names = []
            print(f"正在生成{self.schoolTerm.enrollYear}级高{self.schoolTerm.grade}名单...")
            for i in range(self.schoolTerm.totalClassCount):
                for j in range(self.schoolTerm.seatCount):
                    try:
                        examNumber = str(self.schoolTerm.enrollYear) + str(i + 1).zfill(2) + '00' + str(j + 1).zfill(2)
                        dataProcess = DataProcess.constructDataProcess(examNumber, self.schoolTerm.sequenceNum,
                                                                       DataProcess.Web)
                        res = dataProcess.handleData()[0]
                        names.append(res)
                    except Exception as e:
                        print(e)
                        continue
            finalNames = [names]
            self.storeExcel(finalNames)
            print("生成完毕")
        if not self.basicInfos:
            self.readExcel()


class UniformRankNameList(NameList):
    def __init__(self, schoolTerm: SchoolTerm):
        super().__init__(schoolTerm)
        self.workSheetsName = ['名单']


class NewNameList(NameList):
    def __init__(self, schoolTerm: SchoolTerm):
        super().__init__(schoolTerm)
        self.workSheetsName = ['理科名单', '文科名单']
