CREATE DATABASE IF NOT EXISTS `HMS` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `HMS`;

CREATE TABLE IF NOT EXISTS `userstore` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`timestamp` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `userstore` (`id`, `username`, `password`, `timestamp`) VALUES (1, 'test', 'test', '12/24/2018, 04:59:31');
