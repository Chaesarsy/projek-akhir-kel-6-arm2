# Host: localhost  (Version 5.5.5-10.4.18-MariaDB)
# Date: 2021-05-08 01:17:57
# Generator: MySQL-Front 6.0  (Build 2.20)


#
# Structure for table "ban"
#

DROP TABLE IF EXISTS `ban`;
CREATE TABLE `ban` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal` varchar(11) DEFAULT NULL,
  `target` varchar(255) DEFAULT NULL,
  `aktual` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

#
# Data for table "ban"
#

INSERT INTO `ban` VALUES (1,'07/05/2021','6','5','under performance'),(2,'08/05/2021','3','9','performance'),(3,'09/05/2021','1','2','performance'),(4,'10/05/2021','1','4','performance'),(5,'11/05/2021','5','2','under performance'),(6,'12/05/2021','6','6','on target'),(7,'13/05/2021','5','10','performance'),(8,'14/05/2021','5','7','performance'),(9,'15/05/2021','5','10','performance'),(10,'16/05/2021','5','2','under performance'),(11,'17/05/2021','4','5','performance'),(12,'18/05/2021','2','4','performance'),(13,'19/05/2021','1','10','performance'),(14,'20/05/2021','6','1','under performance'),(15,'21/05/2021','6','6','on target');

#
# Structure for table "users"
#

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

#
# Data for table "users"
#

INSERT INTO `users` VALUES (1,'admin@admin.com','$2b$12$hfgS6mKe89nVnxBRvs2VeOEqqANb1GEJIq023gWyIVrJRkn4EqkG6','admin',1,'admin'),(2,'user@user.com','$2b$12$2cEtE93w3KYWB9vidvZvCOK2RgDBvOUWBi/g55Y9M3aS.nfZ3AGHu','user',1,'user'),(11,'user1@user.com','$2b$12$.njs0D5lEXswqM44GUam1.cYnEy.YzbLzfOJ3LKDTG0tb4jy/VELm','user',0,'user1');

#
# Structure for table "velg"
#

DROP TABLE IF EXISTS `velg`;
CREATE TABLE `velg` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal` varchar(11) DEFAULT NULL,
  `target` varchar(255) DEFAULT NULL,
  `aktual` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4;

#
# Data for table "velg"
#

INSERT INTO `velg` VALUES (1,'07/05/2021','4','4','on target'),(2,'08/05/2021','6','4','under performance'),(3,'09/05/2021','4','2','under performance'),(4,'10/05/2021','4','7','performance'),(5,'11/05/2021','5','9','performance'),(6,'12/05/2021','2','3','performance');
