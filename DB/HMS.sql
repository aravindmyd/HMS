CREATE DATABASE IF NOT EXISTS `HMS` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `HMS`;

CREATE TABLE IF NOT EXISTS `admission` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`timestamp` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `pharmacist` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`timestamp` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `diagnostic` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`timestamp` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `admission` (`id`, `username`, `password`, `timestamp`) VALUES (1, 'adadmin', 'admin', '12/24/2018, 04:59:31');
INSERT INTO `pharmacist` (`id`, `username`, `password`, `timestamp`) VALUES (1, 'phadmin', 'admin', '12/24/2018, 04:59:31');
INSERT INTO `diagnostic` (`id`, `username`, `password`, `timestamp`) VALUES (1, 'diadmin', 'admin', '12/24/2018, 04:59:31');
 
CREATE TABLE IF NOT EXISTS `patients` (
    patientId int AUTO_INCREMENT,
    ssnId varchar(15) NOT NULL,
    patientName varchar(255) NOT NULL,
    patientAge  varchar(255) NOT NULL,
    DOJ  varchar(255) NOT NULL,
    TOB  varchar(255) NOT NULL,
    address  varchar(255) NOT NULL,
    city  varchar(255) NOT NULL,
    state  varchar(255) NOT NULL,
    status  varchar(255) NOT NULL,
    PRIMARY KEY (patientId)
);

CREATE TABLE IF NOT EXISTS `medicineMaster` (
	`medicineId` int(11) NOT NULL AUTO_INCREMENT,
  	`medicineName` varchar(50) NOT NULL,
  	`qty` varchar(255) NOT NULL,
  	`rate` varchar(100) NOT NULL,
    PRIMARY KEY (`medicineId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
insert into medicineMaster values(3,"Tonic","1500","122");
select * from medicineMaster;
CREATE TABLE IF NOT EXISTS `medicinePatient` (
	`medicineId` int(11) NOT NULL,
    `patientId` varchar(50) NOT NULL,
  	`medicineName` varchar(50) NOT NULL,
  	`qty` varchar(255) NOT NULL,
  	`rate` varchar(100) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `diagnosticMaster` (
	`testId` int(11) NOT NULL AUTO_INCREMENT,
  	`testName` varchar(50) NOT NULL,
  	`charge` varchar(255) NOT NULL,
    PRIMARY KEY (`testId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `diagnosticPatient` (
	`testId` int(11) NOT NULL,
  	`patientId` varchar(50) NOT NULL,
    `testName` varchar(50) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

select * from patients;
DELETE from patients where ssnId =45