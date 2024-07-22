-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 05, 2024 at 11:31 AM
-- Server version: 8.0.36-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `jawazat`
--

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE `answers` (
  `id` int NOT NULL,
  `option` varchar(30) NOT NULL,
  `option_ar` varchar(30) NOT NULL,
  `option_fr` varchar(30) NOT NULL,
  `option_zh` varchar(30) NOT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `answers`
--

INSERT INTO `answers` (`id`, `option`, `option_ar`, `option_fr`, `option_zh`, `createdAt`, `updatedAt`) VALUES
(1, 'راضي', 'AR OPT 1 AR', 'FR OPT 1 FR', 'ZH OPT 1 ZH', '2023-12-19 11:43:59', '2023-12-19 11:43:59'),
(2, 'مقبول', 'AR OPT 2 AR', 'FR OPT 2 FR', 'ZH OPT 2 ZH', '2023-12-19 11:44:25', '2023-12-19 11:44:25'),
(3, 'غير راضي', 'AR OPT 3 AR', 'FR OPT 3 FR', 'ZH OPT 3 ZH', '2023-12-19 11:44:34', '2023-12-19 11:44:34');

-- --------------------------------------------------------

--
-- Table structure for table `askme_category`
--

CREATE TABLE `askme_category` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `askme_category`
--

INSERT INTO `askme_category` (`id`, `name`) VALUES
(1, 'مواطن'),
(2, 'مقيم'),
(3, 'زائر'),
(4, 'حاج'),
(5, 'معتمر'),
(6, 'أخرى');

-- --------------------------------------------------------

--
-- Table structure for table `conversation`
--

CREATE TABLE `conversation` (
  `id` int NOT NULL,
  `question` varchar(150) NOT NULL,
  `question_ar` varchar(100) NOT NULL,
  `question_fr` varchar(100) NOT NULL,
  `question_zh` varchar(100) NOT NULL,
  `answer` varchar(300) NOT NULL,
  `answer_ar` text NOT NULL,
  `answer_fr` text NOT NULL,
  `answer_zh` text NOT NULL,
  `category` int NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `conversation`
--

INSERT INTO `conversation` (`id`, `question`, `question_ar`, `question_fr`, `question_zh`, `answer`, `answer_ar`, `answer_fr`, `answer_zh`, `category`) VALUES
(47, 'How old are you', 'انا بخير والحمد لله', 'Quel âge avez-vous', '你今年多大', 'I am 22', 'عمري 23', 'j\'ai 22 ans', '我22歲', 1),
(48, 'Who is the manager?', 'من هو المدير', 'Qui est le gérant ?', '經理是誰？', 'The manager is Ammar from Sudan', 'المدير هو عمار من السودان', 'Le manager est Ammar du Soudan', '經理是來自蘇丹的Ammar', 6),
(49, 'who is bilal', 'من هو بلال', 'Qui est Bilal ?', '比拉爾是誰？', 'He is the best programmer in the world', 'هو افضل مبرمج في العالم', 'C\'est le meilleur programmeur du monde', '他是世界上最好的程式設計師', 2),
(50, 'What is your name', 'ما اسمك؟', 'Quel est votre nom?', '你叫什麼名字', 'I\'m fine', 'انا بخير', 'Je vais bien', '我很好', 3);

-- --------------------------------------------------------

--
-- Table structure for table `functions_update_flag`
--

CREATE TABLE `functions_update_flag` (
  `id` int NOT NULL,
  `name` varchar(20) NOT NULL,
  `is_updated` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `functions_update_flag`
--

INSERT INTO `functions_update_flag` (`id`, `name`, `is_updated`) VALUES
(1, 'survey', 1),
(2, 'main_robot_functions', 0),
(3, 'take_me', 0);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int NOT NULL,
  `question` text NOT NULL,
  `question_ar` varchar(150) NOT NULL,
  `question_fr` varchar(150) NOT NULL,
  `question_zh` varchar(150) NOT NULL,
  `createdAt` datetime NOT NULL,
  `updatedAt` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question`, `question_ar`, `question_fr`, `question_zh`, `createdAt`, `updatedAt`) VALUES
(1, 'First survey question', 'مرحبا بكم', 'FR survey question 1 FR', 'ZH survey question 1 ZH', '2023-12-19 11:43:59', '2023-12-19 11:43:59');

-- --------------------------------------------------------

--
-- Table structure for table `robot_functions`
--

CREATE TABLE `robot_functions` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `robot_functions`
--

INSERT INTO `robot_functions` (`id`, `name`, `status`) VALUES
(1, 'support', 1),
(2, 'take_me', 0),
(3, 'ask_me', 1),
(4, 'suggestions', 1),
(5, 'survey', 1),
(6, 'procedures', 1);

-- --------------------------------------------------------

--
-- Table structure for table `robot_usage`
--

CREATE TABLE `robot_usage` (
  `id` int NOT NULL,
  `name` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lang` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `robot_usage`
--

INSERT INTO `robot_usage` (`id`, `name`, `created_at`, `lang`) VALUES
(1, 'ask_me', '2024-04-17 07:18:23', 'en'),
(2, 'sugg_comp', '2024-04-17 07:18:26', 'en'),
(3, 'survey', '2024-04-17 07:18:40', 'en'),
(4, 'procedures', '2024-04-17 07:18:44', 'en'),
(5, 'support', '2024-04-17 07:18:48', 'en'),
(6, 'ask_me', '2024-04-17 07:21:08', 'en'),
(7, 'ask_me', '2024-04-17 07:23:50', 'ar'),
(8, 'ask_me', '2024-04-17 07:38:33', 'en'),
(9, 'survey', '2024-04-17 10:50:55', 'ar'),
(10, 'ask_me', '2024-04-18 07:20:40', 'ar'),
(11, 'survey', '2024-04-18 07:21:01', 'ar'),
(12, 'ask_me', '2024-04-18 07:35:10', 'en'),
(13, 'procedures', '2024-04-18 07:35:17', 'en'),
(14, 'sugg_comp', '2024-04-18 07:35:22', 'en'),
(15, 'support', '2024-04-18 07:35:33', 'ar'),
(16, 'ask_me', '2024-04-18 07:46:44', 'ar'),
(17, 'survey', '2024-04-18 07:46:52', 'ar'),
(18, 'ask_me', '2024-04-18 07:47:35', 'ar'),
(19, 'ask_me', '2024-04-18 07:48:15', 'ar'),
(20, 'sugg_comp', '2024-04-18 07:48:19', 'ar'),
(21, 'sugg_comp', '2024-04-18 07:50:13', 'ar'),
(22, 'sugg_comp', '2024-04-18 07:51:47', 'ar'),
(23, 'sugg_comp', '2024-04-18 07:54:19', 'ar'),
(24, 'sugg_comp', '2024-04-18 07:55:30', 'en'),
(25, 'procedures', '2024-04-18 07:58:58', 'en'),
(26, 'ask_me', '2024-04-18 09:09:27', 'en'),
(27, 'ask_me', '2024-04-18 10:48:40', 'en'),
(28, 'ask_me', '2024-04-18 10:48:47', 'en'),
(29, 'sugg_comp', '2024-04-18 10:48:56', 'en'),
(30, 'sugg_comp', '2024-04-18 10:48:58', 'en'),
(31, 'sugg_comp', '2024-04-18 10:49:00', 'en'),
(32, 'sugg_comp', '2024-04-18 10:49:01', 'en'),
(33, 'sugg_comp', '2024-04-18 10:49:03', 'en'),
(34, 'sugg_comp', '2024-04-18 10:49:04', 'en'),
(35, 'sugg_comp', '2024-04-18 10:49:05', 'en'),
(36, 'sugg_comp', '2024-04-18 10:49:10', 'en'),
(37, 'sugg_comp', '2024-04-18 10:49:11', 'en'),
(38, 'sugg_comp', '2024-04-18 10:49:12', 'en'),
(39, 'sugg_comp', '2024-04-18 10:49:13', 'en'),
(40, 'sugg_comp', '2024-04-18 10:49:15', 'en'),
(41, 'sugg_comp', '2024-04-18 10:49:16', 'en'),
(42, 'survey', '2024-04-18 12:05:38', 'en'),
(43, 'ask_me', '2024-04-18 12:07:32', 'en'),
(44, 'ask_me', '2024-04-21 08:42:33', 'ar'),
(45, 'ask_me', '2024-04-21 10:28:43', 'ar'),
(46, 'ask_me', '2024-04-21 10:30:33', 'ar'),
(47, 'ask_me', '2024-04-21 10:31:22', 'ar'),
(48, 'ask_me', '2024-04-21 11:29:11', 'ar'),
(49, 'ask_me', '2024-04-22 09:38:48', 'en'),
(50, 'ask_me', '2024-04-22 09:39:00', 'ar'),
(51, 'ask_me', '2024-04-22 09:41:46', 'ar'),
(52, 'support', '2024-04-22 09:48:16', 'ar'),
(53, 'ask_me', '2024-04-22 09:48:41', 'ar'),
(54, 'ask_me', '2024-04-22 10:21:41', 'ar'),
(55, 'ask_me', '2024-04-22 10:25:17', 'en'),
(56, 'ask_me', '2024-04-22 10:39:02', 'en'),
(57, 'ask_me', '2024-04-22 10:39:38', 'ar'),
(58, 'support', '2024-04-22 10:40:42', 'ar'),
(59, 'sugg_comp', '2024-05-01 06:38:12', 'en');

-- --------------------------------------------------------

--
-- Table structure for table `surveys`
--

CREATE TABLE `surveys` (
  `id` int NOT NULL,
  `session_id` bigint NOT NULL,
  `question_id` int DEFAULT NULL,
  `answer_id` int DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `surveys`
--

INSERT INTO `surveys` (`id`, `session_id`, `question_id`, `answer_id`, `date`) VALUES
(18, 713424861168, 1, 1, '2024-04-18'),
(23, 713426412445, 1, 2, '2024-04-18'),
(28, 713441938952, 1, 1, '2024-04-18');

-- --------------------------------------------------------

--
-- Table structure for table `take_me_map`
--

CREATE TABLE `take_me_map` (
  `composer_id` varchar(30) NOT NULL,
  `composer_name` text NOT NULL,
  `point_name` text NOT NULL,
  `point_name_ar` varchar(25) NOT NULL,
  `point_name_fr` varchar(25) NOT NULL,
  `point_name_zh` varchar(25) NOT NULL,
  `lang` text NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `take_me_map`
--

INSERT INTO `take_me_map` (`composer_id`, `composer_name`, `point_name`, `point_name_ar`, `point_name_fr`, `point_name_zh`, `lang`, `status`) VALUES
('_s6a34avgck', 'kkia_home', 'Point 1', 'المكان الأول', 'Point 1 FR', 'Point 1 ZH', 'AR', 1),
('_szijps1rc3', 'kkia_success', 'Point 2', 'المكان الثاني', 'Point 2 FR', 'Point 1 ZH', 'EN', 1),
('_szijps1rc334', 'kkia_success', 'point 3', 'المكان الثالث', 'Point 3 FR', 'Point 1 ZH', 'EN', 1),
('_szijps1rc3cdh', 'kkia_success', 'halaby', 'المكان الرابع', 'Point 4 FR', 'Point 1 ZH', 'EN', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint UNSIGNED NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `remember_token` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `remember_token`, `created_at`, `updated_at`) VALUES
(1, 'Admin', 'admin@jawazat.com', NULL, '$2y$12$eJ9iR87tdR0VLtZs0FLVfuaUnUsthrqwpLSzVSAriBoSgGFnYI8lC', NULL, '2024-04-05 11:08:26', '2024-04-05 11:08:26'),
(3, 'Woodrow Baumbach', 'jawazat@qltyss.com', '2024-04-22 08:27:02', '$2y$10$ahmTttGMBFEP329bFmeZxO.29.61j9mh2B1VHLxdDJG/B0BJexqwa', 'POyDgMkdVxuLmzV4BJuDrtDg1qvY7mesDWm8Dj27fxc9Uimr8CZ8UM8LC05e', '2024-04-22 08:27:02', '2024-04-22 08:27:02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `answers`
--
ALTER TABLE `answers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `askme_category`
--
ALTER TABLE `askme_category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `conversation`
--
ALTER TABLE `conversation`
  ADD PRIMARY KEY (`id`),
  ADD KEY `conversation_ibfk_1` (`category`);

--
-- Indexes for table `functions_update_flag`
--
ALTER TABLE `functions_update_flag`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `robot_functions`
--
ALTER TABLE `robot_functions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `robot_usage`
--
ALTER TABLE `robot_usage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `surveys`
--
ALTER TABLE `surveys`
  ADD PRIMARY KEY (`id`),
  ADD KEY `surveys_ibfk_1` (`question_id`),
  ADD KEY `surveys_ibfk_2` (`answer_id`);

--
-- Indexes for table `take_me_map`
--
ALTER TABLE `take_me_map`
  ADD PRIMARY KEY (`composer_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `answers`
--
ALTER TABLE `answers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `askme_category`
--
ALTER TABLE `askme_category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `conversation`
--
ALTER TABLE `conversation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT for table `functions_update_flag`
--
ALTER TABLE `functions_update_flag`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `robot_functions`
--
ALTER TABLE `robot_functions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `robot_usage`
--
ALTER TABLE `robot_usage`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT for table `surveys`
--
ALTER TABLE `surveys`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `conversation`
--
ALTER TABLE `conversation`
  ADD CONSTRAINT `conversation_ibfk_1` FOREIGN KEY (`category`) REFERENCES `askme_category` (`id`);

--
-- Constraints for table `surveys`
--
ALTER TABLE `surveys`
  ADD CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `questions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `surveys_ibfk_2` FOREIGN KEY (`answer_id`) REFERENCES `answers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
