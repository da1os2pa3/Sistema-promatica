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
-- Table structure for table `informa`
--

DROP TABLE IF EXISTS `informa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `informa` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `i_empresa` varchar(30) NOT NULL DEFAULT '',
  `i_direccion` varchar(30) NOT NULL DEFAULT '',
  `i_localidad` varchar(20) NOT NULL DEFAULT '',
  `i_provincia` varchar(15) NOT NULL DEFAULT '',
  `i_postal` varchar(5) NOT NULL DEFAULT '',
  `i_correo` varchar(40) NOT NULL DEFAULT '',
  `i_telef1` varchar(15) NOT NULL DEFAULT '',
  `i_telef2` varchar(15) NOT NULL DEFAULT '',
  `i_titular` varchar(30) NOT NULL DEFAULT '',
  `i_contacto` varchar(30) NOT NULL DEFAULT '',
  `i_sitfis` varchar(20) NOT NULL DEFAULT '',
  `i_cuit` varchar(13) NOT NULL DEFAULT '',
  `i_rentas` varchar(20) NOT NULL DEFAULT '',
  `i_municip` varchar(20) NOT NULL DEFAULT '',
  `i_iva1` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_iva2` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_iva3` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_impint` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_reten` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_percep` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_dolar1` decimal(10,2) NOT NULL DEFAULT 0.00,
  `i_dolar2` decimal(10,2) NOT NULL DEFAULT 0.00,
  `i_cargo1_tarj` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_cargo2_tarj` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_cargo3_tarj` decimal(5,2) NOT NULL DEFAULT 0.00,
  `i_ultimo_saldo` decimal(12,2) NOT NULL DEFAULT 0.00,
  `i_ruta_fotos` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informa`
--

LOCK TABLES `informa` WRITE;
/*!40000 ALTER TABLE `informa` DISABLE KEYS */;
INSERT INTO `informa` VALUES (1,'Promatica computacion','Avda. Estrada 318','Villa C. Paz','Cordoba','5152','promatica@gmail.com','3541-330082','','Pasin Daniel Oscar','','RI - Responsable Ins','20132720674','','',21.00,10.50,0.00,4.00,4.00,4.00,1420.00,1420.00,10.00,20.00,0.00,1560.00,'\"C:\\\\Proyectos_Python\\\\ABM_Clientes\\\\fotos\"');
/*!40000 ALTER TABLE `informa` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-16 18:49:20
