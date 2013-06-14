CREATE TABLE `Users` (
`Id` int NOT NULL AUTO_INCREMENT,
`Username` varchar(20) NULL,
`Password` varchar(20) NULL,
`Phone` varchar(11) NULL,
`Email` varchar(50) NULL,
`Name` varchar(20) NULL,
`LastLoginDate` datetime NULL DEFAULT now(),
`IsDeleted` bit NULL,
`CreateDate` datetime NULL DEFAULT now(),
PRIMARY KEY (`Id`) 
);

CREATE TABLE `Tasks` (
`Id` int NOT NULL AUTO_INCREMENT,
`TopicId` int NOT NULL,
`Name` varchar(50) NULL,
`Deadline` datetime NULL,
`Status` int NULL,
`IsDeleted` bit NULL,
`CreateDate` datetime NULL DEFAULT now(),
PRIMARY KEY (`Id`) 
);

CREATE TABLE `Categories` (
`Id` int NOT NULL AUTO_INCREMENT,
`Name` varchar(20) NULL,
`Location` int NULL,
`IsDeleted` bit NULL,
PRIMARY KEY (`Id`) 
);

CREATE TABLE `References` (
`Id` int NOT NULL,
`TaskId` int NOT NULL,
`Url` varchar(500) NULL,
`IsDeleted` bit NULL,
`CreateDate` datetime NULL DEFAULT now(),
PRIMARY KEY (`Id`) 
);

CREATE TABLE `TaskActionRecords` (
`Id` int NOT NULL AUTO_INCREMENT,
`TaskId` int NOT NULL,
`UserId` int NOT NULL,
`Action` varchar(20) NULL,
`CreateDate` datetime NULL DEFAULT now(),
PRIMARY KEY (`Id`) 
);

CREATE TABLE `Topics` (
`Id` int NOT NULL AUTO_INCREMENT,
`UserId` int NOT NULL,
`CategoryId` int NOT NULL,
`Name` varchar(50) NULL,
`Status` int NULL DEFAULT 0,
`LastUpdateDate` datetime NULL DEFAULT now(),
`IsDeleted` bit NULL,
`CreateDate` datetime NULL DEFAULT now(),
PRIMARY KEY (`Id`) 
);


ALTER TABLE `Topics` ADD CONSTRAINT `fk_Topics_Users_1` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`);
ALTER TABLE `Topics` ADD CONSTRAINT `fk_Topics_Categories_1` FOREIGN KEY (`CategoryId`) REFERENCES `Categories` (`Id`);
ALTER TABLE `Tasks` ADD CONSTRAINT `fk_Tasks_Topics_1` FOREIGN KEY (`TopicId`) REFERENCES `Topics` (`Id`);
ALTER TABLE `References` ADD CONSTRAINT `fk_References_Tasks_1` FOREIGN KEY (`TaskId`) REFERENCES `Tasks` (`Id`);
ALTER TABLE `TaskActionRecords` ADD CONSTRAINT `fk_DoneRecords_Tasks_1` FOREIGN KEY (`TaskId`) REFERENCES `Tasks` (`Id`);
ALTER TABLE `TaskActionRecords` ADD CONSTRAINT `fk_TaskActionRecords_Users_1` FOREIGN KEY (`UserId`) REFERENCES `Users` (`Id`);

