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
-- Table structure for table `rma`
--

DROP TABLE IF EXISTS `rma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rma` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `rm_fecha` date DEFAULT NULL,
  `rm_articulo` varchar(150) NOT NULL DEFAULT '',
  `rm_proceso` varchar(20) NOT NULL DEFAULT '',
  `rm_estado` varchar(40) NOT NULL DEFAULT '',
  `rm_proveedor` varchar(50) NOT NULL DEFAULT '',
  `rm_cliente` varchar(80) NOT NULL DEFAULT '',
  `rm_falla_motivo` varchar(200) NOT NULL DEFAULT '',
  `rm_costo_venta` varchar(200) NOT NULL DEFAULT '',
  `rm_observaciones` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rma`
--

LOCK TABLES `rma` WRITE;
/*!40000 ALTER TABLE `rma` DISABLE KEYS */;
INSERT INTO `rma` VALUES (1,'2024-10-29','Toner 1060 Coprint','RMA','Cambio','Trade','','','',''),(5,'2024-12-05','Notebook Lenovo - Fernanda Salas ','Reparacion','Finalizado','Divnet - servicio tecnico','','No enciende ','','La deje sin bateria y sin fuente - el disco lo deje puesto - reparada en Divnet pesos 89.000 - cliente 120.000'),(6,'2024-12-05','Notebook Exo - Patricia Nardi','Reparacion','Devolucion','Divnet','','','','deje sin cargador y  con disco duro -- Devolucion sin reparacion - posible problema de flez no conseguido'),(7,'2025-01-08','Toner office 1060 2000 hojas','RMA','Devolucion','Eikon','','Ruido','',''),(8,'2025-01-15','Mini PC core I5 Cx - con embalaje original','RMA','Cambio','Airoldi','','','',''),(9,'2025-01-18','Notebook Lenovo - Lopez Maria Ines','Reparacion','Devolucion','Divnet','','No enciende - en corto - presupuesto entre 110.000 y 135.000','','Me avisaron de divnet que esta el procesador en corto y no tiene reparacion'),(12,'2025-01-23','Cable USB impresora nisuta 3 metros','Prestamo','Finalizado','','Rodo','para probar','','llevo Cludio'),(13,'2025-02-12','cable usado monitor VGA','Prestamo','Finalizado','','Abratte Gabriel','para probar','','nunca me deovlvio el cable'),(14,'2025-02-28','antena tplink bluethoot','RMA','Finalizado','','sra libreria','','','La compro y me pago por transferencia'),(15,'2025-02-15','notebook en reparacion','Reparacion','Devolucion','divnet','Dominguez Sergio','No enciende , no tiene onsumo','110.000 y 135.000','no se pudo reparar'),(16,'2025-05-23','Notebook Asus','Reparacion','Finalizado','Divnet','Casado  Claudia','No encinde','150.000','reparada'),(17,'2025-04-03','Notebook HP','Reparacion','Devolucion','Divnet','Zabala Cecilia','Placa mojada no enciende','de 120.000 a 150.000','no se pude reparar'),(18,'2025-05-23','Placa base Asus','RMA','Finalizado','Air','Senni Marcelo','no enciende','',''),(19,'2025-08-25','placa base y procesador Rizen 9','RMA','Finalizado','Airoldi','Senni Marcelo','no da imagen el conjunto','','me fallaban porque no actgualizaba el BIOS'),(20,'2025-08-25','Notebook Sony Vaio','Reparacion','Finalizado','Divnet','Pinat Daniel','Flex','','Era la pantalla, se cambio la pantalla'),(22,'2026-04-16','memoria DDR$ de 4Gb','Prestamo','Pendiente','','Viviana mama de Luca Lanzeni','a prueba por falla rara','45.000 le pase en caso de andar bien',''),(23,'2026-04-16','ventilador 80x80 netmak en reemplazo de una turboina que ya no refrigera el micro','Prestamo','Pendiente','','Vila Daniel','se apagaba','45.00 le pase si andaba todo bien',''),(24,'2026-04-16','Disco SSD WD Green de 240Gb','Prestamo','Pendiente','','Nievas Oscar','por falla rara que sospechamos del disco que tenia el','vemos segun que haya que hacer a futuro',''),(25,'2026-04-17','Notebook HP sin cargador y sin funda','Reparacion','Pendiente','Divnet Tecnica','Molina Violeta','le ingreso ñliquidpo en el interior y no enciende','presupueste aproximado en 190.000','deje en divnet el 16-4 - presup. aeptado 18-4 wathsapp en pesos 190.000 con costo 95.000 mas 35.000'),(26,'2026-04-17','Notebook Lenovo','Reparacion','Pendiente','Divnet tecnica','Marchelli Maria del Carmen','Falla de imagen al mover la tapa (flex o pantalla)','no pase presupuesto porque no se la falla','lleve a divnet el 16-4'),(27,'2026-04-17','Notebook HP','Reparacion','Pendiente','Divnet Tecnica','Henry Tulian','no enciende le entro agua','190.000 aproximado','');
/*!40000 ALTER TABLE `rma` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21 22:31:22
