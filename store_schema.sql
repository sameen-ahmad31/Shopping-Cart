PRAGMA foreign_keys=off;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
  username varchar(50) not null PRIMARY KEY,
  password varchar(50) not null,
  fname    varchar(50) not null,
  lname    varchar(50) not null
);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  user_ varchar(50) not null PRIMARY KEY,
  dateOfOrd varchar(50) not null,
  total    integer not null,
  FOREIGN KEY (user_) REFERENCES user(username)
);

DROP TABLE IF EXISTS orderItem;
CREATE TABLE orderItem (
  id integer not null,
  user_email varchar(50) not null,
  dateOfOrd varchar(50) not null,
  product_id integer not null,
  product_name   varchar(50) not null,
  quantity   integer not null,
  FOREIGN KEY (user_email) REFERENCES user(username),
  FOREIGN KEY (product_id) REFERENCES product(id),
  FOREIGN KEY (product_name) REFERENCES product(name)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  id        integer not null PRIMARY KEY,
  name       varchar(50) not null,
  price       integer not null,
  stock       integer not null,
  category_id    integer not null,
  pic   varchar not null,
  description varchar not null,
  FOREIGN KEY (category_id) REFERENCES category(id)
);

DROP TABLE IF EXISTS category;
CREATE TABLE category (
  id         integer not null PRIMARY KEY,
  name       varchar(50) not null
);

INSERT INTO category VALUES (10, 'Coffee Beans');
INSERT INTO category VALUES (11, 'Ground Coffee');
INSERT INTO category VALUES (12, 'Miscellaneous');

INSERT INTO user VALUES ('testuser', 'testpass', 'Test', 'User');
INSERT INTO user VALUES ('smessina', 'abehkf01!', 'Shea', 'Messina');
INSERT INTO user VALUES ('bellarina', 'jfdvnkdfjd23@1', 'Bella', 'Barrera');
INSERT INTO user VALUES ('issi', 'jfdakjfvj873!az', 'Isabelle', 'Cordero');
INSERT INTO user VALUES ('pupatella', 'dkfjdkjfvi89@1!', 'Sara', 'Ahmad');
INSERT INTO user VALUES ('kpiccorossi', 'itaespn31!', 'Krystyna', 'Piccorossi');

INSERT INTO product VALUES (100, 'Espresso Italiano Classico Coffee Beans', 9.99, 50, 10, 'static/espresso.jpeg', 'Made with love and care, the Espresso Italiano Classico coffee beans are a classic blend of high-quality Arabica beans, roasted to perfection in the traditional Italian style!');
INSERT INTO product VALUES (101, 'Crema Coffee Beans', 12.99, 35, 10, 'static/crema.png', 'Made with high-quality ingredients, the Crema Beans add a delicious creamy crema to your daily coffee while you enjoy the rich flavor and creamy texture');
INSERT INTO product VALUES (102, 'Churros Coffee Beans', 19.99, 98, 10, 'static/churros.jpg', 'One our favorite recipes, beautifully made with the traditional Spanish churros blending it with the high-quality coffee beans to give you a unique taste of coffee only at El Café de España');
INSERT INTO product VALUES (103, 'Creme Caramel Coffee Beans', 8.99, 12, 10, 'static/caramel.png', 'Infused with the flavor of the creamy caramel this delicious blend of coffee gives a sweet yet fulfilling experience for the coffee lovers who want to start their morning filled with nothing but sweetness');

INSERT INTO product VALUES (200, 'Decaf Ground Coffee', 9.99, 60, 11, 'static/groundcoff.jpeg', 'For all the coffee lovers out there who desire to drink coffee without caffeine. This Decaf Ground Coffee is delicately designed for you. It brings the rich flavor and aroma of coffee while having no caffeine content at all!');
INSERT INTO product VALUES (201, 'Tiramisu Ground Coffee', 13.99, 48, 11, 'static/groundcaf3.jpg', 'One our favorite recipes of all time, the Tiramisu Ground Coffee is infused with the Italian dessert Tiramisu and the high-quality Arabica coffee beans to bring you  a delightful coffee experience');
INSERT INTO product VALUES (202, 'Tres Leches Ground Coffee', 7.99, 55, 11, 'static/groundcoffe2.jpg', 'Only served at El Café de España, the Tres Leches Ground Coffee strives to blend the popular Latin American dessert, Tres Leches cake with the ground coffee so our coffee lovers can enjoy their morning with the delicious cup of coffee');
INSERT INTO product VALUES (203, 'Churros Ground Coffee', 11.99, 29, 11, 'static/cgc.png', 'Perfectly and carefully crafted, passed down through generations, perfectly and carefully crafted with the blend of the traditional Spanish churros and the high-quality ground coffee, we strive to enhance the natural sweetness of the coffee while bringing out the rich and delicious flavor of the Churros');

INSERT INTO product VALUES (300, 'Espresso Shots', 15.99, 70, 12, 'static/shots.png', 'For our Die-Hard Coffee Lovers, who need that little more caffeine than others, the Espresso Shots is for you! Served in a small cup, it gives a quick burst of caffeine while maintaining the rich and creamy flavor of the coffee');
INSERT INTO product VALUES (301, 'Cups', 20.99, 37, 12, 'static/cups.png', 'An essential part of the coffee experience are the coffee cups, the right coffee cup can enhance the overall coffee experience. Here at El Café de España, we craft our own coffee cups to bring you delightful experience');
INSERT INTO product VALUES (302, 'Straws', 9.99, 48, 12, 'static/straws.png', 'Our beautiful straws reflecting the Spanish heritage come in a pack of 10 straws each which are designed to assist you in sipping your coffee while preserving the layers of cream on top');
