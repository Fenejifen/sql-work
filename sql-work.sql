/*
 Navicat Premium Data Transfer

 Source Server         : root
 Source Server Type    : MySQL
 Source Server Version : 80030 (8.0.30)
 Source Host           : localhost:3306
 Source Schema         : sql-work

 Target Server Type    : MySQL
 Target Server Version : 80030 (8.0.30)
 File Encoding         : 65001

 Date: 16/12/2022 20:30:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 书籍
-- ----------------------------
DROP TABLE IF EXISTS `书籍`;
CREATE TABLE `书籍`  (
  `ISBN` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `书名` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `作者` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `出版社` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `类型` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `馆藏总数` int NULL DEFAULT NULL,
  `可借书籍数` int NULL DEFAULT NULL,
  PRIMARY KEY (`ISBN`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of 书籍
-- ----------------------------
INSERT INTO `书籍` VALUES ('9787040406641', '数据库系统概论（第5版）', '王珊 萨师煊', '高等教育出版社', '教育', 3, 2);
INSERT INTO `书籍` VALUES ('9787040439922', '离散数学学习指导与习题解析（第2版）', '科技', '科技', '教育', 3, 3);
INSERT INTO `书籍` VALUES ('9787040595550', '走进人工智能', '吴飞', '高等教育出版社', '科技', 3, 3);

-- ----------------------------
-- Table structure for 借阅信息
-- ----------------------------
DROP TABLE IF EXISTS `借阅信息`;
CREATE TABLE `借阅信息`  (
  `借阅编号` int NOT NULL AUTO_INCREMENT,
  `学号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ISBN` char(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `借阅时间` datetime NOT NULL,
  `归还时间` datetime NULL DEFAULT NULL,
  `续借次数` int NOT NULL,
  PRIMARY KEY (`借阅编号`) USING BTREE,
  INDEX `ISBN`(`ISBN` ASC) USING BTREE,
  INDEX `学号`(`学号` ASC) USING BTREE,
  CONSTRAINT `ISBN` FOREIGN KEY (`ISBN`) REFERENCES `书籍` (`ISBN`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `学号` FOREIGN KEY (`学号`) REFERENCES `学生` (`学工号`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of 借阅信息
-- ----------------------------

-- ----------------------------
-- Table structure for 学生
-- ----------------------------
DROP TABLE IF EXISTS `学生`;
CREATE TABLE `学生`  (
  `学工号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `姓名` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `年龄` int NULL DEFAULT NULL,
  `班级` char(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `专业` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `性别` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `联系方式` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `账户密码` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `剩余可借阅书籍数` int NULL DEFAULT 3,
  PRIMARY KEY (`学工号`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of 学生
-- ----------------------------
INSERT INTO `学生` VALUES ('2020302887', '王学生', 22, '10012000', 'SE', '男', '20000000000', '123456', 3);
INSERT INTO `学生` VALUES ('2020302888', '李学生', 21, '10012000', 'CS', '男', '10000000000', '123456', 2);

-- ----------------------------
-- Table structure for 操作申请
-- ----------------------------
DROP TABLE IF EXISTS `操作申请`;
CREATE TABLE `操作申请`  (
  `操作编号` int NOT NULL AUTO_INCREMENT,
  `学号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `工号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ISBN` char(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `申请日期` datetime NOT NULL,
  `操作类型` enum('借阅','续借','归还') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `是否同意` tinyint(1) NULL DEFAULT NULL,
  `借阅编号` int NULL DEFAULT NULL,
  `备注` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`操作编号`) USING BTREE,
  INDEX `操作申请表_书籍_ISBN_fk`(`ISBN` ASC) USING BTREE,
  INDEX `操作申请表_学生_学工号_fk`(`学号` ASC) USING BTREE,
  INDEX `操作申请表_管理员_学工号_fk`(`工号` ASC) USING BTREE,
  INDEX `操作申请_借阅信息_借阅编号_fk`(`借阅编号` ASC) USING BTREE,
  CONSTRAINT `操作申请_书籍_ISBN_fk` FOREIGN KEY (`ISBN`) REFERENCES `书籍` (`ISBN`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `操作申请_借阅信息_借阅编号_fk` FOREIGN KEY (`借阅编号`) REFERENCES `借阅信息` (`借阅编号`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `操作申请_学生_学工号_fk` FOREIGN KEY (`学号`) REFERENCES `学生` (`学工号`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `操作申请_管理员_学工号_fk` FOREIGN KEY (`工号`) REFERENCES `管理员` (`学工号`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of 操作申请
-- ----------------------------
INSERT INTO `操作申请` VALUES (1, '2020302888', NULL, '9787040406641', '2022-12-16 20:13:16', '借阅', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for 管理员
-- ----------------------------
DROP TABLE IF EXISTS `管理员`;
CREATE TABLE `管理员`  (
  `学工号` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `姓名` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `账户密码` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `联系方式` char(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `性别` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `年龄` int NOT NULL,
  PRIMARY KEY (`学工号`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of 管理员
-- ----------------------------
INSERT INTO `管理员` VALUES ('2020302888', '李管理', '123456', '11111111111', '男', 22);
INSERT INTO `管理员` VALUES ('2020302889', '孙管理', '123456', '22222222222', '男', 21);

-- ----------------------------
-- View structure for 学生借阅未归还书籍信息
-- ----------------------------
DROP VIEW IF EXISTS `学生借阅未归还书籍信息`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `学生借阅未归还书籍信息` AS select `借阅信息`.`借阅编号` AS `借阅编号`,`书籍`.`ISBN` AS `ISBN`,`借阅信息`.`学号` AS `学号`,`书籍`.`书名` AS `书名`,`书籍`.`作者` AS `作者`,`借阅信息`.`借阅时间` AS `借阅时间`,(`借阅信息`.`借阅时间` + interval 2 week) AS `应还时间`,`借阅信息`.`续借次数` AS `续借次数` from (`借阅信息` join `书籍` on((`书籍`.`ISBN` = `借阅信息`.`ISBN`))) where (`借阅信息`.`归还时间` is null);

-- ----------------------------
-- View structure for 学生平台个人展示信息
-- ----------------------------
DROP VIEW IF EXISTS `学生平台个人展示信息`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `学生平台个人展示信息` AS select `学生`.`姓名` AS `姓名`,`学生`.`性别` AS `性别`,`学生`.`年龄` AS `年龄`,`学生`.`班级` AS `班级`,`学生`.`学工号` AS `学工号`,`学生`.`专业` AS `专业`,`学生`.`剩余可借阅书籍数` AS `剩余可借阅书籍数` from `学生`;

-- ----------------------------
-- View structure for 学生查询书籍信息
-- ----------------------------
DROP VIEW IF EXISTS `学生查询书籍信息`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `学生查询书籍信息` AS select `书籍`.`ISBN` AS `ISBN`,`书籍`.`书名` AS `书名`,`书籍`.`作者` AS `作者`,`书籍`.`出版社` AS `出版社`,`书籍`.`类型` AS `类型`,`书籍`.`可借书籍数` AS `可借书籍数` from `书籍`;

-- ----------------------------
-- View structure for 学生账号密码
-- ----------------------------
DROP VIEW IF EXISTS `学生账号密码`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `学生账号密码` AS select `学生`.`学工号` AS `学工号`,`学生`.`账户密码` AS `账户密码` from `学生`;

-- ----------------------------
-- View structure for 待确认事项
-- ----------------------------
DROP VIEW IF EXISTS `待确认事项`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `待确认事项` AS select `操作申请`.`操作编号` AS `操作编号`,`操作申请`.`学号` AS `学号`,`学生`.`姓名` AS `姓名`,`操作申请`.`ISBN` AS `ISBN`,`书籍`.`书名` AS `书名`,`操作申请`.`申请日期` AS `申请日期`,`操作申请`.`操作类型` AS `操作类型` from ((`操作申请` join `书籍` on((`书籍`.`ISBN` = `操作申请`.`ISBN`))) join `学生` on((`操作申请`.`学号` = `学生`.`学工号`))) where (`操作申请`.`是否同意` is null);

-- ----------------------------
-- View structure for 管理员平台个人展示信息
-- ----------------------------
DROP VIEW IF EXISTS `管理员平台个人展示信息`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `管理员平台个人展示信息` AS select `管理员`.`姓名` AS `姓名`,`管理员`.`性别` AS `性别`,`管理员`.`年龄` AS `年龄`,`管理员`.`学工号` AS `学工号` from `管理员`;

-- ----------------------------
-- View structure for 管理员账号密码
-- ----------------------------
DROP VIEW IF EXISTS `管理员账号密码`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `管理员账号密码` AS select `管理员`.`学工号` AS `学工号`,`管理员`.`账户密码` AS `账户密码` from `管理员`;

SET FOREIGN_KEY_CHECKS = 1;
