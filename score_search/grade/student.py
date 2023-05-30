class Student:
    def __init__(self, enrollYear: int = None, lesson: int = None, seatNumber: int = None, examNumber: str = None):
        self.examNumber: str = examNumber
        self.enrollYear: int = enrollYear
        self.lesson: int = lesson
        self.seatNumber: int = seatNumber
        if examNumber:
            self.handleByExamNum()
        else:
            self.handleExamNum()

    def handleByExamNum(self):
        self.enrollYear = int(self.examNumber[:4])
        self.lesson = int(self.examNumber[4:6])
        self.seatNumber = int(self.examNumber[8:10])

    def handleExamNum(self):
        self.examNumber = str(self.enrollYear) + str(self.lesson).zfill(2) + '00' + str(self.seatNumber).zfill(2)
