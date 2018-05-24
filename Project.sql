CREATE TABLE Student (
    Stu_num       NUMBER(5,0)
        CONSTRAINT pk_stu_num PRIMARY KEY,
    stu_fname     VARCHAR2(10),
    stu_lname     VARCHAR2(15),
    stu_street    VARCHAR2(25),
    stu_city      VARCHAR2(20),
    stu_state     VARCHAR2(2),
    stu_zip       VARCHAR2(6),
    stu_email   VARCHAR2(50),
    stu_dob      date,
    stu_date_joined date,
    stu_mobile number(10,0),
    CONSTRAINT stu_mob_unique UNIQUE (stu_mobile)
);


CREATE TABLE parents (
    stu_num        NUMBER(5,0)
        CONSTRAINT fk_stu_num
            REFERENCES student,
    par_fname      VARCHAR2(10),
    par_lname      VARCHAR2(15),
    par_relation   VARCHAR2(6),
    par_email      VARCHAR2(50),
    par_mob        NUMBER(10,0)
);


CREATE TABLE payment_info (
    stu_num           NUMBER(5,0)
        CONSTRAINT fk_stu_num_1
            REFERENCES student,
    pay_productinfo   VARCHAR2(50),
    pay_amount        NUMBER(10),
    pay_date          DATE
);

CREATE TABLE class (
    class_id      NUMBER(4)
        CONSTRAINT pk_id PRIMARY KEY,
    class_level   VARCHAR2(35),
    class_time    VARCHAR2(14),
    class_day     VARCHAR2(10)
);

CREATE TABLE attendance (
    stu_num    NUMBER(5,0),
    class_id   NUMBER(4),
    tt_date    DATE,
    CONSTRAINT fk_att_stu FOREIGN KEY ( stu_num )
        REFERENCES student,
    CONSTRAINT fk_att_class FOREIGN KEY ( class_id )
        REFERENCES class
);


CREATE TABLE rank (
    rank_id      NUMBER(4)
        CONSTRAINT pk_rank_id PRIMARY KEY,
    rank_color   VARCHAR(15),
    CONSTRAINT rank_col_unique UNIQUE ( rank_color )
);



CREATE TABLE student_rank (
    stu_num           NUMBER(5,0)
        CONSTRAINT fk_stu_num_2
            REFERENCES student,
    rank_id           NUMBER(4)
        CONSTRAINT fk_rank_id
            REFERENCES rank,
    rank_award_date   DATE
);

CREATE TABLE user_info (
    username   VARCHAR2(15)
        CONSTRAINT pk_uname PRIMARY KEY,
    password   VARCHAR2(15) NOT NULL
);

insert into user_info values('admin','password');

insert into rank values(1,'White');
insert into rank values(2,'Yellow');
insert into rank values(3,'Half Green');
insert into rank values(4,'Green');
insert into rank values(5,'Half Blue');
insert into rank values(6,'Blue');
insert into rank values(7,'Half Red');
insert into rank values(8,'Red');
insert into rank values(9,'Half Black');
insert into rank values(10,'Black');


insert into class values(1,'beginner','6:00 pm','Monday');

insert into class values(2,'intermediate','5:00 pm','Monday');
insert into class values(3,'advance','5:00 pm','Tuesday');
insert into class values(4,'expert','4:00 pm','Wednesday');