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
-- Table structure for table `resu_ventas`
--

DROP TABLE IF EXISTS `resu_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resu_ventas` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `rv_numero` int(10) NOT NULL DEFAULT 0,
  `rv_fecha` date DEFAULT NULL,
  `rv_cod_cliente` int(5) NOT NULL DEFAULT 0,
  `rv_cliente` varchar(45) NOT NULL DEFAULT '',
  `rv_sitfis` varchar(40) NOT NULL DEFAULT '',
  `rv_cuit` varchar(13) NOT NULL DEFAULT '',
  `rv_tipo_pago` varchar(30) NOT NULL DEFAULT '',
  `rv_detalle_pago` varchar(100) NOT NULL DEFAULT '',
  `rv_dolarhoy` decimal(10,2) NOT NULL DEFAULT 0.00,
  `rv_total` decimal(10,2) NOT NULL DEFAULT 0.00,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resu_ventas`
--

LOCK TABLES `resu_ventas` WRITE;
/*!40000 ALTER TABLE `resu_ventas` DISABLE KEYS */;
INSERT INTO `resu_ventas` VALUES (8,2,'2024-09-30',2245,'Barrionuevo Matias Nicolas','CF - Consumidor Final','','Efectivo','',994.00,13800.00),(10,1,'2024-09-30',678,'Frances Carlos','CF - Consumidor Final','','Cuenta Corriente','la llevo para probar',994.00,25500.00),(12,5,'2024-10-03',2103,'Mustafa Melisa','CF - Consumidor Final','','Efectivo','',994.00,7000.00),(14,7,'2024-10-03',2236,'Vega Gerardo','CF - Consumidor Final','','Efectivo','',994.00,9200.25),(36,26,'2026-03-07',2914,'Vezzosi Jorge','CF - Consumidor Final','','Efectivo','',1450.00,110000.00),(40,29,'2026-03-11',1933,'Kamar Gustavo','CF - Consumidor Final','','Efectivo','',1450.00,2700.00),(42,30,'2026-03-13',0,'Consumidor Final','CF - Consumidor Final','','Efectivo','',1450.00,19600.00),(44,28,'2026-03-09',60,'Arenas propiedades ','CF - Consumidor Final','','Efectivo','',1450.00,354000.00),(45,31,'2026-03-18',0,'Consumidor Final','CF - Consumidor Final','','Efectivo','',1450.00,26700.00),(46,32,'2026-03-26',0,'Consumidor Final','CF - Consumidor Final','','Efectivo','',1450.00,31000.00),(47,33,'2026-04-15',0,'Consumidor Final','CF - Consumidor Final','','Efectivo','',1420.00,48000.00),(49,34,'2026-04-28',842,'Josecito Gas ','CF - Consumidor Final','','Efectivo','',1450.00,33000.00);
/*!40000 ALTER TABLE `resu_ventas` ENABLE KEYS */;
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
