USE analistv1;

CREATE TABLE examtypes (
    exam_type_ID INT PRIMARY KEY AUTO_INCREMENT,
    exam_type VARCHAR(255)
);

-- Create the 'classes' table
CREATE TABLE classes (
    class_ID INT PRIMARY KEY AUTO_INCREMENT,
    class VARCHAR(255)
);

-- Create the 'exams' table with foreign key constraints
CREATE TABLE exams (
    exam_ID INT PRIMARY KEY AUTO_INCREMENT,
    exam_type_ID INT,
    exam_name VARCHAR(255),
    date DATE,
    FOREIGN KEY (exam_type_ID) REFERENCES examtypes(exam_type_ID)
);

-- Create the 'users' table with foreign key constraints
CREATE TABLE users (
    user_ID INT PRIMARY KEY AUTO_INCREMENT,
    class_ID INT,
    username VARCHAR(255),
    password VARCHAR(255),
    school_no INT,
    isTeacher BOOLEAN,
    FOREIGN KEY (class_ID) REFERENCES classes(class_ID)
);

-- Create the 'examresults' table with foreign key constraints
CREATE TABLE examresults (
    user_ID INT,
    exam_ID INT,
    qtrue INT,
    qfalse INT,
    qabs FLOAT,
    score INT,
    FOREIGN KEY (user_ID) REFERENCES users(user_ID),
    FOREIGN KEY (exam_ID) REFERENCES exams(exam_ID)
);
INSERT INTO classes (class) VALUES ('Yok');
INSERT INTO examtypes (exam_type) VALUES ('TYT');
INSERT INTO examtypes (exam_type) VALUES ('AYT');
INSERT INTO users (username, password, school_no, class_ID, isTeacher) VALUES ('ogretmen', 'ogrt1234', 1, 1, 1);
INSERT INTO users (username, password, school_no, class_ID, isTeacher) VALUES ('admin', 'sifreadmin1234', 1, 1, 1);
