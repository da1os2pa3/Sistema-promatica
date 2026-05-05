-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: sist_prom
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `saldosctacte`
--

DROP TABLE IF EXISTS `saldosctacte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saldosctacte` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `scc_codcli` decimal(7,0) DEFAULT NULL COMMENT 'codigo del cliente',
  `scc_nomcli` varchar(60) NOT NULL DEFAULT '' COMMENT 'nombre del cliente',
  `scc_saldo` decimal(15,2) NOT NULL DEFAULT 0.00 COMMENT 'saldo del cliente',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3725 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Es auxilliar donde cargo cada cliente y su saldo para luego imprimirla';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saldosctacte`
--

LOCK TABLES `saldosctacte` WRITE;
/*!40000 ALTER TABLE `saldosctacte` DISABLE KEYS */;
INSERT INTO `saldosctacte` VALUES (3711,200,'Colasanto Jose',2000.00),(3712,243,'Vila Daniel',45000.00),(3713,260,'Marshal Eduardo',800.00),(3714,781,'Meneses - Alta Imagen ',-20000.00),(3715,1029,'Martinez Sady',1800.00),(3716,1830,'Regalli Gonzalo',2000.00),(3717,1863,'Pinat Daniel  nueva cuenta',379791.00),(3718,1933,'KAMAR GUSTAVO',8000.00),(3719,2089,'Zappa Fabiana',-2000.00),(3720,2335,'Mato Eduardo',-900.00),(3721,2385,'Luque Patricia',1500.00),(3722,2465,'Serra Filadelfo',60000.00),(3723,2511,'Paz Tobias',6800.00),(3724,2602,'Restorant Los Abuelos',500.00);
/*!40000 ALTER TABLE `saldosctacte` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-20 19:30:45
