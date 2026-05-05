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
-- Table structure for table `guias_tecnicas`
--

DROP TABLE IF EXISTS `guias_tecnicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guias_tecnicas` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `gt_clave` varchar(50) NOT NULL DEFAULT '',
  `gt_brevedesc` varchar(200) NOT NULL DEFAULT '',
  `gt_ruta` varchar(200) NOT NULL DEFAULT '',
  `gt_contenido` text NOT NULL,
  `gt_fotouno` varchar(60) NOT NULL DEFAULT '',
  `gt_fotodos` varchar(60) NOT NULL DEFAULT '',
  `gt_fototres` varchar(60) NOT NULL DEFAULT '',
  `gt_videouno` varchar(100) NOT NULL DEFAULT '',
  `gt_videodos` varchar(100) NOT NULL DEFAULT '',
  `gt_videotres` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guias_tecnicas`
--

LOCK TABLES `guias_tecnicas` WRITE;
/*!40000 ALTER TABLE `guias_tecnicas` DISABLE KEYS */;
INSERT INTO `guias_tecnicas` VALUES (7,'Office','Licencia office 2019 - Activacion','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERALLICENCIA OFFICE 2019','OPCION UNO\n\nmassgrave.dev\nMicrosoft activation Scrip MAS\ncopiar le linea y poner en powershell\n\nseria asi:\n\nMétodo 1: PowerShell (Windows 8 y versiones posteriores) ❤️\nMétodo 2: tradicional (Windows 7 y posteriores)\nAbra PowerShell (no CMD). Para ello, haga clic derecho en el menú de inicio de Windows y seleccione PowerShell o Terminal.\nCopie y pegue el código a continuación y presione enter\n\nirm https://get.activated.win | iex\n\nVerá las opciones de activación. Elija [1] HWID para la activación de Windows. Elija [2] Ohook para la activación de Office.\nEso es todo\n\nva a aparecer una pantalla DOS con opciones (ver video)\n\n# ===========================================================================\nOPCION DOS\n\nABRO CMD COMO ADMINISTRADOR\nEJECUTO ESOS DOS COMANDOS\n\n.............................<PASO 1>............................\n		(INGRESAR A LA RUTA:  Click-to-Run)\n\n	cd \"Program FilesCommon Filesmicrosoft sharedClickToRun\" \n\n.............................<PASO 2>............................\n		(VOLVER A UNA COMPILACION MAS ANTIGUA)	\n	\n	 OfficeC2rclient.exe /update user updatetoversion=16.0.13801.20266\n\n.............................<PASO 3>............................\n		(ABRIR CUALQUIER PROGRAMA DE OFFICE Por Ej. WORD)\n	- Ya no debería aparecer el banner o mensaje de problema de licencia\n	- Deshabilitar/desactivar las actualizaciones.\n\n*****************************\n','','','','act_off_19.mp4','',''),(8,'Windows','cuando instala solo home','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERALsolucion a inst W10 solo pone home','http://www.bios-pw.org/OPCION UNO\n\nmassgrave.dev\nMicrosoft activation Scrip MAS\ncopiar le linea y poner en powershell\n\nseria asi:\n\nMétodo 1: PowerShell (Windows 8 y versiones posteriores) ❤️\nMétodo 2: tradicional (Windows 7 y posteriores)\nAbra PowerShell (no CMD). Para ello, haga clic derecho en el menú de inicio de Windows y seleccione PowerShell o Terminal.\nCopie y pegue el código a continuación y presione enter\n\nirm https://get.activated.win | iex\n\nVerá las opciones de activación. Elija [1] HWID para la activación de Windows. Elija [2] Ohook para la activación de Office.\nEso es todo\n\nva a aparecer una pantalla DOS con opciones (ver video)\n\n# ===========================================================================\nOPCION DOS\n\nABRO CMD COMO ADMINISTRADOR\nEJECUTO ESOS DOS COMANDOS\n\n.............................<PASO 1>............................\n		(INGRESAR A LA RUTA:  Click-to-Run)\n\n	cd \"Program FilesCommon Filesmicrosoft sharedClickToRun\" \n\n.............................<PASO 2>............................\n		(VOLVER A UNA COMPILACION MAS ANTIGUA)	\n	\n	 OfficeC2rclient.exe /update user updatetoversion=16.0.13801.20266\n\n.............................<PASO 3>............................\n		(ABRIR CUALQUIER PROGRAMA DE OFFICE Por Ej. WORD)\n	- Ya no debería aparecer el banner o mensaje de problema de licencia\n	- Deshabilitar/desactivar las actualizaciones.\n\n*****************************\n','dos.jpg','','','w10_inst_home.mp4','',''),(9,'Windows','Windows no reconoce nuestros discos - IRST en la carpeta','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL\reconocimiento discos win10','','','','','w10_noreconoce_disco.mp4','',''),(10,'Acer BIOS','Quitar contraseña a Acer E5  Acer E1 y demas Acer  Quitar password de Acer E5','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERALcontraseña de fabrica BIOS ACER','http://www.bios-pw.org/','','','','quitar_pass_acer.mp4','',''),(11,'Baterias Notebooks','Test baterias notebooks','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERALbaterias notebooks','','test_baterias.png','1_acad.png','img.JPG','','','problemas_baterias.docx'),(12,'Wifi','El wifi entra en modo avion','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','','','','','wifi_avion.mp4','',''),(13,'rufus USB boot','Crear una USB Booteable MIXTA UefiBios con RUFUS','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','','','','','Crear_USB_RUFUS.mp4','',''),(14,'Windows','Windows update en windows 7 cuando falla','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','borrar la carpeta c:windowssoftaware distribution\n','','','','','',''),(15,'Office','para office 2016 - quitar la pantalla de licencia aunque diga producto activado','','HKEY_LOCAL_MACHINESOFTWAREWow6432NodeMicrosoft Office16.0CommonOEM\nHKEY_LOCAL_MACHINESOFTWAREMicrosoftOffice16.0 CommonOEM','','','','','',''),(16,'Defender','Formas para actualizar defender','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','OTRA MANERA DE HACERLO, POR AHI MAS FACIL Y MENOS MOLESTA..\n\n1- Ubica el archivo \"C:Program FilesWindows DefenderMpCmdRun.exe\" igual que el apartado anterior.\n2- Hacele un acceso directo a ese archivo, haciendo click con el boton secundario del mouse -> enviar a -> escritorio.\n3- Anda al escritorio, ubicas el acceso directo, ponele algun nombre como \"Actualizador Defender\" o algo asi.\n4- hace click con el boton secundario en el acceso directo -> propiedades.\n\nDond dice \"DESTINO: \" agregar al final \" -signatureupdate\"   te tiene que quedar asi:\n\n\"C:Program FilesWindows DefenderMpCmdRun.exe\" -signatureupdate\n\nDonde dice \"Ejecutar: \" pone minimizado (esto hace que se inicie minimizado y no moleste).\n\n5- Ahora copia ese archivito acceso directo que hicimos.. hace click en el menu inicio -> todos los programas -> inicio, en esa carpeta hace click con el boton secundario, abrir. Se te abre una carpeta.. y pega ahi el acceso directo. Esto hace que se ejecute el \"Actualizad Defender\" al prender la PC.\n\n','','','','','',''),(17,'Windows','Moodo seguro formas de entrar en  windows 10','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','','','','','','','modo_seguro_w10.pdf'),(18,'Defender','defender_directiva de grupo.png','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','','','','','','','defender_directiva_degrupo.png'),(19,'Thuderbolt','thuderbolt 3 vs usb-c.JPG','C:UsersDopDesktopSOLUCIONES TECNICAS USO TALLERTRUCOS TECNICOS EN GENERAL','','','','','','','thuderbolt3vsusbc.JPG'),(20,'Python','Video de Hotel management 1/6','C:Proyectos_PythonABM_Clientes	ecnica','','','','','1_6hotel.mp4','',''),(21,'Python','Video de hotel management 2/6','C:Proyectos_PythonABM_Clientes	ecnica','','','','','2_6hotel.mp4','',''),(22,'SQL','copiar estructura de una tabla a otra','','CREATE TABLE nueva LIKE desde_cual','','','','','',''),(23,'Ventoy','CREAR USB Multiboot BIOS Y UEFI Con VENTOY Todo En Un Solo USB','C:Proyectos_PythonABM_Clientes	ecnica','','','','','ventoy.mp4','',''),(26,'windows 11 24h2','Instalar windows 11 24h2 sin perder datos','C:Proyectos_PythonABM_Clientes\\_internal	ecnicawin11_24H2_sin_perde_datos_2.mp4','','','','','win11_24h2_sin_perde_datos.mp4','win11_24H2_sin_perde_datos_2.mp4',''),(27,'WIndows','Saber que version de windows es la que est instalada','C:Proyectos_PythonABM_Clientes\\_internal	ecnica','','version_windows.png','','','','',''),(28,'Onedrive','Desvincular equipo de onedrive y restablecer las carpetas a su lugar natural','C:Proyectos_PythonABM_Clientes\\_internal	ecnicadesvincular_onedrive.mp4','','','','','desvincular_onedrive.mp4','',''),(29,'Windows 11 24h2','Instalar windows 11 de cero sin que pida inicio de sesion','','','','','','inst_W11_saltar_inicio_sesion.mp4','',''),(30,'Windows modo S','Como desaactivar modo S en windows desde el BIOS','','','','','','','','Como_desactivar_modo_S_de_Windows_11_sin_cta.pdf'),(31,'Windows modo S','Salir de<l modo S en windows desde el Bios','','','','','','C:/Proyectos_Python/ABM_Clientes/tecnica/Salir_del_modo_S_desde_la_BIOS.mp4','','');
/*!40000 ALTER TABLE `guias_tecnicas` ENABLE KEYS */;
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
