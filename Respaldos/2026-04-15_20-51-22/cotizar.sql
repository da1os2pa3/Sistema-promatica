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
-- Table structure for table `cotizar`
--

DROP TABLE IF EXISTS `cotizar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cotizar` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `cz_fecha` date NOT NULL,
  `cz_numcotiz` int(8) NOT NULL,
  `cz_codcli` int(5) NOT NULL DEFAULT 0,
  `cz_apellido` varchar(20) NOT NULL DEFAULT '',
  `cz_nombre` varchar(25) NOT NULL DEFAULT '',
  `cz_sitfis` varchar(2) NOT NULL,
  `cz_cuit` varchar(13) NOT NULL,
  `cz_tipopago` varchar(20) NOT NULL,
  `cz_detpago` varchar(100) NOT NULL,
  `cz_impago` float(15,2) NOT NULL DEFAULT 0.00,
  `cz_totcotiz` float(15,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `ind_nunvta` (`cz_numcotiz`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizar`
--

LOCK TABLES `cotizar` WRITE;
/*!40000 ALTER TABLE `cotizar` DISABLE KEYS */;
INSERT INTO `cotizar` VALUES (1,'2023-01-29',10,1254,'Pasin','Daniel','RI','20132720674','efectivo','billetes',850.00,850.00),(2,'2023-02-05',11,2548,'Manso','Olga Edith','CF','','cheque','30 dias',1450.00,1450.00);
/*!40000 ALTER TABLE `cotizar` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-15 20:51:22
