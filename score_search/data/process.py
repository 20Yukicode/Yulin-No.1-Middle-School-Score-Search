import re
import urllib.parse
from typing import List

import requests
from bs4 import BeautifulSoup

from score_search.common.basic import GradeMap
from score_search.exception.apiError import ApiException
from score_search.grade.schoolTerm import SchoolTerm
from score_search.utils.util import isNull


class DataProcess:
    Excel = 1
    Web = 2

    def __init__(self, examNumber: str, schoolTerm: SchoolTerm):
        self.examNumber: str = examNumber
        self.schoolTerm: SchoolTerm = schoolTerm
        self.data = None

    @staticmethod
    def constructDataProcess(examNumber: str, schoolTerm: SchoolTerm, dataOrigin: int):
        if dataOrigin == DataProcess.Excel:
            return DataProcessExcel(examNumber, schoolTerm)
        elif dataOrigin == DataProcess.Web:
            return DataProcessWeb(examNumber, schoolTerm)
        raise ApiException("没有这种爬虫")

    def initData(self):
        pass

    def filterData(self):
        pass

    def cleanData(self) -> (List[str], List[List[str]]):
        pass

    def handleData(self) -> (List[str], List[List[str]]):
        self.initData()
        self.filterData()
        basicInfo, cleanData = self.cleanData()
        return basicInfo, cleanData


class DataProcessExcel(DataProcess):
    Url = "http://116.11.184.151:3288/cjcx%5E&/daochu.asp?"
    ScoreUrl = "http://116.11.184.151:3288/cjcx%5E&/chengji.xls"

    def __init__(self, examNumber: str, schoolTerm: SchoolTerm):
        super().__init__(examNumber, schoolTerm)

    # 爬取数据 data->str
    def initData(self):
        year = self.examNumber[:4]
        generator = f'{DataProcessExcel.Url}tb=studinfo{year}{self.schoolTerm.sequenceNum}&kaohao={self.examNumber}'
        requests.get(generator)
        # 打印生成的链接
        # print(generator)
        result = requests.get(DataProcessExcel.ScoreUrl)
        self.data = result.content.decode('gbk')
        if isNull(self.data):
            raise ApiException(f"第{self.schoolTerm.sequenceNum}学期，{self.examNumber}此学生不存在成绩")

    # 筛选数据 data->List[str]
    def filterData(self):
        data1 = re.findall('(?<=")[^"]*(?=")', self.data)
        self.data = []
        # print("原始数据:")
        # print(data)
        for item in data1:
            if item == '\t=':
                continue
            self.data.append(item.strip())

    # 拿到的数据分离出姓名和每次月考的成绩
    def cleanData(self) -> (List[str], List[List[str]]):
        basicInfoCount = 3
        subjectCount = 15

        # 考生基本信息 班别,姓名,考号
        basicInfo = self.data[:basicInfoCount]
        times = (len(self.data) - basicInfoCount) // subjectCount

        # 二维数组
        scores = [self.data[i * subjectCount + basicInfoCount:(i + 1) * subjectCount + basicInfoCount] for i in
                  range(times)]
        # print("经过第一次处理后的数据")
        # print(cleanData)
        return basicInfo, scores


def decodeStr(s: str) -> str:
    return urllib.parse.unquote(s, encoding='gbk')


def getExamTimes(schoolTerm: SchoolTerm, dataProcessType=DataProcess.Web) -> int | None:
    examNumber = str(schoolTerm.enrollYear) + "010001"
    dataProcess = DataProcess.constructDataProcess(examNumber, schoolTerm, dataProcessType)
    try:
        dataProcess.initData()
        dataProcess.filterData()
    except ApiException:
        return None
    examTimes = len(dataProcess.data) // 10 - 1
    if examTimes == -1:
        return None
    return examTimes


class DataProcessWeb(DataProcess):
    Url = "http://116.11.184.151:3288/cjcx%5E&/list.asp"

    def __init__(self, examNumber: str, schoolTerm: SchoolTerm):
        super().__init__(examNumber, schoolTerm)
        self.schoolTerm = schoolTerm
        # self.nameList = NameList.constructNameList(self.schoolTerm)
        # self.nameList.storeNameList()
        self.basicInfo = []

    # 爬取数据 data->str
    def initData(self):
        if not self.schoolTerm.isNowSchoolTerm:
            raise ApiException("不是当前学期，无法通过web方式查询")
        # self.basicInfo = self.nameList.getInfoByExamNum(self.examNumber)
        dataProcessExcel = DataProcessExcel(examNumber=self.examNumber, schoolTerm=self.schoolTerm)
        # 先通过excel的方式获取基本信息
        self.basicInfo = dataProcessExcel.handleData()[0]
        stuData = {
            'name': self.basicInfo[1].encode('gbk'),
            'kaohao': self.examNumber,
            "kaohao1": self.examNumber,
            "Submit": '查询'.encode('gbk'),
            'name1': f'studinfo{self.schoolTerm.enrollYear}{self.schoolTerm.sequenceNum}'
        }
        result = requests.post(DataProcessWeb.Url, data=stuData)
        self.data = result.content.decode('gbk')
        if isNull(self.data):
            raise ApiException(f"第{self.schoolTerm.sequenceNum}学期，{self.examNumber}此学生不存在成绩")

    # 筛选数据 data->List[str]
    def filterData(self):
        soup = BeautifulSoup(self.data, 'html.parser')
        self.data = soup.findAll('td', attrs={'width': '4%'})

    # 拿到的数据分离出姓名和每次月考的成绩
    def cleanData(self) -> (List[str], List[List[str]]):
        splitTime = len(self.data) // 10

        mapData = list(map(lambda x: x.string, self.data))
        self.data = []
        for i in range(splitTime):
            self.data.append(mapData[i * 10:(i + 1) * 10])

        # 重新设置考试次数
        GradeMap[self.schoolTerm.enrollYear]['examTimes'] = splitTime - 1

        basicInfo, cleanData = self.basicInfo, self.data[1:]
        return basicInfo, cleanData


if __name__ == "__main__":
    examNum = '2021120001'
    schoolTermExample = SchoolTerm(2021, 3)
    dataProcess = DataProcess.constructDataProcess(examNum, schoolTermExample, DataProcess.Web)
    res = dataProcess.handleData()
    print(res)

    # test3('王宇宁', '2020130045', 2020, 5)
