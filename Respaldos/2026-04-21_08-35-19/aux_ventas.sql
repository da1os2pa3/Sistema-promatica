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
-- Table structure for table `aux_ventas`
--

DROP TABLE IF EXISTS `aux_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aux_ventas` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `av_codigo_art` varchar(30) NOT NULL DEFAULT '',
  `av_desc_art` varchar(100) NOT NULL DEFAULT '',
  `av_marca_art` varchar(60) NOT NULL DEFAULT '',
  `av_cantidad` int(5) NOT NULL DEFAULT 0,
  `av_tot_uni_conta` decimal(12,2) NOT NULL DEFAULT 0.00,
  `av_tot_uni_lista` decimal(11,2) NOT NULL DEFAULT 0.00,
  `av_neto_unidad` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_impor_iva21` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_impor_iva105` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_impor_ganancia` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_costo_bruto` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_costo_dolar` decimal(10,2) NOT NULL DEFAULT 0.00,
  `av_tasaiva` decimal(5,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=342 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aux_ventas`
--

LOCK TABLES `aux_ventas` WRITE;
/*!40000 ALTER TABLE `aux_ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `aux_ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21  8:35:19
