from typing import List

from score_search.common.basic import GradeMap, Map
from score_search.utils.util import isNum


# 把字符串成绩加起来得到总分，并返回浮点数的成绩数组
def scoreStrToFloat(oneStuExamScores: List[str]) -> (float, List[str]):
    totalScore = 0
    floatList = []
    for item in oneStuExamScores[:9]:
        if isNum(item):
            item = float(item)
            totalScore += item
        floatList.append(item)
    return totalScore, floatList


class SchoolTerm:
    def __init__(self, enrollYear: int, schoolTermSequenceNum: int):
        self.enrollYear: int = enrollYear
        self.sequenceNum: int = schoolTermSequenceNum
        self.grade: str = Map[(schoolTermSequenceNum - 1) // 2]
        self._totalExamTimes: int = 4
        self.uniformRank: bool = self.sequenceNum == 1 or self.enrollYear > 2020
        # 这个是因为高一高二同学的需求，对于物理划为一类，历史划为一类
        self.branch: bool = True
        self.totalClassCount: int = GradeMap[enrollYear]['totalClassCount']
        self.seatCount: int = GradeMap[enrollYear]['seatCount']

    @property
    def totalExamTimes(self) -> int | None:
        examTimes = GradeMap[self.enrollYear].get('examTimes')
        if examTimes is None:
            self._totalExamTimes: int = 4
        else:
            self._totalExamTimes = examTimes
        return self._totalExamTimes

    def specificScores(self, oneStuExamScores: List[str], dataProcessType: int):
        totalScore, floatList = scoreStrToFloat(oneStuExamScores)
        if dataProcessType == 1:
            # 第一学期要关注文理科分数，所以需要另外看
            if self.sequenceNum == 1:
                finalScores = floatList + [oneStuExamScores[9]] + oneStuExamScores[11:15] + [totalScore]
            else:
                # 第二学期之后
                finalScores = floatList + [oneStuExamScores[9]] + [totalScore]
        elif dataProcessType == 2:
            # 第二学期之后
            finalScores = floatList + [totalScore]
        else:
            raise Exception("没有其他类型")
        return finalScores

    def sortScores(self, scores: List[List], dataProcessType: int):
        if dataProcessType == 1:
            # print(scores)
            if self.uniformRank and not self.branch:
                number = 17
            else:
                number = 13
        else:
            number = 12
        scores.sort(key=lambda x: x[number], reverse=True)
        for index in range(len(scores)):
            scores[index] += [index + 1]

    # 后置处理成绩，排序并且给予排名
    # 返回值是一个学期一次月考并且分文理科的成绩
    def postProcessScore(self, allStuScores: List[List[str]], dataProcessType: int) -> List[List[List[str]]]:
        finalScores = []
        # print(allStuScores)
        if self.uniformRank and not self.branch:
            self.sortScores(allStuScores, dataProcessType)
            finalScores.append(allStuScores)
        else:
            scienceScores = []
            liberalScores = []
            for item in allStuScores:
                if item[6] != '' and item[6] is not None:
                    scienceScores.append(item)
                else:
                    liberalScores.append(item)
            self.sortScores(scienceScores, dataProcessType)
            self.sortScores(liberalScores, dataProcessType)
            finalScores.append(scienceScores)
            finalScores.append(liberalScores)
        return finalScores
