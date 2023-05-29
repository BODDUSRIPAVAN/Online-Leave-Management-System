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

create table faculty(
 id_num varchar(10) not null primary key,
 name varchar(20),
 email varchar(20),
 phone varchar(10),
 password varchar(8)
);

create table leave_application(
	num int auto_increment primary key,
    id_num varchar(7),
    from_date varchar(15),
    to_date varchar(15),
    reason varchar(200),
    status varchar(1) default 'n'
);

create user 'monkey'@'localhost' identified by 'tail';
grant all privileges on college.* to 'monkey'@'localhost';