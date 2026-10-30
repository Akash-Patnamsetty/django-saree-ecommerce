-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: gnapika_store
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(50) DEFAULT NULL,
  `address` text,
  `is_default` tinyint(1) DEFAULT '0',
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,16,'Home','H.No 4-12, Main Road, Guntur, Andhra Pradesh 522001',1,'9876543210'),(2,17,'Office','Plot No. 45, Tech Park, Hi-Tech City, Hyderabad 500081',1,'8765432109'),(3,18,'Work','Flat 202, Sunshine Apartments, Vijayawada 520010',1,'7654321098'),(4,19,'Home','Door No 10-5, Jubilee Hills, Hyderabad 500033',1,'9988776655'),(5,20,'College','Girls Hostel Block A, JNTUK Campus, Kakinada 533003',1,'8877665544'),(6,16,'Secondary','123 New Street, Guntur',0,'9123456789'),(7,17,'Home','Flat 402, Sai Residency, Ameerpet, Hyderabad 500038',0,'9848012345'),(8,18,'Home','D.No 5-88, Arundelpet 3rd Line, Guntur 522002',0,'9908054321'),(9,19,'Work','Mindspace IT Park, Building 12, Madhapur, Hyderabad 500081',0,'7702211223'),(10,20,'Home','H.No 12/A, Near Clock Tower, Anantapur 515001',0,'9440055667'),(11,16,'Office','IT Park, Phase 2, Mangalagiri, Andhra Pradesh 522503',0,'9123456780'),(12,16,'Warehouse','Plot 88, Industrial Estate, Guntur 522005',0,'9123456781'),(13,17,'Parents Home','Door No 5-1, Main Bazaar, Vijayawada 520001',0,'8765400001'),(14,17,'Gym Address','FitLife Center, Banjara Hills, Hyderabad 500034',0,'8765400002'),(15,18,'Studio','Room 204, Creative Block, Film City, Hyderabad 500096',0,'7654300003'),(16,18,'Secondary Office','Sigma Tech Park, Whitefield, Bengaluru 560066',0,'7654300004'),(17,19,'Farmhouse','Survey No. 112, Chevella Road, Vikarabad 501101',0,'9988700005'),(18,19,'Sister Residence','H.No 9-44, Lalapet, Secunderabad 500017',0,'9988700006'),(19,20,'Internship Office','T-Hub 2.0, Madhapur, Hyderabad 500081',0,'8877600007'),(20,20,'Permanent Address','15/342, Nehru Road, Kurnool, Andhra Pradesh 518001',0,'8877600008'),(21,21,'Akash Patnamsetty','Gunter',0,'09000920161'),(22,29,'a','v',0,'1'),(23,31,'Akash Patnamsetty','Gunter',0,'9000920161'),(24,22,'Akash Patnamsetty','Gunter',0,'09000920161'),(25,32,'Akash Patnamsetty','Gunter',0,'09000920161'),(26,23,'sarath chandra','7-142/1  yadlapalli',0,'07386568606'),(27,33,'Koushik','Guntur, reddy hostel',0,'9124528566'),(28,30,'Dinesh Nagandla','5-640/4 kummara colony 1st floor ',0,'7032970626');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$ztoqNEj0hO4BZfj5VXiKwX$u6YXUY5NR5uZkoNBlY0GZywaoIeAo4H8Uq1GNWgWYJc=','2026-04-10 17:25:44.718375',1,'admin','','','',1,1,'2026-04-04 02:41:46.154250');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT '1',
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_id`),
  UNIQUE KEY `unique_cart` (`user_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (39,33,22,1,'2026-04-12 08:32:40');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `category_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (21,'VYKUNTAPURAM ','2026-04-11 01:21:28','category_images/WhatsApp Image 2026-04-11 at 10.15.15 AM.jpeg'),(22,'Traditinal colour combination','2026-04-11 01:26:18','category_images/WhatsApp Image 2026-04-11 at 10.14.00 AM (2).jpeg'),(23,'silk sarees','2026-04-11 09:07:24','category_images/WhatsApp Image 2026-04-10 at 10.29.05 PM (2).jpeg'),(24,'mysore silk ','2026-04-11 09:15:30','category_images/WhatsApp Image 2026-04-10 at 10.29.06 PM (2).jpeg');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-04-04 02:47:08.234622','2','Product object (2)',1,'[{\"added\": {}}]',7,1),(2,'2026-04-10 17:27:48.839013','4','Product object (4)',1,'[{\"added\": {}}]',7,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(8,'store','category'),(7,'store','product'),(9,'store','productimage');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-28 03:04:16.169552'),(2,'auth','0001_initial','2026-03-28 03:04:16.861898'),(3,'admin','0001_initial','2026-03-28 03:04:17.014298'),(4,'admin','0002_logentry_remove_auto_add','2026-03-28 03:04:17.022248'),(5,'admin','0003_logentry_add_action_flag_choices','2026-03-28 03:04:17.030126'),(6,'contenttypes','0002_remove_content_type_name','2026-03-28 03:04:17.145783'),(7,'auth','0002_alter_permission_name_max_length','2026-03-28 03:04:17.255440'),(8,'auth','0003_alter_user_email_max_length','2026-03-28 03:04:17.295561'),(9,'auth','0004_alter_user_username_opts','2026-03-28 03:04:17.304459'),(10,'auth','0005_alter_user_last_login_null','2026-03-28 03:04:17.374285'),(11,'auth','0006_require_contenttypes_0002','2026-03-28 03:04:17.377706'),(12,'auth','0007_alter_validators_add_error_messages','2026-03-28 03:04:17.388151'),(13,'auth','0008_alter_user_username_max_length','2026-03-28 03:04:17.465951'),(14,'auth','0009_alter_user_last_name_max_length','2026-03-28 03:04:17.540681'),(15,'auth','0010_alter_group_name_max_length','2026-03-28 03:04:17.567166'),(16,'auth','0011_update_proxy_permissions','2026-03-28 03:04:17.575541'),(17,'auth','0012_alter_user_first_name_max_length','2026-03-28 03:04:17.646781'),(18,'sessions','0001_initial','2026-03-28 03:04:17.693153'),(19,'store','0001_initial','2026-03-30 15:12:46.461248');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2ocxu9zsve6sdfld9vw03tcp21lcj0ql','eyJ1c2VyX2lkIjoxMCwidXNlcl9uYW1lIjoiQmFuaSJ9:1w7Gy8:VGhW2pJ9a-zqsLp2Xm63Klquo7hKWgFRb-43vhYDy0Q','2026-04-13 18:04:08.261703'),('79dptfcx5jcylmkhhw3fh229a6xic758','eyJ1c2VyX2lkIjoxNiwidXNlcl9uYW1lIjoiQWthc2gifQ:1w7TMT:_PEFNRQyo-wEuGWdTRXajjvh9lueIoysUqH2-4nLaHA','2026-04-14 07:18:05.867619'),('a2kyvi1kd3gdp83ue7p52xi30h8njqtz','eyJ1c2VyX2lkIjozMCwidXNlcl9uYW1lIjoiRGluZXNoIE5hZ2FuZGxhIn0:1w9RAA:lM3Y6l1EYsF5nASIRTRmRxZSGv-r3v9R3Y38vtcw9xk','2026-04-19 17:21:30.954301'),('a4vapizbm0fdgcugc88unj5h1t7jzhqj','.eJxVjcEOgjAQRH_F7Jk0QClruendxD8g23YriJaEloMx_rsQiQnHmXkz84Y58tT2DhpZZj8R6MnQwGmg2B2ulBYdOaUXZNDSnLr2X4Fi7xmyA4c1cHcKt1HYMaSpN2JFxJZGcRkdP84buxvolsulbbQyNavKsya0rkR7tFyqovZVrnWJ7CWiJOMIK2eQ88JLZVBLb2stlYPPF47DR5o:1wBFc0:efZonIKu-WwG7v8EHPaoO5QOaHtbvhSyl5jHq2MFBTs','2026-04-24 17:25:44.727322'),('x5yrey3oax5v691165w968bub2tgq3yi','eyJ1c2VyX2lkIjozMywidXNlcl9uYW1lIjoiS2luZyJ9:1wB7XC:bc8xYQFOz5SPcK3zmplZYURrG8-ZLpJees6BPrOGUrw','2026-04-24 08:48:14.047140'),('xhrhbvwzs6zjrrxgv7efbcimeuvq83e4','eyJ1c2VyX2lkIjoyMiwidXNlcl9uYW1lIjoiQW5qaSJ9:1w9MUC:fpGkw7sPG-iew3K-QM7COZ9GCzJDEQJwccFU1bWsKRQ','2026-04-19 12:21:52.308057'),('xk6wwvm1935rc86mxwy7ipuzsxjw522c','eyJ1c2VyX2lkIjoyMywidXNlcl9uYW1lIjoiU2FyYXRoIGNoYW5kcmEifQ:1w9OOA:FkkfH2_c7cFBGcpYzY6gIQkj-H_iXCKTgf_NvGD2B0Q','2026-04-19 14:23:46.385058'),('y4wms7md7eg2wnuchn4s5sp67c4jk5n4','eyJ1c2VyX2lkIjoxMCwidXNlcl9uYW1lIjoiQmFuaSJ9:1w7Gy8:VGhW2pJ9a-zqsLp2Xm63Klquo7hKWgFRb-43vhYDy0Q','2026-04-13 18:04:08.317067'),('yn0jn2xsu3t3yupga7xpovwl7dw7hbdu','eyJ1c2VyX2lkIjoyMSwidXNlcl9uYW1lIjoiYWtraSJ9:1w9JxO:h-vmXwqNPvoTI9WQfefU-Bo8YaNSIke1Jo0O-EGA_O8','2026-04-19 09:39:50.053643');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `likes` (
  `like_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `product_id` int NOT NULL,
  `liked_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`like_id`),
  UNIQUE KEY `unique_like` (`user_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `address_id` int DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_status` varchar(20) DEFAULT 'Pending',
  `razorpay_order_id` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `address_id` (`address_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (4,16,1,500.00,'COD','Pending',NULL,'2026-04-05 08:26:11'),(7,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:02:09'),(8,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:04:00'),(9,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:06:20'),(10,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:06:25'),(11,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:06:54'),(12,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:15:36'),(13,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:16:10'),(14,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:16:51'),(15,31,1,23992.00,'COD','Pending',NULL,'2026-04-05 13:20:14'),(16,31,1,23992.00,'COD','Pending',NULL,'2026-04-05 13:23:24'),(17,31,1,23992.00,'COD','Pending',NULL,'2026-04-05 13:24:38'),(18,31,1,2999.00,'COD','Pending',NULL,'2026-04-05 13:47:16'),(19,22,1,2999.00,'COD','Pending',NULL,'2026-04-05 14:51:47');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_images`
--

DROP TABLE IF EXISTS `product_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `is_main` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_images_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_images`
--

LOCK TABLES `product_images` WRITE;
/*!40000 ALTER TABLE `product_images` DISABLE KEYS */;
INSERT INTO `product_images` VALUES (36,12,'products/WhatsApp Image 2026-04-11 at 10.14.39 AM(1).jpeg',1),(37,12,'products/WhatsApp Image 2026-04-11 at 10.14.39 AM.jpeg',0),(38,13,'products/WhatsApp Image 2026-04-11 at 10.15.15 AM.jpeg',1),(39,13,'products/WhatsApp Image 2026-04-11 at 10.15.14 AM.jpeg',0),(43,15,'products/WhatsApp Image 2026-04-11 at 10.13.54 AM.jpeg',1),(44,15,'products/WhatsApp Image 2026-04-11 at 10.13.56 AM.jpeg',0),(45,15,'products/WhatsApp Image 2026-04-11 at 10_kA0EMsm.13.54 AM.jpeg',0),(46,15,'products/WhatsApp Image 2026-04-11 at 10.13.56 AM (1).jpeg',0),(47,16,'products/WhatsApp Image 2026-04-10 at 10.29.10 PM (2).jpeg',1),(48,16,'products/WhatsApp Image 2026-04-11 at 10.13.52 AM (1).jpeg',0),(49,16,'products/WhatsApp Image 2026-04-11 at 10.13.59 AM (1).jpeg',0),(50,17,'products/WhatsApp Image 2026-04-10 at 10.29.19 PM (2).jpeg',1),(51,17,'products/WhatsApp Image 2026-04-11 at 10.14.01 AM.jpeg',0),(52,17,'products/WhatsApp Image 2026-04-10 at 10.29.24 PM.jpeg',0),(53,17,'products/WhatsApp Image 2026-04-11 at 10_sjlLWXx.14.00 AM (2).jpeg',0),(54,17,'products/WhatsApp Image 2026-04-11 at 10_7lJhPVk.14.01 AM (1).jpeg',0),(55,18,'products/WhatsApp Image 2026-04-10 at 10.29.36 PM (3).jpeg',1),(56,18,'products/WhatsApp Image 2026-04-10 at 10.29.17 PM.jpeg',0),(57,18,'products/WhatsApp Image 2026-04-10 at 10.29.19 PM (1).jpeg',0),(58,18,'products/WhatsApp Image 2026-04-10 at 10.29.37 PM (2).jpeg',0),(59,19,'products/WhatsApp Image 2026-04-10 at 10.29.35 PM (2).jpeg',1),(60,19,'products/WhatsApp Image 2026-04-10 at 10.29.35 PM (1).jpeg',0),(61,20,'products/WhatsApp Image 2026-04-10 at 10.29.35 PM.jpeg',1),(62,20,'products/WhatsApp Image 2026-04-10 at 10.29.34 PM (2).jpeg',0),(63,21,'products/WhatsApp Image 2026-04-10 at 10.29.05 PM (1).jpeg',1),(64,21,'products/WhatsApp Image 2026-04-10 at 10.29.05 PM.jpeg',0),(65,22,'products/WhatsApp Image 2026-04-10 at 10.29.05 PM (2).jpeg',1),(66,22,'products/WhatsApp Image 2026-04-10 at 10_trXXpcy.29.35 PM.jpeg',0),(67,22,'products/WhatsApp Image 2026-04-10 at 10_9xamn9R.29.05 PM (1).jpeg',0),(68,23,'products/WhatsApp Image 2026-04-10 at 10.29.06 PM.jpeg',1),(69,23,'products/WhatsApp Image 2026-04-10 at 10.29.30 PM.jpeg',0),(70,24,'products/WhatsApp Image 2026-04-10 at 10.29.06 PM (1).jpeg',1),(71,24,'products/WhatsApp Image 2026-04-10 at 10.29.18 PM (1).jpeg',0),(72,24,'products/WhatsApp Image 2026-04-10 at 10_WYX7KjT.29.19 PM (2).jpeg',0),(73,24,'products/WhatsApp Image 2026-04-11 at 10_lCxzK4W.14.00 AM (2).jpeg',0),(74,25,'products/WhatsApp Image 2026-04-10 at 10.29.06 PM (2).jpeg',1),(75,25,'products/WhatsApp Image 2026-04-10 at 10.29.09 PM (2).jpeg',0),(76,25,'products/WhatsApp Image 2026-04-10 at 10.29.30 PM (1).jpeg',0);
/*!40000 ALTER TABLE `product_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `price` decimal(10,2) NOT NULL,
  `old_price` decimal(10,2) DEFAULT NULL,
  `stock_quantity` int DEFAULT '0',
  `is_trending` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `category_id` int NOT NULL,
  PRIMARY KEY (`product_id`),
  KEY `fk_category` (`category_id`),
  CONSTRAINT `fk_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (12,'semi  pattu vintage saree with both side Kanchi desgin','Exclusive collection semi  pattu vintage saree with both side Kanchi desgin \r\nRich contrast pallu n contrast blouse\r\nAllover saree mangalagiri checks\r\nEach colour 25 saree available\r\n',1399.00,1999.00,100,0,'2026-04-11 01:24:07',21),(13,'semi  pattu vintage saree with both side Kanchi desgin','Exclusive collection semi  pattu vintage saree with both side Kanchi desgin \r\nRich contrast pallu n contrast blouse\r\nAllover saree mangalagiri checks',1399.00,1999.00,100,0,'2026-04-11 01:25:48',21),(15,'Classy green mango pattu saree desgin ','Allover saree nice zari weaving butts  desgin \r\nClassy weaving creaper boader desgin  rich pallu n contrast  blouse',2650.00,3550.00,100,0,'2026-04-11 01:36:41',22),(16,'Classy krishna blue  pattu saree desgin','Allover saree nice zari weaving butts  desgin \r\nClassy weaving creaper boader desgin  rich pallu n contrast  blouse',2650.00,2950.00,100,0,'2026-04-11 07:57:07',21),(17,'Classy red pattu saree desgin ','Allover saree nice zari weaving butts  desgin \r\nClassy weaving creaper boader desgin  rich pallu n contrast  blouse',2655.00,3550.00,100,0,'2026-04-11 08:00:10',21),(18,'gradient colors of  pattu saree','Allover saree nice zari weaving butts  desgin \r\nClassy weaving creaper boader desgin  rich pallu n contrast  blouse',2999.00,3599.00,100,0,'2026-04-11 08:05:00',21),(19,'pochampally lkat style saree with white and red color','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',2555.00,2999.00,100,0,'2026-04-11 08:12:53',22),(20,'tusser silk saree [light wight,classy]','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',2555.00,2999.00,100,0,'2026-04-11 08:15:38',22),(21,'silk saree','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',1999.00,2555.00,100,0,'2026-04-11 09:06:30',22),(22,'soft silk saree','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',1999.00,2555.00,100,0,'2026-04-11 09:08:46',23),(23,'blue color saree with red border','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',2499.00,2899.00,100,0,'2026-04-11 09:12:23',21),(24,'red colour saree with best border','Embrace timeless Indian artistry with this stunning handloom-inspired saree. Featuring a rich crimson body contrasted against a striking monochrome striped pallu, this piece is defined by its iconic \"temple\" zigzag border.',2999.00,3499.00,100,0,'2026-04-11 09:14:05',22),(25,'mysore silk zaranlines wearing desigin','classy rich peacock weaving pallu n plain blouse\r\n',3699.00,3999.00,100,0,'2026-04-11 09:22:39',24);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_joined` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (16,'Akash','p.akash.me10@gmail.com','9000920161','pbkdf2_sha256$1200000$H2EXQkLZZ8pxnUP20iCndZ$WN0EECL8zXuZ7q//EHbuTPCemPpGr/T+ptGVTtBq54A=','2026-03-31 01:47:38','2026-03-31 12:49:05',1),(17,'aniket','talwekar@gmail.com','9370969887','pbkdf2_sha256$1200000$ldaeIOcdVKRXMZQYyMRs7S$X3Sqdo05T6vZVBQKEmiTU6byfGI5oaek+EmblB+OSEQ=','2026-03-31 11:18:21','2026-03-31 16:48:45',1),(18,'Akash Patnamsetty','p.akashme10@gmail.com','9000920171','pbkdf2_sha256$1200000$E2Yvy4xQNgKSL9Gmd7LXuY$+FKQrjCeQVfBfiTCREO7vNgHN2G4VwiQlEiorzBmYSE=','2026-04-02 06:26:33','2026-04-02 11:57:21',1),(19,'adi','adibonthala2003@gmail.com','7396016754','pbkdf2_sha256$1200000$u1zE3UJ7jhSbmtwNYPIlr9$PXpDVxhLXg9vG37wQ3kyZln7Q0AZ+pVfFKtYeIdRab4=','2026-04-03 01:50:54','2026-04-03 07:21:21',1),(20,'mimi','p.akash10@gmail.com','6900092016','pbkdf2_sha256$1200000$gt5LgrPsUc8bmRlqttpNvG$wdtUfl0w4qeuuNbgwMamD5YgNOlN7nT0vNjQJEWV7OI=','2026-04-03 07:12:23','2026-04-03 12:42:35',1),(21,'akki','p.akash@gmail.com','9100920161','pbkdf2_sha256$1200000$G9NNo9moqpRp0dwRMxCxgx$qyx/QJCKiH9IvcEdkMChuqGjazx0tboxKWQnMy3khXw=','2026-04-05 04:09:28','2026-04-05 09:39:50',1),(22,'Anji','pakash10@gmail.com','9200920161','pbkdf2_sha256$1200000$sgzKTfAkHLzYXL4k6Uugvu$hMxI1h6pxPWfyMv5Uxt38RJ8fvLY61tXpVr3JdyKVy4=','2026-04-05 06:51:00','2026-04-05 12:21:52',1),(23,'Sarath chandra','saraththeruler33@gmail.com','07386568606','pbkdf2_sha256$1200000$mTqyAxqOgjAYmX9RKVQpV5$zqPY+3smyDn7qz9kouB1//mS82VAw9m0AbYQgeYeZSo=','2026-04-05 08:53:30','2026-04-05 14:23:46',1),(24,'Khalifunnisa Begum','unnisa143@gmail.com','1111111111','pbkdf2_sha256$1200000$N2cA0TcC4BJnMe3saL6I7M$ANCKOkTHwlCsQ5So1Alkbkcc5FLUj10tnFawKHCMO4E=','2026-04-05 09:18:02','2026-04-05 14:48:22',1),(25,'abc','abc@jfnksafnckla','123','pbkdf2_sha256$1200000$Tdg1jqRZtnrKBog4hIZZfx$dqfSYCuTHPrWbLClWaM4ZFHdmcGS5VwEYWYNBuVHhOw=','2026-04-05 09:21:24',NULL,1),(26,'a','1111111111@gsafsdf','1','pbkdf2_sha256$1200000$mni20PLgOeGj7ob1lKzsHo$Sq8sbDGMaw54vcA56TJgAE3J7c86BdMTUBdL9othWlE=','2026-04-05 09:24:22',NULL,1),(27,'Akash Patnamsetty','p.a@com','11111','pbkdf2_sha256$1200000$uFJc7NL1qlUtUK55OLIeQu$DTQ+k13vQnO3qT8kwqka+f1DS8JNV753zagi67Ag+rQ=','2026-04-05 09:25:29',NULL,1),(28,'akki','p.aksh10@gmail.com','9000990161','pbkdf2_sha256$1200000$hAil3PBQiHywTazJph6ZYu$ptBbBCHBU6XUdva+t6tPlJ/C5akwgpqOcAlBeGJhi10=','2026-04-05 09:49:41','2026-04-05 15:19:59',1),(29,'asd','aaa@gmail.com','9999999999','pbkdf2_sha256$1200000$v2LzRQ8YFAJJJUcHLej7vr$INu4ac6i0GuEy+NTohP8wXjP1E3V2d0XsgUg8fPSniE=','2026-04-05 10:32:25','2026-04-05 16:02:50',1),(30,'Dinesh Nagandla','dineshnagandla0@gmail.com','7032970626','pbkdf2_sha256$1200000$IGFkCqkFDHC4kr5nQ73hwF$sodlmUAbDgq6ihoJxH5uQO4lpsaQZSrLaLgJx0eruSM=','2026-04-05 11:51:19','2026-04-05 17:21:31',1),(31,'Akash Patnamsetty','p.akash.me10@gmailvv.com','9000920111','pbkdf2_sha256$1200000$1Y6io7hP7b2CyzhORZ9LWW$Kc8koGgx8I+AfO9rcu0uWGLz3X1moOFXgAcwzR6BNPQ=','2026-04-05 12:06:03','2026-04-05 17:36:15',1),(32,'Akash Patnamsetty','akash@gmail.com','9898123223','pbkdf2_sha256$1200000$Tz2hoenGwujV9qUt3UxRB2$uxoj5nxT+3r/qA6gwBvJAptDSD2ED+OyXRh/DbujQEw=','2026-04-06 06:32:09','2026-04-06 12:02:24',1),(33,'King','mrxman@gmail.com','9143262752','pbkdf2_sha256$1200000$RfNYDqAhQE68OngjNZtcLA$tiwlJd0bycyGiDYqgsX1xg60Y/52Ubn2axmxUM5heT4=','2026-04-10 03:17:15','2026-04-10 08:48:14',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-20 12:11:55
