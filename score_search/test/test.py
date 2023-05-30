from score_search import getOneStuScore, getSomeStuScores
from score_search.grade.schoolTerm import SchoolTerm
from score_search.grade.score import Score
from score_search.grade.student import Student


def test():
    student = Student(examNumber='2022220044')
    schoolTerm = SchoolTerm(2022, 1)
    kk = Score.handleClassScores(schoolTerm, 22)
    for item in kk:
        for items in item:
            print(items)
        print("___")
    stuScore = Score(student, schoolTerm)
    print(stuScore.scores)


def testApi():
    res = getOneStuScore(examNumber='2021010018', schoolTermSequence=3, examTimes=0)
    res2 = getOneStuScore(examNumber='2021010018')
    print(res)
    print(res2)


def testApi2():
    # getSomeStuScores(2022,2)
    getSomeStuScores(2020, 6)


if __name__ == "__main__":
    testApi2()
    # str="2016220044"
    # print(int(str[:4]))
    # arr = []
    # sub = [1, 4, 5]
    # for i in range(4):
    #     arr .append(sub)
    # print(arr)
