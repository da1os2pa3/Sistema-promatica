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
-- Table structure for table `faltantes`
--

DROP TABLE IF EXISTS `faltantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faltantes` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `fa_fecha` date DEFAULT NULL,
  `fa_articulo` varchar(120) NOT NULL DEFAULT '',
  `fa_estado` varchar(10) NOT NULL DEFAULT '' COMMENT 'si esta pendiente de comprar o ya se compro',
  `fa_observaciones` varchar(150) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='para anotar los articulos que faltan y que hay que comprar';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faltantes`
--

LOCK TABLES `faltantes` WRITE;
/*!40000 ALTER TABLE `faltantes` DISABLE KEYS */;
INSERT INTO `faltantes` VALUES (58,'2024-11-30','ROLLO CABLE UTP 305MTS - INTERIOR - CAT5E -NM-R01- NETMAK','Comprado',''),(123,'2025-07-14','NM-C81A adaptador','Pendiente',''),(126,'2025-08-01','TONER 2612','Finalizado',''),(130,'2025-08-26','fuente lenovo 24284','Finalizado',''),(144,'2025-11-21','toner 103L muni icho cruz','Finalizado',''),(146,'2025-11-27','toner 1105 comprar tres o cuatro - se esta vendiendo mas','Finalizado',''),(147,'2025-12-01','cartuchosd 133 negro','Finalizado',''),(152,'2025-12-12','cargador lenovo  pin fino ojo... no es el 1701030','Finalizado',''),(154,'2025-12-16','tp-link EAP 225 exteriores','Pendiente',''),(157,'2025-12-31','fuente gamemax de 500 o 600 VPN bronze','Finalizado',''),(158,'2025-12-31','conversores HDMI a VGA','Finalizado',''),(160,'2026-01-09','cable usb c99','Finalizado',''),(161,'2026-01-10','toner 279','Finalizado',''),(168,'2026-02-24','nm-117-b','Pendiente',''),(171,'2026-02-26','UPS Lyon','Pendiente',''),(178,'2026-04-22','pad numerico de teclado','Pendiente',''),(179,'2026-04-23','logitech mk250 mouse y teclado','Pendiente','');
/*!40000 ALTER TABLE `faltantes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-28 17:01:14
