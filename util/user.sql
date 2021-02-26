CREATE DATABASE Chat;
USE Chat;

CREATE TABLE Users(
    account char(20) NOT NULL UNIQUE,
    passwd  char(20) NOT NULL,
    name    char(20) NOT NULL,
    user_id  int AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE Friend(
    user_id int NOT NULL,
    friend_id int NOT NULL,
    accepted Boolean DEFAULT false,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES Users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (user_id,friend_id)
);

CREATE TABLE FriendHistory(
    user_id int NOT NULL,
    friend_id int NOT NULL,
    message text,
    extra_address varchar(80) DEFAULT NULL,
    create_time DATETIME DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    accepted Boolean DEFAULT FALSE
);

CREATE TABLE Room(
    room_id int AUTO_INCREMENT PRIMARY KEY,
    name char(20)
);

CREATE TABLE RoomUser(
    room_id int NOT NULL,
    user_id int NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY(room_id,user_id)
);

CREATE TABLE RoomHistory(
    room_id int NOT NULL,
    user_id int NOT NULL,
    message text,
    extra_address varchar(80) DEFAULT NULL,
    create_time DATETIME DEFAULT NULL,
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    accepted Boolean DEFAULT FALSE
);