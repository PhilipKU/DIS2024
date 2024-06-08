DROP TABLE IF EXISTS Desserts;
DROP TABLE IF EXISTS French_fries;
DROP TABLE IF EXISTS Beverages;
DROP TABLE IF EXISTS Burgers;
DROP TABLE IF EXISTS Food;
DROP TABLE IF EXISTS Complaints;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Users;

CREATE TABLE IF NOT EXISTS Food(
    id serial PRIMARY KEY,
    price float,
    amount integer
    );


CREATE TABLE IF NOT EXISTS Users(
    userid serial primary key, 
    username varchar(30) UNIQUE, 
    budget float
    ); 


CREATE TABLE IF NOT EXISTS Orders(
    orderid serial primary key, 
    customerid integer REFERENCES Users(userid) ON DELETE CASCADE 
    );  

CREATE TABLE IF NOT EXISTS Complaints(
    orderid integer REFERENCES Orders(orderid) ON DELETE CASCADE,
    phonenumber integer,
    complaint_text VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS Burgers(
    burger_type varchar(20), 
    patty_type varchar(20), 
    bun_type varchar(20),
    orderid integer REFERENCES Orders(orderid) ON DELETE CASCADE,
    food_id integer PRIMARY KEY, 
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
    );  


CREATE TABLE IF NOT EXISTS Beverages(
    beverage_type varchar(20), 
    beverage_volume integer, 
    orderid integer REFERENCES Orders(orderid) ON DELETE CASCADE,
    food_id integer PRIMARY KEY, 
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
    );


CREATE TABLE IF NOT EXISTS French_fries(
    french_fries_type varchar(20), 
    french_fries_size varchar(20), 
    orderid integer REFERENCES Orders(orderid) ON DELETE CASCADE,
    food_id integer PRIMARY KEY, 
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
    );


CREATE TABLE IF NOT EXISTS  Desserts(
    dessert_type varchar(20), 
    dessert_size varchar(20),
    orderid integer REFERENCES Orders(orderid) ON DELETE CASCADE,
    food_id integer PRIMARY KEY, 
    FOREIGN KEY (food_id) REFERENCES Food(id) ON DELETE CASCADE
    );

start transaction;

insert into Users (username, budget) values ('Anders And1', 250.12);
insert into Users (username, budget) values ('Anders And2', 350.42);
insert into Users (username, budget) values ('Anders And3', 450.44);
insert into Users (username, budget) values ('Anders And4', 550.55);
insert into Users (username, budget) values ('Anders And5', 650);
insert into Users (username, budget) values ('Anders And6', 750);
insert into Users (username, budget) values ('Anders And7', 850);
insert into Users (username, budget) values ('Anders And8', 950);
insert into Users (username, budget) values ('Anders And9', 1050);
insert into Users (username, budget) values ('Anders And10', 1150);

commit;
