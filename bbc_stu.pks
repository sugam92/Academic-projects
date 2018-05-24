CREATE OR REPLACE PACKAGE bbc_stu AS 

    PROCEDURE add_stu (
        fname           IN VARCHAR2,
        lname           IN VARCHAR2,
        street          IN VARCHAR2,
        city            IN VARCHAR2,
        province        IN VARCHAR2,
        zip             IN VARCHAR2,
        email           IN VARCHAR2,
        mobile          IN VARCHAR2,
        dob             IN VARCHAR2,
        father_fname    IN VARCHAR2,
        father_lname    IN VARCHAR2,
   --f_relation in varchar2,
        father_email    IN VARCHAR2,
        father_mobile   IN VARCHAR2,
        mother_fname    IN VARCHAR2,
        mother_lname    IN VARCHAR2,
   --m_relation in varchar2,
        mother_email    IN VARCHAR2,
        mother_mobile   IN VARCHAR2,
        product1        IN VARCHAR2,
        stu_num         OUT NUMBER
    );

    PROCEDURE add_att (
        p_stu_num    NUMBER,
        p_c_id       NUMBER,
        p_att_date   VARCHAR2
    );

    PROCEDURE add_rank (
        p_colour VARCHAR2
    );

    PROCEDURE add_promo (
        p_stu_num IN NUMBER,
        a_date DATE
    );


END bbc_stu;
/