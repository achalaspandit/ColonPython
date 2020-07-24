-- sqlite3 binpy.db < binpy-schema.sql


create table signup(
userid varchar(10) NOT NULL PRIMARY KEY,
user_name varchar(30) NOT NULL,
password varchar(10) NOT NULL,
mobile_no int
);

create table login(
userid varchar(10) NOT NULL,
password varchar(10) NOT NULL,
PRIMARY KEY(userid,password)
);

CREATE TRIGGER aft_insert AFTER INSERT ON signup
begin
INSERT INTO login(userid,password)
    values(NEW.userid,NEW.password);
end;
