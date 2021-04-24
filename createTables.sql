#CREATE DATABASE Cookies;

DROP TABLE OrderDetails;
DROP TABLE CustomerOrder;
DROP TABLE Customer;
DROP TABLE Store;
DROP TABLE Cookie;

CREATE TABLE Cookie
(
    cookieID TINYINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    flavor   VARCHAR(50)                  NOT NULL,
    cost     FLOAT(3, 2)                  NOT NULL,
    deleted  BOOLEAN                      NOT NULL
);

CREATE TABLE Customer
(
    customerID INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fName      VARCHAR(30)              NOT NULL,
    lName      VARCHAR(30)              NOT NULL,
    sex        CHAR(1)                  NOT NULL,
    age        TINYINT UNSIGNED         NOT NULL,
    deleted    BOOLEAN                  NOT NULL
);

CREATE TABLE Store
(
    storeID  SMALLINT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name     VARCHAR(50)                   NOT NULL,
    state    VARCHAR(30)                   NOT NULL,
    phoneNum VARCHAR(25)                   NOT NULL,
    deleted  BOOLEAN                       NOT NULL
);

CREATE TABLE CustomerOrder
(
    orderID    INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    customerID INT UNSIGNED             NOT NULL,
    storeID    SMALLINT UNSIGNED        NOT NULL,
    orderDate  DATETIME                 NOT NULL,
    deleted    BOOLEAN                  NOT NULL,
    FOREIGN KEY (customerID)
        REFERENCES Customer (customerID),
    FOREIGN KEY (storeID)
        REFERENCES Store (storeID)
);

CREATE TABLE OrderDetails
(
    detailID INT UNSIGNED PRIMARY KEY NOT NULL AUTO_INCREMENT,
    orderID  INT UNSIGNED             NOT NULL,
    cookieID TINYINT UNSIGNED         NOT NULL,
    quantity TINYINT UNSIGNED         NOT NULL,
    price    FLOAT(5, 2)              NOT NULL,
    deleted  BOOLEAN                  NOT NULL,
    FOREIGN KEY (orderID)
        REFERENCES CustomerOrder (orderID),
    FOREIGN KEY (cookieID)
        REFERENCES Cookie (cookieID)
);