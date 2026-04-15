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
-- Table structure for table `inf_tecnicos`
--

DROP TABLE IF EXISTS `inf_tecnicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inf_tecnicos` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `it_fecha` date DEFAULT NULL,
  `it_usuario` varchar(50) NOT NULL DEFAULT '',
  `it_dni` varchar(50) NOT NULL DEFAULT '',
  `it_numdoc` varchar(15) NOT NULL DEFAULT '',
  `it_equipo` varchar(100) NOT NULL DEFAULT '',
  `it_modelo` varchar(100) NOT NULL DEFAULT '',
  `it_serie` varchar(30) NOT NULL DEFAULT '',
  `it_diagnostico` varchar(250) NOT NULL DEFAULT '',
  `it_provocado` varchar(250) NOT NULL DEFAULT '',
  `it_informe` text NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inf_tecnicos`
--

LOCK TABLES `inf_tecnicos` WRITE;
/*!40000 ALTER TABLE `inf_tecnicos` DISABLE KEYS */;
INSERT INTO `inf_tecnicos` VALUES (5,'2025-08-28','Salvatierra Jeronimo','DNI-Documento Nacional de Identidad','13272067','Notebook','Pavilion 270','AA25663-5558PL','no enciende-no da imagen-daño placa principal','descarga electrica, tormenta','De acuerdo a lo solicitado por el señor/a Salvatierra Jeronimo DNI-Documento Nacional de Identidad - Nº: 13272067, se extiende el presente informe tècnico sobre la revisiòn del siguiente equipo: Notebook HP Modelo Pavilion 270 Nº de serieAA25663-5558PL Una vez revisado/a, se constata que el mismo presenta las siguientes fallas: no enciende-no da imagen-daño placa principal. Se estima que los daños fueron provocados por descarga electrica, tormenta. Se extiende este informe para ser presentado ante quien corresponda.'),(11,'2026-03-27','Veronica Dellasiega','DNI-Documento Nacional de Identidad','22333555','Monitor Samsung','56565','56565','dañado electrico','electricidad','De acuerdo a lo solicitado por el señor/a Veronica Dellasiega DNI-Documento Nacional de Identidad - Nº: 22333555, se extiende el presente informe tècnico sobre la revisiòn del siguiente equipo: Monitor Samsung Modelo 56565 Nº de serie56565 Una vez revisado/a, se constata que el mismo presenta las siguientes fallas: dañado electrico. Se estima que los daños fueron provocados por electricidad. Se extiende este informe para ser presentado ante quien corresponda.'),(12,'2026-04-13','Veronica Dellasiega','DNI-Documento Nacional de Identidad','27225658','Disco Duro SATA 1Tb Seagate','Seagate SATA Barracuda 1 Tb ST1000DM003','s1deas89','Daño mecanico de funcionamiento','Descarga electrica','De acuerdo a lo solicitado por el señor/a Veronica Dellasiega DNI-Documento Nacional de Identidad - Nº: 27225658, se extiende el presente informe tècnico sobre la revisiòn del siguiente equipo: Disco Duro SATA 1Tb Seagate Modelo Seagate SATA Barracuda 1 Tb ST1000DM003 Nº de serie s1deas89 Una vez revisado/a, se constata que el mismo presenta las siguientes fallas: Daño mecanico de funcionamiento. Se estima que los daños fueron provocados por Descarga electrica. Se extiende este informe para ser presentado ante quien corresponda.');
/*!40000 ALTER TABLE `inf_tecnicos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 23:39:22
