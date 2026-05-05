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
-- Table structure for table `funcsel`
--

DROP TABLE IF EXISTS `funcsel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcsel` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `fs_dato1` varchar(150) NOT NULL DEFAULT '' COMMENT 'Lo hago mas grande para que vaya el nombre de cliente, articulo, proveedor o lo que sea descriptivo primero',
  `fs_dato2` varchar(20) NOT NULL DEFAULT '' COMMENT 'este es para usar con codigos y datos mas cortos',
  `fs_dato3` decimal(15,2) NOT NULL DEFAULT 0.00 COMMENT 'este es numerico con decimales, para usar con importes',
  `fs_dato4` varchar(20) NOT NULL DEFAULT '' COMMENT 'este puede usarse con fechas guardandolas tipo str',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabla auxilliar para usar en la seleccion de cliente, articulos, proveedores ... etc.';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcsel`
--

LOCK TABLES `funcsel` WRITE;
/*!40000 ALTER TABLE `funcsel` DISABLE KEYS */;
INSERT INTO `funcsel` VALUES (2,'Pasin Carlos','59',0.00,'hola'),(3,'Pasin Fernando','219',0.00,'hola'),(4,'PASIN DANIEL OSCAR','2138',0.00,'hola'),(5,'Pasini Joaco','2655',0.00,'hola'),(6,'GOMEZ HECTOR','798',0.00,'hola'),(7,'GOMEZ NATASHA','865',0.00,'hola'),(8,'Gomez Cristian','898',0.00,'hola'),(9,'GOMEZ SILVINA','1071',0.00,'hola'),(10,'GOMEZ GRACIELA','1286',0.00,'hola'),(11,'GOMEZ EDUARDO','1373',0.00,'hola'),(12,'Gomez GOMEZ MARCELA','1471',0.00,'hola'),(13,'GOMEZ GUILLERMO','1538',0.00,'hola'),(14,'GOMEZ CAROLINA','1554',0.00,'hola'),(15,'GOMEZ NATALIA','1619',0.00,'hola'),(16,'GOMEZ FABIAN MARCELO','1667',0.00,'hola'),(17,'GOMEZ DIEGO GOMEZ DIEGO','2545',0.00,'hola'),(18,'GOMEZ GOMEZ ALICIA LIDIA','2566',0.00,'hola'),(19,'GOMEZ JOSE LUIS GOMEZ JOSE LUIS','2587',0.00,'hola'),(20,'Gomez Jorgelina','2735',0.00,'hola'),(21,'Gomez Pablo Sergio','2748',0.00,'hola'),(22,'Pasin Carlos','59',0.00,'hola'),(23,'Pasin Fernando','219',0.00,'hola'),(24,'PASIN DANIEL OSCAR','2138',0.00,'hola'),(25,'Pasini Joaco','2655',0.00,'hola');
/*!40000 ALTER TABLE `funcsel` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-20 19:30:44
