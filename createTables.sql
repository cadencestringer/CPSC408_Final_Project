CREATE DATABASE Cookies;

USE Cookies;

DROP TABLE OrderDetails;
DROP TABLE CustomerOrder;
DROP TABLE Customer;
DROP TABLE Store;
DROP TABLE Cookie;

# Creates tables

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
    zipcode  VARCHAR(5)                    NOT NULL,
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
    deleted  BOOLEAN                  NOT NULL,
    FOREIGN KEY (orderID)
        REFERENCES CustomerOrder (orderID),
    FOREIGN KEY (cookieID)
        REFERENCES Cookie (cookieID)
);


# Indexes

CREATE INDEX Cookie_cookieID_index
 on Cookie (cookieID);

CREATE INDEX Customer_customerID_index
 on Customer (customerID);

CREATE INDEX CustomerOrder_orderID_index
 on CustomerOrder (orderID);

CREATE INDEX OrderDetails_detailID_index
 on OrderDetails (detailID);

CREATE INDEX Store_storeID_index
 on Store (storeID);

CREATE VIEW Customer_Metrics AS SELECT sex, age FROM Customer;


# Stored Procedures:

CREATE PROCEDURE SelectCookies()
BEGIN
    SELECT * FROM Cookie;
END;

CREATE PROCEDURE SelectCookieName(IN cookieName VARCHAR(50))
BEGIN
    SELECT * FROM Cookie
    WHERE flavor = cookieName AND deleted = 0;
END;

CREATE PROCEDURE SelectStoreName(IN storeName VARCHAR(50))
BEGIN
    SELECT * FROM Store
    WHERE name = storeName AND deleted = 0;
END;

CREATE PROCEDURE SelectCustFName(IN name VARCHAR(30))
BEGIN
    SELECT * FROM Customer
    WHERE fName = name AND deleted = 0;
END;

CREATE PROCEDURE SelectCustLName(IN name VARCHAR(30))
BEGIN
    SELECT * FROM Customer
    WHERE lName = name AND deleted = 0;
END;

CREATE PROCEDURE SelectCustLName(IN name VARCHAR(30))
BEGIN
    SELECT * FROM Customer
    WHERE lName = name AND deleted = 0;
END;
