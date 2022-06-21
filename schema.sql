CREATE TABLE messages(
    ID int NOT NULL AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    message varchar(512) NOT NULL,
    PRIMARY KEY (ID)
);