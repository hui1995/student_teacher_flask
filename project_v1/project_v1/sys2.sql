/*
 Navicat Premium Data Transfer

 Source Server         : 腾讯云
 Source Server Type    : MySQL
 Source Server Version : 50728
 Source Host           : 148.70.172.191:3306
 Source Schema         : sys2

 Target Server Type    : MySQL
 Target Server Version : 50728
 File Encoding         : 65001

 Date: 14/05/2020 12:00:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `CourseId` int(11) NOT NULL AUTO_INCREMENT,
  `courseName` varchar(50) NOT NULL,
  `totalNum` int(10) DEFAULT NULL,
  `teacherId` int(10) DEFAULT NULL,
  `teamType` int(1) DEFAULT NULL,
  PRIMARY KEY (`CourseId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for course_and_student
-- ----------------------------
DROP TABLE IF EXISTS `course_and_student`;
CREATE TABLE `course_and_student` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `CourseId` int(10) DEFAULT NULL,
  `studentId` int(10) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS `file`;
CREATE TABLE `file` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for invite
-- ----------------------------
DROP TABLE IF EXISTS `invite`;
CREATE TABLE `invite` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `inviteId` int(10) DEFAULT NULL,
  `teamId` int(10) DEFAULT NULL,
  `inviteeId` int(10) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for member
-- ----------------------------
DROP TABLE IF EXISTS `member`;
CREATE TABLE `member` (
  `contribution` varchar(50) DEFAULT NULL,
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `teamId` int(10) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `studentId` int(10) DEFAULT NULL,
  `votenum` int(10) NOT NULL DEFAULT '0',
  `isVote` int(1) DEFAULT '0',
  `leaderEvate` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `programme` varchar(50) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `GPA` float DEFAULT NULL,
  `email` varchar(24) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=17300007 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for sub_con
-- ----------------------------
DROP TABLE IF EXISTS `sub_con`;
CREATE TABLE `sub_con` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `contribution` varchar(50) NOT NULL,
  PRIMARY KEY (`contribution`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for sub_item
-- ----------------------------
DROP TABLE IF EXISTS `sub_item`;
CREATE TABLE `sub_item` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `title` varchar(50) NOT NULL,
  `percentage` float DEFAULT NULL,
  `courseId` int(10) DEFAULT NULL,
  PRIMARY KEY (`title`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  `programme` varchar(50) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for team
-- ----------------------------
DROP TABLE IF EXISTS `team`;
CREATE TABLE `team` (
  `create_time` int(11) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL,
  `TeamName` varchar(50) NOT NULL,
  `TeamNumber` int(11) NOT NULL AUTO_INCREMENT,
  `courseId` int(10) DEFAULT NULL,
  `leader` int(10) DEFAULT NULL,
  `isFinish` int(1) DEFAULT '0',
  PRIMARY KEY (`TeamNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

SET FOREIGN_KEY_CHECKS = 1;
