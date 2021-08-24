-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.6.0-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- tasks 데이터베이스 구조 내보내기
DROP DATABASE IF EXISTS `tasks`;
CREATE DATABASE IF NOT EXISTS `tasks` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tasks`;

-- 테이블 tasks.auth 구조 내보내기
DROP TABLE IF EXISTS `auth`;
CREATE TABLE IF NOT EXISTS `auth` (
  `address` text DEFAULT NULL,
  `token` text DEFAULT NULL,
  `user` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.buylog 구조 내보내기
DROP TABLE IF EXISTS `buylog`;
CREATE TABLE IF NOT EXISTS `buylog` (
  `sites` bigint(19) DEFAULT NULL,
  `id` text DEFAULT NULL,
  `name` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.captcha 구조 내보내기
DROP TABLE IF EXISTS `captcha`;
CREATE TABLE IF NOT EXISTS `captcha` (
  `address` text DEFAULT NULL,
  `token` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.category 구조 내보내기
DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `site` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` mediumtext DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.codelog 구조 내보내기
DROP TABLE IF EXISTS `codelog`;
CREATE TABLE IF NOT EXISTS `codelog` (
  `sites` int(11) DEFAULT NULL,
  `id` mediumtext DEFAULT NULL,
  `code` text DEFAULT NULL,
  `name` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.coupon 구조 내보내기
DROP TABLE IF EXISTS `coupon`;
CREATE TABLE IF NOT EXISTS `coupon` (
  `sites` int(11) DEFAULT NULL,
  `number` text DEFAULT NULL,
  `amount` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.cracking 구조 내보내기
DROP TABLE IF EXISTS `cracking`;
CREATE TABLE IF NOT EXISTS `cracking` (
  `name` text DEFAULT NULL,
  `hwid` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.label 구조 내보내기
DROP TABLE IF EXISTS `label`;
CREATE TABLE IF NOT EXISTS `label` (
  `site` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `day` text DEFAULT NULL,
  `value` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.license 구조 내보내기
DROP TABLE IF EXISTS `license`;
CREATE TABLE IF NOT EXISTS `license` (
  `code` text DEFAULT NULL,
  `day` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.price 구조 내보내기
DROP TABLE IF EXISTS `price`;
CREATE TABLE IF NOT EXISTS `price` (
  `sites` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `rank` text DEFAULT NULL,
  `day` text DEFAULT NULL,
  `amount` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.product 구조 내보내기
DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `site` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `image` text DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `low` int(11) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.raw 구조 내보내기
DROP TABLE IF EXISTS `raw`;
CREATE TABLE IF NOT EXISTS `raw` (
  `id` mediumtext DEFAULT NULL,
  `context` mediumtext DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.sites 구조 내보내기
DROP TABLE IF EXISTS `sites`;
CREATE TABLE IF NOT EXISTS `sites` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address` text DEFAULT NULL,
  `message` text DEFAULT NULL,
  `account` text DEFAULT NULL,
  `culture` text DEFAULT NULL,
  `culturedown` int(11) DEFAULT NULL,
  `discordwebhook` text DEFAULT NULL,
  `bankpin` text DEFAULT NULL,
  `cultureapi` text DEFAULT NULL,
  `name` text DEFAULT NULL,
  `verify` text DEFAULT NULL,
  `by` text DEFAULT NULL,
  `end` text DEFAULT NULL,
  `guild` text DEFAULT NULL,
  `role` text DEFAULT NULL,
  `message2` text DEFAULT NULL,
  `message3` text DEFAULT NULL,
  `message4` text DEFAULT NULL,
  `channelplugin` text DEFAULT NULL,
  `refer_percent` int(11) DEFAULT 0,
  `color` text DEFAULT '4e4e50|1a1a1d|fff|2c2c2e|fff|1a1a1d|fff|fff|gray|fff|302f2f',
  `music` text DEFAULT NULL,
  `buylog` text DEFAULT NULL,
  `logo` text DEFAULT NULL,
  `template` mediumtext DEFAULT 'Default',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.stock 구조 내보내기
DROP TABLE IF EXISTS `stock`;
CREATE TABLE IF NOT EXISTS `stock` (
  `sites` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `stock` text DEFAULT NULL,
  `day` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.user 구조 내보내기
DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `sites` int(11) DEFAULT NULL,
  `name` text DEFAULT NULL,
  `pw` text DEFAULT NULL,
  `number` text DEFAULT NULL,
  `money` text DEFAULT NULL,
  `rank` text DEFAULT NULL,
  `bankname` text DEFAULT NULL,
  `did` text DEFAULT NULL,
  `refer_code` text DEFAULT NULL,
  `refer_by` text DEFAULT NULL,
  `refer_count` int(11) DEFAULT 0,
  `buyamount` int(11) DEFAULT 0
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.verify 구조 내보내기
DROP TABLE IF EXISTS `verify`;
CREATE TABLE IF NOT EXISTS `verify` (
  `number` text DEFAULT NULL,
  `code` text DEFAULT NULL,
  `isVerify` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 tasks.visitlog 구조 내보내기
DROP TABLE IF EXISTS `visitlog`;
CREATE TABLE IF NOT EXISTS `visitlog` (
  `sites` int(11) DEFAULT NULL,
  `id` text DEFAULT NULL,
  `ip` text DEFAULT NULL,
  `isban` text DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- 내보낼 데이터가 선택되어 있지 않습니다.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
