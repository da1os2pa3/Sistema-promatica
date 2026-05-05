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
-- Table structure for table `marcas`
--

DROP TABLE IF EXISTS `marcas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `marcas` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ma_nombre` varchar(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `marcas`
--

LOCK TABLES `marcas` WRITE;
/*!40000 ALTER TABLE `marcas` DISABLE KEYS */;
INSERT INTO `marcas` VALUES (1,'Tp-link'),(2,'Evertec'),(3,'Genius'),(4,'Logitech'),(5,'Kingston'),(6,'CDtek'),(7,'Office'),(8,'Blow'),(9,'Premiun'),(10,'E-view'),(11,'Nisuta'),(12,'Netmak'),(13,'Gneiss'),(14,'Amd'),(15,'Gigabyte'),(16,'Intel'),(17,'Cromax'),(18,'Performance'),(19,'Thermaltek'),(20,'Gamemax'),(21,'Delta'),(22,'Epson'),(23,'HPinc'),(24,'IntCo'),(25,'Xtech'),(26,'Belsic'),(28,'Global'),(29,'Tecnovibe'),(42,'Over'),(43,'BKT'),(44,'Boreal'),(45,'BIO'),(46,'Klipxtreme'),(47,'Coprint'),(48,'INK CARTRIGE'),(49,'Philips'),(50,'Hikvision'),(52,'Sandisk'),(55,'TripleKit'),(56,'Promatica'),(57,'Msi'),(58,'Only'),(59,'Aoweixun'),(60,'Puresonic'),(61,'Skyway'),(62,'Kaise'),(63,'Cooler-Master'),(66,'Lenovo'),(67,'Csb'),(68,'Brother'),(69,'Soul'),(70,'Duracel'),(71,'Bags'),(72,'WD'),(73,'Xiaomi'),(74,'Asus'),(75,'Glc'),(76,'Noganet'),(78,'Furukawa'),(79,'Aerocool'),(80,'SINMARCA'),(81,'Interno'),(83,'Compulogic'),(84,'Generico'),(85,'Trv'),(86,'Maxell'),(87,'Mixor'),(88,'Hiksemi'),(89,'Kolke'),(90,'CX'),(91,'NextOne'),(92,'StarInk'),(93,'Ubiquiti'),(94,'Bbox'),(96,'Fiat'),(103,'Bitpower'),(104,'Lyonn'),(105,'Mti'),(106,'Xo');
/*!40000 ALTER TABLE `marcas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-28 17:01:15
