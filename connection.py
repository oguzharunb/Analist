from sqlalchemy import create_engine, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String,Float

# Replace the following with your MySQL connection information
username = "root"
password = "root1234"
host = "db"
database = "analistv1"

connection_string = f"mysql://{username}:{password}@{host}/{database}"
engine = create_engine(connection_string)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Class(Base):
    __tablename__ = "classes"
    class_ID = Column(Integer, primary_key=True, autoincrement=True)
    class_name = Column(String(100), nullable=False, name="class")

class ExamType(Base):
    __tablename__ = "examtypes"
    exam_type_ID = Column(Integer, primary_key=True, autoincrement=True)
    exam_type = Column(String(100), nullable=False)

class Exam(Base):
    __tablename__ = "exams"
    exam_ID = Column(Integer, primary_key=True, autoincrement=True)
    exam_name = Column(String(255), nullable=True)
    exam_type_ID = Column(Integer, ForeignKey("examtypes.exam_type_ID"), nullable=True)
    date = Column(DateTime, nullable=True)

class User(Base):
    __tablename__ = "users"
    user_ID = Column(Integer, primary_key=True, autoincrement=True)
    isTeacher = Column(Boolean, nullable= False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)  # Assuming SHA256 encryption
    school_no = Column(String(50), nullable=True)
    class_ID = Column(Integer, ForeignKey("classes.class_ID"), nullable=True)

class ExamResult(Base):
    __tablename__ = "examresults"
    user_ID = Column(Integer, ForeignKey("users.user_ID"), nullable=True, primary_key=True)
    exam_ID = Column(Integer, ForeignKey("exams.exam_ID"), nullable=True, primary_key=True)
    qtrue = Column(Integer, nullable=True)
    qfalse = Column(Integer, nullable=True)
    #qempty = Column(Boolean, nullable=True)
    qabs = Column(Float, nullable=True)
    score = Column(Integer, nullable=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return str(self.as_dict())


def add_class(class_name):
    c = Class(class_name=class_name)
    session.add(c)
    session.commit()

def add_exam_type(exam_type):
    et = ExamType(exam_type=exam_type)
    session.add(et)
    session.commit()

def add_exam(exam_name, exam_type_ID, date):
    exam = Exam(exam_name=exam_name, exam_type_ID=exam_type_ID, date=date)
    session.add(exam)
    session.commit()

def add_user(username, password, school_no, class_ID, isTeacher):
    user = User(username=username, password=password, school_no=school_no, class_ID=class_ID, isTeacher= isTeacher)
    session.add(user)
    session.commit()

def add_exam_result(user_ID, exam_ID, qtrue, qfalse, qabs, score):
    exam_result = ExamResult(user_ID=user_ID, exam_ID=exam_ID, qtrue=qtrue, qfalse=qfalse, qabs=qabs, score=score)
    session.add(exam_result)
    session.commit()

# Add other helper functions for querying and checking data


def user_exists(username):
    user = session.query(User).filter_by(username=username).first()
    return user is not None

def class_exists(class_name):
    class_ = session.query(Class).filter_by(class_name=class_name).first()
    return class_ is not None


def get_username_by_userID(user_ID):
    c = session.query(User).filter_by(user_ID=user_ID).first()
    return c.username if c else None


def get_exam_result_by_user_id(user_id):
    c = session.query(ExamResult).filter_by(user_ID=user_id).all()
    return c if c else None

def get_password_id_by_username(user_name):
    c = session.query(User).filter_by(username=user_name).first()
    return c.password if c else None

def get_class_id_by_name(class_name):
    c = session.query(Class).filter_by(class_name=class_name).first()
    return c.class_ID if c else None

def get_user_id_by_name(username):
    c = session.query(User).filter_by(username=username).first()
    return c.user_ID if c else None

def get_exam_id_by_name(exam_name):
    c = session.query(Exam).filter_by(exam_name=exam_name).first()
    return c.exam_ID if c else None

def get_exam_name_by_id(exam_ID):
    c = session.query(Exam).filter_by(exam_ID=exam_ID).first()
    return c.exam_name if c else None

def get_isTeacher_by_user_id(user_ID):
    c = session.query(User).filter_by(user_ID=user_ID).first()
    return c.isTeacher if c else None

def get_all_exam_results():
    exam_results = session.query(ExamResult).all()
    return exam_results

def get_class_name_by_user_id(user_id):
    user = session.query(User).filter_by(user_ID=user_id).first()
    if user:
        class_id = user.class_ID
        if class_id:
            class_ = session.query(Class).filter_by(class_ID=class_id).first()
            if class_:
                return class_.class_name
    return None

def get_exam_type_by_exam_id(exam_id):
    exam = session.query(Exam).filter_by(exam_ID=exam_id).first()
    if exam:
        exam_type_record = session.query(ExamType).filter_by(exam_type_ID=exam.exam_type_ID).first()
        if exam_type_record:
            return exam_type_record.exam_type
    return None

def get_all_class_names():
    classes = session.query(Class).all()
    return [c.class_name for c in classes]

def get_all_exam_names():
    exams = session.query(Exam).all()
    return [c.exam_name for c in exams]

def get_all_exam_types():
    exams = session.query(ExamType).all()
    return [c.exam_type for c in exams]

#
#def get_city_by_id(city_id):
#    return session.query(Cities).filter_by(city_id=city_id).first()
#
#def get_city_id_by_name(city_name):
#    city = session.query(Cities).filter_by(city_name=city_name).first()
#    return city.city_id if city else None
#
#
#def city_exists(city_name):
#    city = session.query(Cities).filter_by(city_name=city_name).first()
#    return city is not None
#