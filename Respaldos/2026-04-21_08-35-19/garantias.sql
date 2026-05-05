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
-- Table structure for table `garantias`
--

DROP TABLE IF EXISTS `garantias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `garantias` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `gt_fechaventa` date DEFAULT NULL,
  `gt_meses` int(2) NOT NULL DEFAULT 0,
  `gt_fechavto` date DEFAULT NULL,
  `gt_codcli` decimal(5,0) NOT NULL DEFAULT 0,
  `gt_nomcli` varchar(70) NOT NULL DEFAULT '',
  `gt_articulo` varchar(200) NOT NULL DEFAULT '',
  `gt_impventa` decimal(10,2) NOT NULL DEFAULT 0.00,
  `gt_factura` varchar(20) NOT NULL DEFAULT '',
  `gt_observaciones` varchar(150) NOT NULL DEFAULT '',
  `gt_detalle` text NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garantias`
--

LOCK TABLES `garantias` WRITE;
/*!40000 ALTER TABLE `garantias` DISABLE KEYS */;
INSERT INTO `garantias` VALUES (6,'2024-08-03',12,'2025-08-03',1998,'Pesci Fernando','PC Celeron 8GB RAM-SSD 250 m.2 Gallara-Gab 609-disco 500GB usado',380000.00,'','con migracion de equipo anterior',''),(8,'2024-09-11',12,'2025-09-11',494,'Osiecki Nidia','MONITOR 19 PHILIPS VGA HDMI VESA',159000.00,'','en dos veces entrgo 80.000 y quedan pesos 79.000',''),(9,'2024-10-04',12,'2025-10-04',315,'Carot Maria Alejandra','PC Celeron 8 Gb SSD 240Gb-Gab.con fuente-PB MSI',360000.00,'','',''),(10,'2024-10-09',12,'2025-10-09',14,'Senni Marcelo','Ryzen5 32 gb gabinete y fuente - placa base ver planilla',966000.00,'','ver detalle en planillas',''),(11,'2024-10-09',12,'2025-10-09',14,'Senni Marcelo','placa video',1360000.00,'','ver detalle en planilla',''),(12,'2024-10-16',12,'2025-10-16',1233,'Pons Adrian','CPU INTEL CELERON G5905 3.50GHZ S1200\n-MOTHER MSI PRO H510M-B H/V M.2 1200 (10ma GEN)-\nDDR4 8GB KINGSTON 3200MHZ CL16 FURY BEAST BLACK-\nDISCO SSD 240',310000.00,'000','se armo en su gabinete con windows 10 mas backup',''),(15,'2024-10-28',12,'2025-10-28',2233,'Luc Patricia','MONITOR 19 PHILIPS VGA HDMI VESA',154000.00,'','en dos pagos - entrega 80.000 y a 30 dias 74.000',''),(16,'2024-12-28',12,'2025-12-28',2390,'Picabea Santiago','Kit Actualizacion SEGUN PRESUPUESTO PB Gigabyte -  RYZEN 7  - 32 ram - SSD 500Gb NV2 -vent 120x120 led',1200000.00,'','total de operacion ver presupuesto y canjes por usados',''),(18,'2025-01-25',6,'2025-07-25',2666,'Chavez Facundo','bateria para notebook Dell - comprada en Divnet pesos 59.500',82000.00,'','',''),(19,'2025-01-30',12,'2026-01-30',1423,'Penella Alejandro','Placa base Gigabyte - Celeron G5905 - 2 bancos de 8Gb Kingston Fury DDR4 - Disco SSD KC600 512Gb ',398000.00,'348','',''),(20,'2025-01-30',12,'2026-01-30',1423,'Penella Alejandro','Impresora Laser Brother 1212W',265000.00,'349','',''),(21,'2025-01-23',12,'2026-01-23',0,'Distel Bautista','RYZEN 5 5600',200000.00,'','',''),(22,'2025-01-23',12,'2026-01-23',0,'Distel Bautista','DISCO SSD 1TB NV2 SNVS SERIE-PCIe NVME M.2 KINGSTON',98000.00,'','',''),(23,'2025-02-06',3,'2025-05-06',1350,'Laclau Miguel','PC I3 4Gb RAM SSD 120Gb mas Disco mecanico de 500Gb con windows 10',180000.00,'','',''),(25,'2025-02-11',12,'2026-02-11',2774,'Nardi Patricia','Pc Celeron G5905 - PBase H510M - SSD 250  NV2 M.2 - 8Gb 3200 kingston - gab C102 Gigabyte - fuente gamemax 80 - philips 19\" - combo mouse teclado',618000.00,'','le puse el disco de la notebook SSD de 240Gb como adicioonal',''),(26,'2025-02-18',12,'2026-02-18',2489,'Olivier Mateo','Kit segun presupuesto mas fuente gamemax',598000.00,'','se le agrego despues fuente al presupuesto inicial',''),(27,'2025-02-20',12,'2026-02-20',2802,'Biaggi Adrian','Pc Celeron 8Gb RAM ssd nv2 500 - ver presupuesto',489000.00,'','',''),(28,'2025-02-24',12,'2026-02-24',2802,'Biaggi Adrian','Pc Celeron segun presupuesto',489000.00,'','40% entrega y 3 cuotas de 196.000',''),(29,'2025-03-07',12,'2026-03-07',1032,'Amestoy Crristina','Kit Celeron G5905 - 8Gb RAM DDR 4 - Placa base MSI PRO H510M',290000.00,'','se uso su gabinete y fuente - ','Se cambio la placa base el dia 6-10-25 por daño. La placa no encendia electricamente. Placa MSI H510M de Eikon. Le puse una que tenia en stock igualita de Airoldi. Lleve la otra a Eikon para cambio.'),(30,'2025-05-30',12,'2026-05-30',2834,'Ladu mama Jael Mariela','notebook Lenovo Core I5 - 8 Gb RAM -SSDnvme 500Gb. 15\" - segun presupuesto',960000.00,'','pago contado',''),(31,'2025-06-04',12,'2026-06-04',1863,'Pinat Daniel  nueva cuenta','Pc servidora segun presupuesto',1128000.00,'','',''),(32,'2025-06-16',12,'2026-06-16',2489,'Olivier Mateo','Placa de video MSI RTX 3050 geforce',330000.00,'','',''),(33,'2025-06-16',12,'2026-06-16',2489,'Olivier Mateo','DDR4 8 GB 3200MHZ FURY BEAST BLK .',87000.00,'','',''),(34,'2025-08-01',12,'2026-08-01',2000,'Vasque Silvia','Notebook Lenovo V15 G2 detalle en presupuesto',620000.00,'','me dejo una usada lenovo core i3 para vender',''),(35,'2025-08-28',12,'2026-08-28',1933,'Kamar Gustavo','CPU AMD RYZEN 5 5600GT AM4 65W WRAITH STEALTH COOL',270000.00,'','',''),(37,'2025-09-01',12,'2026-09-01',721,'Dellasiega Veronica','PC Ryzen 3 segun presupuesto',708000.00,'','-',''),(46,'2025-09-03',12,'2026-09-03',2391,'Scida Leonardo','SSD M.2 NVME 500GB G4 KINGSTON NV3',115.00,'','',''),(59,'2025-10-31',12,'2026-10-31',2874,'Caimi Ivan','segun presupuesto mas conversor displayport a vga',500000.00,'','se hizo factura A','montado en gabinete de el con disco de el un SSD PNY mas dos discos toshiba mecanicos.'),(63,'2025-11-20',3,'2026-02-20',2407,'Aviles Jose','Reparacion notebook Lenovo en Divnet mas cambio de bateria',220000.00,'','se paga en dos veces',''),(64,'2025-11-27',12,'2026-11-27',1933,'Kamar Gustavo','monitor lenovo 24\"',290000.00,'','cambio delprimer lenovo de 19',''),(65,'2025-11-27',12,'2026-11-27',101,'Gonzalez Tati','MONITOR 19 LENOVO D19-10 VGA/HDMI     ',190000.00,'','le dije que tenia tres dias de uso y se lo vendi a un precio bajo en dos pagos',''),(66,'2025-12-11',12,'2026-12-11',2364,'Cocentino Monica','Pc celeron segun presupuesto',640000.00,'','',''),(67,'2025-12-30',12,'2026-12-30',1168,'Funes Carlos Osvaldo','notebook lenovo segun detalle',250000.00,'','fue a cambio de la que rompi - total 480.000 el pago 250.000',''),(68,'2026-01-12',3,'2026-04-12',2894,'Almanza Gustavo','Kit usado pentiun 3020 micro y placa solamente mas placa wifi tp-link',120000.00,'','','le deje mi gabinete cn la fuente para no tener que desarmar tanto'),(70,'2026-01-16',3,'2026-04-16',2888,'Blengini Ricardo','SSD 240Gb usado',85000.00,'','',''),(71,'2026-01-19',12,'2027-01-19',2307,'Zechin Andres','MONITOR 19 PHILIPS VGA HDMI VESA',195000.00,'','',''),(72,'2026-01-27',12,'2027-01-27',2845,'Crivello Guillermo','MONITOR 22 MSI PRO MP225V FHD 100HZ HDMI VGA',198000.00,'','pago efectivo',''),(73,'2026-01-27',3,'2026-04-27',1998,'Pesci Fernando','reparacion notebook Lenovo thinkpad',178000.00,'','',''),(74,'2026-02-02',12,'2027-02-02',2902,'Gil Cecilia','Pc intel core I3 segun presupuesto',880000.00,'','','Con Factura A'),(75,'2026-02-20',12,'2027-02-20',373,'Pinat Patricia','IMPRESORA LASER BROTHER HL-1212W WIFI         ',280000.00,'','',''),(76,'2026-03-05',1,'2026-04-05',0,'Steiner Roberto','Notebook Lenovo de Silvia',200000.00,'','',''),(77,'2026-03-26',12,'2027-03-26',721,'Dellasiega Veronica','monitor HP 324pv 24 pulgadas',250000.00,'466','informe tecnico',''),(78,'2026-04-20',12,'2027-04-20',180,'Moeremans Marcelo','notebook lenovo ryzen 7 segun presupuesto',1990000.00,'','Es para el colegio de arquitectos Carlos Paz','');
/*!40000 ALTER TABLE `garantias` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21  8:35:20
