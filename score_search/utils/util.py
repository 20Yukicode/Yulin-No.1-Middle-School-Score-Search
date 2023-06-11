import datetime
import os

from environment import BASE_PATH

PathPrefix = os.path.join(BASE_PATH, "resources")
# '../../resources'
ScoreIndex = 0


# 注意grade是1-3,schoolTerm的范围是1-6
def nowSchoolTerm(year: int) -> int:
    now = datetime.date.today()
    nowYear = now.year
    nowMonth = now.month
    # 当前年级
    nowGrade = nowYear - year
    temp = 0
    if 3 <= nowMonth <= 8:
        pass
    elif 1 <= nowMonth <= 2:
        temp = 1
    else:
        temp = -1
    # 当前学期
    schoolTerm = nowGrade * 2 - temp
    return schoolTerm


def isNull(string: str) -> bool:
    return string is None or string.isspace() or string.strip() == ""


def isNum(n: str) -> bool:
    if n is None:
        return False
    try:
        k = float(n)
        return True
    except ValueError:
        return False


def writeError(content: str, path: str = "../error.txt"):
    with open(path, "w", encoding='utf-8') as f:
        f.write(content)


# 入学年份 年级 学期 班别号
def generatorScoreFilePath(enrollYear: int, grade: str, examTimes: int, schoolTerm: int,
                           classNumber: int = None) -> str:
    global ScoreIndex
    path = f'{PathPrefix}/{enrollYear}级/高{grade}/{schoolTerm}学期'
    if not os.path.exists(f'{path}/{ScoreIndex}'):
        os.makedirs(f'{path}/{ScoreIndex}')
    if classNumber is None:
        while True:
            if os.path.exists(f'{path}/{ScoreIndex}/第{examTimes + 1}次月考成绩单.xls'):
                ScoreIndex = ScoreIndex + 1
            else:
                if not os.path.exists(f'{path}/{ScoreIndex}'):
                    os.makedirs(f'{path}/{ScoreIndex}')
                return f'{path}/{ScoreIndex}/第{examTimes + 1}次月考成绩单.xls'
    else:
        while True:
            if os.path.exists(f'{path}/{ScoreIndex}/{classNumber}班第{examTimes + 1}次月考成绩单.xls'):
                ScoreIndex = ScoreIndex + 1
            else:
                if not os.path.exists(f'{path}/{ScoreIndex}'):
                    os.makedirs(f'{path}/{ScoreIndex}')
                return f'{path}/{ScoreIndex}/{classNumber}班第{examTimes + 1}次月考成绩单.xls'


if __name__ == "__main__":
    print(isNum('1d'))
