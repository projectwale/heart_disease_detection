/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - object_detect
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`object_detect` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `object_detect`;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userid` int(255) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `email` varchar(50) default NULL,
  `password` varchar(50) default NULL,
  UNIQUE KEY `userid` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`userid`,`name`,`email`,`password`) values (1,'asd','a@gmail.com','a');

/*Table structure for table `user_info` */

DROP TABLE IF EXISTS `user_info`;

CREATE TABLE `user_info` (
  `Uid` int(255) NOT NULL auto_increment,
  `UserName` varchar(255) NOT NULL,
  `UserEmail` varchar(255) NOT NULL,
  `UserMobile` varchar(255) NOT NULL,
  PRIMARY KEY  (`Uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `user_info` */

insert  into `user_info`(`Uid`,`UserName`,`UserEmail`,`UserMobile`) values (1,'Sushant','s@gmail.com','9856321470');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
