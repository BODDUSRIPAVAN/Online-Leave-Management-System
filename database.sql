drop database if exists college;
create database college;
use college;
create table student_details(
id_num varchar(7) not null primary key,
name varchar(20),
email varchar(20),
phone varchar(10),
password varchar(8)
);
drop table faculty;
create table faculty(
 id_num varchar(10) not null primary key,
 name varchar(20),
 email varchar(20),
 phone varchar(10),
 password varchar(8),
 hod varchar(1) default 'n'
);
drop table leave_application;
create table leave_application(
	num int auto_increment primary key,
    id_num varchar(7),
    from_date varchar(15),
    to_date varchar(15),
    reason varchar(200),
    status varchar(1) default 'c'
);

create user 'monkey'@'localhost' identified by 'tail';
grant all privileges on college.* to 'monkey'@'localhost';

select * from student_details;
insert into faculty values('f1','f1','f1@gmail.com','f1','f1','n'),
('f2','f2','f2@gmail.com','f2','f2','n'),('h1','h1','h1@gmail.com','h1','h1','y');
select * from faculty;
select * from leave_application;


-- truncate  comments;

CREATE table comments(
	num int,
    comment varchar(25)
);
select * from comments;
-- drop table comments;
SELECT num FROM leave_application where id_num='5';
INSERT INTO comments VALUES ((SELECT num FROM leave_application where id_num='5'), "aaa");
