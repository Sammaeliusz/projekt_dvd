-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 07 Lut 2023, 21:33
-- Wersja serwera: 10.4.24-MariaDB
-- Wersja PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `wyp2`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `filmy`
--

CREATE TABLE IF NOT EXISTS `filmy` (
  `id_film` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `tytul` varchar(255) NOT NULL,
  `gatunek` varchar(128) NOT NULL,
  `kat_wiek` int(11) NOT NULL,
  `rezyser` varchar(255) NOT NULL,
  `rok_produkcji` year(4) NOT NULL,
  `dost` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_film`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `uzytkownicy`
--

CREATE TABLE IF NOT EXISTS `uzytkownicy` (
  `id_user` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `nazwa` varchar(128) NOT NULL,
  `email` varchar(255) NOT NULL,
  `haslo` varchar(24) NOT NULL,
  `bilans_kar` int(11) NOT NULL,
  `czy_admin` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `wyporzyczenia`
--

CREATE TABLE IF NOT EXISTS `wyporzyczenia` (
  `id_wyporzyczenie` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_film` int(10) UNSIGNED NOT NULL,
  `id_user` int(10) UNSIGNED NOT NULL,
  `termin_wyporzycz` date NOT NULL,
  `termin_zwrot` date NOT NULL,
  `data_zwrot` date DEFAULT NULL,
  PRIMARY KEY (`id_wyporzyczenie`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
