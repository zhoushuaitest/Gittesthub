show databases;
use aaa;
show tables;

use aaa;
create table cs_0001(
username int,
psaa varchar(10),
sicdh int
);

create table `cs_0002`(
`usernam` int,
`passwd` varchar(60),
`sicdh` int
);

create table `cs_0003`(
`name` varchar(30) comment '姓名',
`passwd` int comment '密码'
)engine=InnoDB comment '学生表';

select * from cs_0003;
#添加字段
-- 回电话·
insert into cs_0003 value('周帅',133) ;
insert into cs_0003 value('周帅02',1333) ;
insert into cs_0003 value('冯路',13) ; 

alter table cs_0003 add home varchar(30);
alter table cs_0003 add age int;

#向所有字段添加多条数据

insert into cs_0003 value ('cs001',35,'眉山',15),('cs002',234,'成都',76),('cs003',24,'资阳',26);

#向对应字段添加数据

insert into cs_0003 (home,age) value ('重庆',15), ('长沙',35);

delete from cs_0003;

update cs_0003 set passwd=100  where passwd is null;

select passwd = 234 from cs_0003 where age>=26;
select * from cs_0003 where age>=26;

select * from cs_0003 where age between 15 and 35;

select * from cs_0003 where age in (15,26,35);

select * from cs_0003 where age not in (15,26,35);

create table `student`(
`sno` int comment '编号',
`sname` varchar(20),
`ssex` varchar(5),
`sbirthday` varchar(30),
`sclass` int 
);

insert into student values('108','曾华','男','1977-09-01','95033');
insert into student values('105','匡明','男','1975-10-02','95031');
insert into student values('107','王丽','女','1976-01-23','95033');
insert into student values('101','李军','男','1976-02-20','95033');
insert into student values('109','王芳','女','1975-02-10','95031');
insert into student values('103','陆君','男','1974-06-03','95031');

select * from student;

create table score(
sno int,
cno varchar(20),
degree int
);

insert into score values('103','3-245','86');
insert into score values('105','3-245','75');
insert into score values('109','3-245','68');
insert into score values('103','3-105','92');
insert into score values('105','3-105','88');
insert into score values('109','3-105','76');
insert into score values('103','3-105','64');
insert into score values('105','3-105','91');
insert into score values('109','3-105','78');
insert into score values('103','6-166','85');
insert into score values('105','6-166','79');
insert into score values('109','6-166','81');

select * from score;


#1、 查询student表中的所有记录的sname、ssex和class列
select sname ,ssex,sclass from student;
#2、 查询学生所有的学号即不重复的sno列
select distinct sno from score;
#3、 查询student表的所有记录
select * from student;
#4、查询score表中成绩在60到80之间的所有记录\
select * from score where degree between 60 and 80;
#5、 查询score表中成绩为85，86或88的记录
select * from score where degree in (85,86,88);
#6、 查询student表中“95031”班或性别为“女”的同学记录\
select * from student where sclass=95031 or ssex='女';
select * from student where sclass=95031 and ssex='女';
#7、 以class降序查询Student表的所有记录
select * from student order by sclass desc;
#8、 以cno升序、degree降序查询score表的所有记录

select * from score order by cno ,degree desc;
#9、 查询“95031”班的学生人数
select count(*) from student where sclass=95031;
#10、查询score表中的最高分的学生学号和课程号
#11、查询每门课的平均成绩
#12、查询score表中至少有5名学生选修的并以3开头的课程的平均分数
#13、查询分数大于70，小于90的sno列
select * from score where degree >70 and degree <90 ;






