-- MySQL dump 10.13  Distrib 8.0.32, for Linux (aarch64)
--
-- Host: localhost    Database: wypozyczalnia
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

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
-- Table structure for table `filmy`
--

DROP TABLE IF EXISTS `filmy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filmy` (
  `id_film` int unsigned NOT NULL AUTO_INCREMENT,
  `tytul` varchar(255) NOT NULL,
  `gatunek` varchar(128) NOT NULL,
  `kat_wiek` int NOT NULL,
  `rezyser` varchar(255) NOT NULL,
  `rok_produkcji` year NOT NULL,
  `dost` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_film`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filmy`
--

LOCK TABLES `filmy` WRITE;
/*!40000 ALTER TABLE `filmy` DISABLE KEYS */;
INSERT INTO `filmy` VALUES (1,'Serce Gór','Dramat, Obyczajowy',0,'Kasia Adamik',2019,1),(2,'Serce Gór','Dramat, Obyczajowy',0,'Kasia Adamik',2019,1),(3,'Serce Gór','Dramat, Obyczajowy',0,'Kasia Adamik',2019,1),(4,'Serce Gór','Dramat, Obyczajowy',0,'Kasia Adamik',2019,1),(5,'Serce Gór','Dramat, Obyczajowy',0,'Kasia Adamik',2019,1),(6,'Avatar Istota Wody','Sci-Fi',13,'James Cameron',2022,1),(7,'Black Panther 2018','Akcja, Sci-Fi',13,' Ryan Coogler',2018,1),(8,'Kung Fury','Parodia, Akcja, Sci-Fi, Komedia',18,'David Sandberg',2015,1),(9,'Finding Jesus','Animacja, Rodzinny, Fantasy',0,'Jason Wright',2020,1);
/*!40000 ALTER TABLE `filmy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uzytkownicy`
--

DROP TABLE IF EXISTS `uzytkownicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uzytkownicy` (
  `id_user` int unsigned NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(128) NOT NULL,
  `email` varchar(255) NOT NULL,
  `haslo` varchar(24) NOT NULL,
  `bilans_kar` int DEFAULT NULL,
  `czy_admin` tinyint(1) DEFAULT NULL,
  `status` tinyint NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uzytkownicy`
--

LOCK TABLES `uzytkownicy` WRITE;
/*!40000 ALTER TABLE `uzytkownicy` DISABLE KEYS */;
INSERT INTO `uzytkownicy` VALUES (1,'admin','admin@ppp.com','XSW@3edc',NULL,1,0),(3,'test1','test1@test.pl','Test1234;',NULL,NULL,0),(4,'Lunar','pozdrowionka@od.lunar','hi25',NULL,NULL,0),(5,'test2','test2@test.pl','ZAQ!2wsx',NULL,NULL,0),(6,'puszkapiwazubr','puszkapiwa@gmail.com','puszkapiwazubr',NULL,NULL,0),(7,'Cebula','cebula@c.com','zxc',NULL,NULL,0),(8,'Papryka','chuj@chuj.com','chuj',NULL,NULL,0);
/*!40000 ALTER TABLE `uzytkownicy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wypozyczenia`
--

DROP TABLE IF EXISTS `wypozyczenia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wypozyczenia` (
  `id_rent` int unsigned NOT NULL AUTO_INCREMENT,
  `id_film` int unsigned NOT NULL,
  `id_user` int unsigned NOT NULL,
  `termin_rent` date NOT NULL,
  `termin_zwrot` date NOT NULL,
  `data_zwrot` date DEFAULT NULL,
  PRIMARY KEY (`id_rent`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wypozyczenia`
--

LOCK TABLES `wypozyczenia` WRITE;
/*!40000 ALTER TABLE `wypozyczenia` DISABLE KEYS */;
INSERT INTO `wypozyczenia` VALUES (1,4,3,'2023-01-01','2023-01-15',NULL),(2,6,3,'2023-01-01','2023-01-15','2023-01-14'),(3,8,3,'2023-03-01','2023-03-15',NULL),(4,5,5,'2023-01-01','2023-01-15','2023-01-13'),(5,9,5,'2023-02-01','2023-02-15','2023-02-13'),(6,1,5,'2023-03-01','2023-03-15',NULL),(7,7,5,'2023-03-01','2023-03-15',NULL);
/*!40000 ALTER TABLE `wypozyczenia` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-16 17:34:26
