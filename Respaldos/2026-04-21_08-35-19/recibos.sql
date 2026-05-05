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
-- Table structure for table `recibos`
--

DROP TABLE IF EXISTS `recibos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recibos` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `rc_numero` int(10) NOT NULL DEFAULT 0,
  `rc_fecha` date DEFAULT NULL,
  `rc_codcli` int(5) NOT NULL DEFAULT 0,
  `rc_nomcli` varchar(50) NOT NULL DEFAULT '',
  `rc_importe` decimal(12,2) NOT NULL DEFAULT 0.00,
  `rc_concepto` text NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recibos`
--

LOCK TABLES `recibos` WRITE;
/*!40000 ALTER TABLE `recibos` DISABLE KEYS */;
INSERT INTO `recibos` VALUES (3,3,'2024-10-06',0,'Carot Maria Alejandra',200000.00,'Por compra de PC Celeron segun de detalle en presupuesto. Saldo adeudado pesos 160.000'),(8,4,'2024-10-28',2233,'Luc Patricia',80000.00,'Entrega cuenta por compra de Monitor LED Philips 19\". Saldo adeudado pesos 74.000'),(9,5,'2024-11-07',0,'Lotto Mariela',50000.00,'Entrega a cuenta de compra mas instalacion de disco SSD 240Gb Kingston mas cable HDMI.\nTotal pesos 87.600 - entrega pesos 50.0000 - saldo pesos 37.600'),(10,6,'2024-11-08',0,'Ferreyra Maria Alejandra',160000.00,'Pago saldo pendiente por compra de PC Celeron..'),(11,7,'2025-01-23',0,'Distel Bautista',150000.00,'Entrega sobre copra de procesador Ryzen 5 5600 mas disco Kingaston A400 de 960 G. Saldo pesos 148.000	'),(12,8,'2025-02-12',2774,'Nardi Patricia',318000.00,'Entrega compra pc Celeron segun detalle en presupuesto. Inmporte Total pesos 618.000 menos entrega= saldo adeudado pesos 300.000.- (pesos trescientos mil.)'),(13,9,'2025-02-20',2802,'Biaggi Adrian',390000.00,'Entrega a cuenta compra dos PC Celeron segun presupuesto. Total operacion $ 978.00.- Entrega $ 390.000 mas tres cuoitas de pesos 196.000. - Saldo adeudado pesos 588.000.-'),(14,10,'2025-03-07',0,'amestoy',130000.00,'Pago transferencia primera cuota de dos por compra de Kit PC celeron segun presupuesto mas cuatro cartuchos 133.\nTotal 300.000 \nentrega transferencia pesos -130.000 \ncompra ipresora Samsung Laser -40.000\nSaldo adeudado pesos 130.000 \n'),(15,11,'2025-03-10',2774,'Nardi Patricia',150000.00,'Pago cuota uno de dos compra PC segun presupuesto\nSaldo pendiente pesos 150.000'),(16,12,'2025-04-16',0,'Marcela Heil',14500.00,'Compra teclado Genius KB-118	'),(17,13,'2025-05-30',2787,'Abratte Gabriel',12000.00,'Recibi del Sr. Godoy Hecor la suma de pesos 12.000  Pesos doce mil en concepto de pago por reparacion de PC	'),(18,14,'2025-05-30',0,'Rene Ramos',65000.00,'Pro alquiler de cochera en edificio Miralejos de Villa Carlos Paz calle Sgto Cabral.'),(19,15,'2025-06-18',0,'delfo',30000.00,'Entrega a cuenta por reparacion de PC - Saldo restante pesos 190.000	\n\n\n	'),(20,16,'2025-07-01',0,'Ramos Rene',60000.00,'En concepto alquiler cochera edificio Miralejos med de Julio 2025'),(21,17,'2025-07-04',2465,'Serra Filadelfo',80000.00,'Pago a cuenta de reparacion equipo de computacion	'),(22,18,'2025-07-15',0,'Mato Eduardo',64000.00,'Pago compras de articulos : PEN DRIVE 64GB KINGSTON 3.2 DTXM BLUE y PARLANTE PORTATIL  BLUETOOTH  ROJO  10W RMS RADIOSFM/USB/SD.'),(23,19,'2025-07-22',0,'Serra Filadelfo',50000.00,'en concepto de pago a cuenta '),(24,20,'2025-08-01',0,'Ramos Rene',60000.00,'Alquiler cochera Edificio Miralejos mes de Agosto 2025	'),(25,21,'2025-08-01',2000,'Vasque Silvia',240000.00,'pago entrega cmpra notebook Lenovo V15 G2 Celeron 4500 40% del total'),(26,22,'2025-09-08',0,'Ramos Rene',60000.00,'En concepto de alquiler de cochera edificio Miralejos	7 cochera 98'),(117,23,'2025-12-11',2364,'Cocentino Monica',292500.00,'Entrega a cuenta por compra de PC segun presupuesto. Saldo adeudado pesos 347.500.');
/*!40000 ALTER TABLE `recibos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-21  8:35:21
