from schoolTerm import SchoolTerm


class Exam:
    def __init__(self, schoolTerm: SchoolTerm, sequenceNum: int):
        self.schoolTerm: SchoolTerm = schoolTerm
        self.sequenceNum: int = sequenceNum
