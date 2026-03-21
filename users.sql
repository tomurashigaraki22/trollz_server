-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 21, 2026 at 01:29 AM
-- Server version: 8.0.40
-- PHP Version: 8.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trollzstorecom_tr0llz_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(10) NOT NULL,
  `status` int NOT NULL,
  `reset_token` varchar(255) DEFAULT NULL,
  `token_expiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `phone`, `password`, `role`, `status`, `reset_token`, `token_expiry`) VALUES
(2, 'YoungX', 'YoungXadmin', '0', 'tr0ll5t0r3z', 'Admin', 0, NULL, NULL),
(4, 'Test1', 'custom@customer.com', '2147483647', '123456', 'Customer', 0, NULL, NULL),
(5, 'Chinedum Emmanuel', 'chinedumemmanuel73@gmail.com', '2147483647', '$2y$10$Z6YuWIAm/meSqbrQPWbRMeay3h1U0e8tHUnlq79Qr78vrYaC.cnEy', 'Customer', 0, '68c00aafa8dbd2bd89eb585b98942db0', '2025-11-24 23:32:46'),
(6, 'Vincent ', 'vincentoluwafemi11@gmail.com', '2147483647', '$2y$10$Eg9IBLZ6Eb7aw6HNpNcoKuvkqsddpHcsDrLHR6vSOkFsHTlUWiWXm', 'Customer', 0, '77fe3a425017ffb89994f4db001c2454', '2025-08-31 11:35:29'),
(7, 'Abraham Ekwere ', 'ekwere4abraham@gmail.com', '2147483647', 'Daflex1998', 'Customer', 0, NULL, NULL),
(8, 'Miracle ', 'miraclebarbie5@gmail.com', '2147483647', '200244', 'Customer', 0, NULL, NULL),
(9, 'Angel beauty ', 'okeprecious238@gmail.com', '2147483647', 'favour123#', 'Customer', 0, NULL, NULL),
(10, 'Collins Olohi', 'solsammedia@gmail.com', '2147483647', 'Myworld26$', 'Customer', 0, NULL, NULL),
(11, 'Precious ', 'preciouschikezie149@gmail.com', '70', 'fred', 'Customer', 0, NULL, NULL),
(12, 'Precious ', 'fredp8248@gmail.com', '70', 'fred', 'Customer', 0, NULL, NULL),
(13, 'Charles Dubem', 'doubblepventures@gmail.com', '2147483647', 'Youcantseeme@30', 'Customer', 0, NULL, NULL),
(14, 'King zarry ', 'Zarryking06@gmail.com', '701973728', 'Sabinos2233', 'Customer', 0, NULL, NULL),
(15, 'Alicia White', 'aliciawhite818@gmail.com', '08169889760', 'bestbaby', 'Customer', 0, NULL, NULL),
(16, 'Harry Potter', 'oajayi@caretafrica.com', '08110146513', 'Expelliarmus', 'Customer', 0, NULL, NULL),
(17, 'Raphael Tomiwa', 'emmanuelhudson355@gmail.com', '09110520620', 'Pityboy@22', 'Customer', 0, NULL, NULL),
(18, 'STARNET', 'sirvic52@gmail.com', '08069970081', 'YGDQHRmQxfMg4mT', 'Customer', 0, NULL, NULL),
(19, 'Thankgod ', 'thankgoduzochukwu557@gmail.com', '08110581634', 'thankgod..9', 'Customer', 0, NULL, NULL),
(20, 'Osibemhe Elect ', 'profetcastle@gmail.com', '08126600294', 'elect5125320', 'Customer', 0, NULL, NULL),
(21, 'Christian Ukandu ', 'chrisukandu66@gmail.com', '08162991401', 'mexiconation', 'Customer', 0, NULL, NULL),
(22, 'Peter', 'isibor.peter@gmail.com', '08149094361', 'Petrol10', 'Customer', 0, NULL, NULL),
(23, 'Chinedu Darlington chukwuemeka ', 'chinedudarlington818@gmail.com', '+2348153450427', '97621134', 'Customer', 0, NULL, NULL),
(24, 'Isaac umoren', 'isaacumoren474@gmail.com', '09033032727', 'zyrrej-xystad-0nazkA', 'Customer', 0, NULL, NULL),
(25, 'Maryjane', 'queenmaryjane345@gmail.com', '08129896020', 'queenmaryjane', 'Customer', 0, NULL, NULL),
(26, 'Daniel', 'daniranking83@gmail.com', '9133945436', '21099', 'Customer', 0, NULL, NULL),
(27, 'Precious Oluomachi ', 'ibehprecious2004@gmail.com', '07079808736', 'Godwithus@22', 'Customer', 0, NULL, NULL),
(28, 'Dennis', 'donsavage75@gmail.com', '09071410781', 'Savage375$', 'Customer', 0, NULL, NULL),
(29, 'Kafilat Boluwatife ', 'rabiukafilat9@gmail.com', '09162562076', 'Kafilat', 'Customer', 0, NULL, NULL),
(30, 'Valentina Samuel', 'valentinasamuel91@gmail.com', '+2348106682879', 'strongtweet234', 'Customer', 0, NULL, NULL),
(31, 'Jeff', 'jeffreyugbodaga7@gmail.com', '08162406364', '$Youngkvng10', 'Customer', 0, NULL, NULL),
(32, 'Monday Precious', 'mondayouvokeye@gmail.com', '08169898468', 'Precious2003', 'Customer', 0, NULL, NULL),
(33, 'Divine', 'divineabundance899@gmail.com', '07067298493', 'Bestabigail123.', 'Customer', 0, NULL, NULL),
(34, 'Akanji ', 'akanjigazali@gmail.com', '08152811479', 'olatunji2', 'Customer', 0, NULL, NULL),
(35, 'Jessie', 'onyieni24@gmail.com', '07028306309', 'kimjongin', 'Customer', 0, NULL, NULL),
(36, 'Aloysius ', 'talk2aloy@gmail.com', '09078618190', 'aloy1010', 'Customer', 0, NULL, NULL),
(37, 'Anastasia nwosa', 'preciousnwosa@gmail.com', '08130741288', 'trendyyy', 'Customer', 0, NULL, NULL),
(38, 'Kevin bright ', 'kevinbrighten125@gmail.com', '08164709761', 'OSINACHI123$', 'Customer', 0, NULL, NULL),
(40, 'Pella', 'Pellashmurda42@gmail.com', '09025057795', 'Brindle1', 'Customer', 0, NULL, NULL),
(41, 'Ayomide ', 'elizabethayomide2023@gmail.com', '09133828737', '200517', 'Customer', 0, NULL, NULL),
(42, 'Atiku Abdulsalam Muhammad', 'atikuabdulsalam777@gmail.com', '08107641948', 'Atiku777', 'Customer', 0, NULL, NULL),
(43, 'Ozioma ihematunam ', 'Ozyihematunam@gmail.com', '07086521447', '0708', 'Customer', 0, NULL, NULL),
(44, 'Udoka', 'udokakelechukwu@gmail.com', '09136351340', '10283170', 'Customer', 0, NULL, NULL),
(45, 'Tomori Maryam ', 'marymatomori@gmail.com', '07040258749', 'Maryma0205#', 'Customer', 0, NULL, NULL),
(46, 'Ola', 'maryhkendra780@gmail.com', '08085078518', 'looking000', 'Customer', 0, NULL, NULL),
(48, 'YOUNG PROSPER ', 'Unezeprosper470@gmail.com', '08102783442', '07042214228', 'Customer', 0, NULL, NULL),
(49, 'Success', 'successonyekachi08@gmail.com', '07010616549', 'successful12345', 'Customer', 0, NULL, NULL),
(50, 'Abraham ', 'hasanmithatt@gmail.com', '09012247186', 'DAFLEX1998.', 'Customer', 0, NULL, NULL),
(51, 'Uche', 'godswillu461@gmail.com', '09025694977', 'Brindke2', 'Customer', 0, NULL, NULL),
(52, 'Victor ', 'vnwankwo804@gmail.com', '08162289128', 'Priest9o9@', 'Customer', 0, 'c2e61618a8bb8f16d081dcbfdbbc0aec', '2025-11-01 10:34:22'),
(53, 'Fred ADA ', 'Jefferus145@gmail.com', '070 7641 6523', 'precious', 'Customer', 0, NULL, NULL),
(54, 'Green Dagogo Larry ', 'larrygreen2844@gmail.com', '09168499740', 'Reset2844', 'Customer', 0, NULL, NULL),
(55, 'Ndubuisi Henry ', 'henryndubuisi686@gmail.com', '09137920698', 'mynameis _001', 'Customer', 0, NULL, NULL),
(56, 'Goodness ', 'Ogoodness970@gmail.com', '+23407030024087', 'savage006', 'Customer', 0, NULL, NULL),
(57, 'Success', 'nwankwos604@gmail.com', '08140291381', 'Onyedikachi2008', 'Customer', 0, 'b6e99202695ec562fa76ec5e874e0e6b', '2025-09-16 10:03:42'),
(58, 'Green Larry ', 'larry0032021@gmail.com', '09073593337', 'Larryand@99', 'Customer', 0, NULL, NULL),
(59, 'Udochukwu ', 'yuddieprosper@gmail.com', '08108391907', '$2y$10$8CNpyZZcKBlN8AhbuG1VFucEJ9vp6u1cP8s.nqQdyAMj578EuDGRC', 'Customer', 0, NULL, NULL),
(60, 'Uche pius', 'owulezipius468@gmail.com', '09132479514', 'Uchepius2', 'Customer', 0, NULL, NULL),
(61, 'princewill ', 'Okereprincewill818@gmail.com', '08032455344', 'cashout3030', 'Customer', 0, NULL, NULL),
(62, 'Akinlabi Gbolahan', 'akandegbolahan166@gmail.com', '09156232452', 'Gbolahan1839', 'Customer', 0, NULL, NULL),
(63, 'Odunze favour', 'odunzefavour95@gmail.com', '08100389701', 'Trollzpassword0810', 'Customer', 0, NULL, NULL),
(64, 'Greg', 'oucprof@gmail.com', '07042265580', 'Malika@393', 'Customer', 0, NULL, NULL),
(65, 'Prime ', 'ganiyualli90@gmail.com', '08118616126', '12334578', 'Customer', 0, NULL, NULL),
(66, 'UCHECHUKWU ', 'Emperorjohnny50@gmail.com', '07040626542', 'Maria@50', 'Customer', 0, NULL, NULL),
(67, 'Green Dagogo Larry ', 'nathanlevi896@gmail.com', '08131474487', '8131474487', 'Customer', 0, NULL, NULL),
(68, 'BIG~JANE', 'ujoy37507@gmail.com', '08166847061', 'popwuv-qukwy2-Romtix', 'Customer', 0, NULL, NULL),
(69, 'Okoji Victor', 'victorokoji35@gmail.com', '08126032024', 'victor1$', 'Customer', 0, NULL, NULL),
(70, 'Lazzy', 'davidjames200505@gmail.com', '07026833835', 'lazzyberry', 'Customer', 0, NULL, NULL),
(71, 'Boluwatife', 'Boluwatifeayodele08@Gmail.Com', '08136572595', 'Password', 'Customer', 0, NULL, NULL),
(72, 'Gideon Simon', 'simonsamuel195@gmail.com', '08102668426', 'Samuel123', 'Customer', 0, NULL, NULL),
(73, 'Barbie ', 'hopek1645@gmail.com', '08066786578', 'hopek1645', 'Customer', 0, NULL, NULL),
(74, 'Claudiu', 'serclaude81@gmail.com', '0728887153', 'Akci.2os', 'Customer', 0, NULL, NULL),
(75, 'Success ', 'Symplymama456@gmail.com', '09032136294', 'Sm223344567', 'Customer', 0, NULL, NULL),
(76, 'Kenechukwu', 'anosikekeechukwu2023@gmail.com', '9022665965', 'Kene2004#', 'Customer', 0, NULL, NULL),
(77, 'Sylvanus Dogo', 'Sylvanusdogo60@gmail.com', '08121658508', '$2y$10$If44bns4xHVVVY7.7yEw2ucKbVpYSIEtclP5jO1Fy0WtBdMgesBo.', 'Customer', 0, NULL, NULL),
(79, 'Sinokor Maritime', 'nuelz800@gmail.com', '081698897606', '$2y$10$tAPuHjS.PjG7iwLxUq/6cOWvrpw9WhmZ9XhFScdk9EZBVny/8aQtS', 'Customer', 0, NULL, NULL),
(80, 'Angel Lee', 'angelinaleorita@gmail.com', '08021153827', '$2y$10$lgl8AXnkH2Ib1OVjFSsBTuvxQqka89EFZFF.iQ.yqx/4bqYHxej0G', 'Customer', 0, NULL, NULL),
(81, 'Sandra', 'cardioflagos@gmail.com', '07045763099', '$2y$10$vd3oD0lgzFBbRdfz89dR0eHv7T/xYKSYI197GByneLEBlh5AMiWOi', 'Customer', 0, NULL, NULL),
(82, 'ggg', 'dddd@gmail.com', '5674878579', '$2y$10$P3kcy4iMNsvHk3PN78KKD.2z8jQH6XWy0Lov/l3Jd5.o36wJ8cQhy', 'Customer', 0, NULL, NULL),
(83, 'Akorede', 'akoredeayomide099@gmail.com', '07062864074', '$2y$10$HjYmIMOy73eLr1mb0Pp6EeO9rJ4B7bFo/AMBNfxc9coA6MVHz5FG6', 'Customer', 0, NULL, NULL),
(84, 'Diogu', 'victordiogu22@gmail.com', '08148588460', '$2y$10$L7BS.TdLBOJlub5x0HGEweWBKDmFzXXd7D6a.7IHbMg9CgWuWfbYG', 'Customer', 0, NULL, NULL),
(85, 'Faith', 'felixfaith723@gmail.com', '07038628788', '$2y$10$wq00jdJXkpR/G6ekFNnu.u4qF6a0r.BUuA52g7OK.TtPYuzkIVFRe', 'Customer', 0, NULL, NULL),
(86, 'Laka', 'chilakaebuka27@gmail.com', '09075950537', '$2y$10$u0Lp4eu0meMwb1R9HwWBJeNg9mcpqdwyUKEw8GdQ4RH.GWuAqgtrS', 'Customer', 0, NULL, NULL),
(87, 'Tesla', 'codewave400@gmail.com', '07043488949', '$2y$10$QugGq7sJgxlXjrIodUSs4eSSsKy.BDTb.ajAjl8C5RwFSp3kVoBli', 'Customer', 0, NULL, NULL),
(88, 'Carl', 'kalnwakanma@gmail.com', '07046385301', '$2y$10$5IYM0GZudHM3HePXaR4SVu8DU.SIhi0I8wnaxnpvSokQcvPSUfgLi', 'Customer', 0, NULL, NULL),
(89, 'jude', 'jachikejude8@gmail.com', '09165115830', '$2y$10$md7SH8uT3bcaf5Ngq1gt8ubWbwww3ssHiWodhC3FOjr1oQOIExCvG', 'Customer', 0, NULL, NULL),
(90, 'success', 'earnily266@gmail.com', '08011111111', '$2y$10$WOeqlbscgcq19eDNoICsPuEF2jIQPZllfc.vtrx5S/mCJhdLxZ3py', 'Customer', 0, NULL, NULL),
(91, 'Barron', 'ekwuemedaniel03@gmail.com', '09065020718', '$2y$10$ZU1OJvOJcxxNNccvTDz4mOmfKzg8S.wkEL5o8n9VakCVqh/OqTfq.', 'Customer', 0, NULL, NULL),
(92, 'Chima winner David', 'chimawinner18@gmail.com', '09035253052', '$2y$10$0f74u8hJBIjjLDjMT.Yo3.d1vrYu7rwDdyrGW7nn1x4Ms6ZmHppNe', 'Customer', 0, NULL, NULL),
(93, 'Opeifa Lawrence Olawale', 'ololadeadetoun@gmail.com', '08135490879', '$2y$10$.K7QraSF0J8SEWvbHWgw.eB4.FYTO4n.y92L3F6u9a.7xY7wgU0.S', 'Customer', 0, NULL, NULL),
(94, 'Alexander', 'okoliealexander46@gmail.com', '07070340925', '$2y$10$.XRQ5OqyAoAUNJpQ1HtA1ukSJwjeczTd06d9U0134BoG75cx5cQOG', 'Customer', 0, NULL, NULL),
(95, 'Tobiloba Jimoh', 'rasheedah27@yahoo.com', '08030568186', '$2y$10$3F/pVH1pzoKJYIUr9bsK6uBzhRLig5Wy5jAO4cEEhFbm503cMtiqW', 'Customer', 0, NULL, NULL),
(96, 'Doris', 'dorisobi106@gmail.com', '09024802671', '$2y$10$.9Q0Ziitz1SWs/YQ2u1azeyAyxii8C3k1bDsEv9.2NMbn0YY3jNr2', 'Customer', 0, NULL, NULL),
(97, 'BIG-LAMBA', 'oparadivine096@gmail.com', '9122429589', '$2y$10$qTpBw6ojRlvwkz.vjJccYufE0L3lUsktGli119gPegbOPvxLCOikS', 'Customer', 0, NULL, NULL),
(98, 'Bharbie', 'osinachihope42@gmail.com', '8056151588', '$2y$10$993j0Bd2Kk9UmMhIxeQ2G.TYnAjLCvFbQhs7DljfXZyFktkLq331S', 'Customer', 0, NULL, NULL),
(99, 'Softie', 'softiebracelet@gmail.com', '09039337917', '$2y$10$r1NIb9J4mQ5RilVdrRCdwOFajzalNVN/T6PSDpbkMHpdV7xASgwP6', 'Customer', 0, NULL, NULL),
(100, 'Oluwatobi', 'oyirioluwatofunmi@gmail.com', '08058621586', '$2y$10$dwWCrqmQaw2B48N8zXtQtuJwFHFgCLBj/nqrJnuUjpDUNmIE4NLJG', 'Customer', 0, NULL, NULL),
(101, 'Shedrach nabuihe', 'shedrachnabuihe7@gmail.com', '09033124809', '$2y$10$mwPy4dnSgZ.hyAR9zf3yo.aBcK5i2rDR42FvxvYID3aKRuEI95zSi', 'Customer', 0, NULL, NULL),
(102, 'Ransom', 'favourcuzoma9@gmail.com', '07049943450', '$2y$10$bMAej.YspL3RUhXfMXT18urQrjLXU.4qyjZbWLN0gzCIXAibXWwKK', 'Customer', 0, NULL, NULL),
(103, 'Enock Mososi', 'enockmososi@gmail.com', '0701228543', '$2y$10$r1qGSVj.761kLxeSFllhdO1/1tm9M2z4ghP71KEIvr0.2VJvuHkpC', 'Customer', 0, NULL, NULL),
(104, 'Godspower', 'martinssmith414@gmail.com', '07088961646', '$2y$10$M25Qo7KI.GvvXIdbUm7UPeZasRIVMEl19yI1LzWcfMnCU9BRMJgHC', 'Customer', 0, NULL, NULL),
(105, 'Iroegbu', 'iroegbuuzo@gmail.com', '09137112139', '$2y$10$bK83WXyOgXoCO2Bcz.w4neNL1uH0buZ6bgGqqWx8glm6dBnlfPbE.', 'Customer', 0, NULL, NULL),
(106, 'Eze favour', 'ezefavourmary@gmail.com', '09161244553', '$2y$10$8bkMung8erR8DcURn4rww.hFA4POXDSf5qfwErkpD.vtrw2YFe8a2', 'Customer', 0, NULL, NULL),
(107, 'Glory', 'gloryuchechi351@gmail.com', '09113013209', '$2y$10$FTLB.7Em/ZfbglgM/eje7OKWoSpczkSaD8C7TADnrrd9nX2X70BCu', 'Customer', 0, '601dc4e36bb0aae0a2c5daee6dd43e0f', '2025-11-06 10:24:46'),
(108, 'Adeniyi Idowu John', 'adeniyiidowujohn2018@gmail.com', '08160105299', '$2y$10$hBgsSFY8lcD3QmwztxyxWemQW/EhDjvfhhKW87MWY/ip9YAOL5Tmq', 'Customer', 0, NULL, NULL),
(109, 'AREMU', 'abefemubaraq@gmail.com', '07083236580', '$2y$10$oOGyFeoVYDYJ5D76tMrV1Oc3Rx42Oje7eoYhNaGi3NmRUK14gf2ju', 'Customer', 0, NULL, NULL),
(110, 'muhammad', 'muhammadbello200426@gmail.com', '09032128594', '$2y$10$R7TC4WigdCAsdlzhw8Pia.4YqJu0wF3YurkurdDclBtGzQyHiwtoi', 'Customer', 0, NULL, NULL),
(111, 'Osas', 'osas@gmail.com', '09067426975', '$2y$10$.49RhtIAKrEXd3kufbg/tOI.dRiexi2U7t5J17E8GM1AQkvzH9nFi', 'Customer', 0, NULL, NULL),
(112, 'John', 'jfavourite22@gmail.com', '08116769885', '$2y$10$SuLuV8SlCJG0Tuk76/ZSFeP1Fo7uG7dI19L2o4y3DemDgS2FtONLu', 'Customer', 0, NULL, NULL),
(113, 'Adaeze', 'adaezealakwe2022@gmail.com', '09040995769', '$2y$10$toRE6HNbpab20L8y88dAper3U71uY/DXvO5z/1A8S.rDHQKilDeJC', 'Customer', 0, NULL, NULL),
(114, 'Eze martha', 'ezehmartha862@gmail.com', '08106498667', '$2y$10$i24uxYCgi.FeDc8OT527..CZZZDEtqFh9j3sIAtzTWStsvsGDlT1C', 'Customer', 0, NULL, NULL),
(115, 'Jonathan', 'nuellajonathan@gmail.com', '09029225336', '$2y$10$pth0WP6X6G.S5gCi.0WDberdpsGigqYVv0vShoUB5L/5/uHznqwX6', 'Customer', 0, NULL, NULL),
(116, 'Anosike Joshua', 'anosikejoshua45@gmail.com', '08123774568', '$2y$10$159bWGV.x637Y.Oqbp15XuiVlLFI48Awif0nbl34lbDySSPPrWnqK', 'Customer', 0, NULL, NULL),
(117, 'Cephas Okechukwu', 'enoughnot435@gmail.com', '08108656905', '$2y$10$O82mFQsnpWQSv03oAcSEJu5voVxYsE0hzbwTpiEPwYaE3dNn81UpO', 'Customer', 0, NULL, NULL),
(118, 'Godswill Promise', 'godswillpromise372@gmail.com', '07040013882', '$2y$10$b4QJGiuyhSvrY4sANbTxbuU5NV8y9wdy6VRSMF0liya8.nS3LCAVe', 'Customer', 0, NULL, NULL),
(119, 'Wisdom Izuchukwu Njoku', 'mhiztaziks@gmail.com', '07045443904', '$2y$10$pvBgmvkBf7w/JbQK2.oN6upI02Gn4.RZF3Y/g3/nN2gT3Xyga4VfO', 'Customer', 0, '5bc6e7962c147456db029d4194e272f2', '2026-01-06 04:29:01'),
(120, 'Levi', 'leviosuagwu70@gmail.com', '08141148246', '$2y$10$YKkwHslsoq2B7pRlLZylwuAU55zoTmw7.AXqlJ.2A9ePGVkoRqof6', 'Customer', 0, NULL, NULL),
(121, 'Marine', 'noblemarine58@gmail.com', '09064893244', '$2y$10$yLjUmljXQ727xF7Qzth3BupzHS/pyB6E2rPaQrbAACMokOq2OsB/6', 'Customer', 0, NULL, NULL),
(122, 'Chiamaka', 'nnajioforamaka9@gmail.com', '08101246749', '$2y$10$x8xphXtFEKCO4XWAik/z8.MkPOSq/GAmDC14J/dfiChVEwx/HmaUK', 'Customer', 0, NULL, NULL),
(123, 'ELVIS EKE IBE', 'elvisekeibe@gmail.com', '09012198048', '$2y$10$vdHy839cw/DZcs7CsjfmAuxJVCuYSSgIiOKGxjgi81nSWUROiTk4e', 'Customer', 0, NULL, NULL),
(126, 'Emma', 'chinedumemmanuel2004@gmail.com', '09072884466', '$2y$10$KUfONUILwAGvOqib.Phjnupub2cm1j5xjYGi5puQAOIZvnwcj/FnG', 'Customer', 0, NULL, NULL),
(127, 'KING', 'kingsleyvicktor@gmail.com', '08105236614', '$2y$10$SVnQCNa2aotfYt1IMkeT/OvugYvc3ou4DebsPkZ4UvHDjUI8VNE4e', 'Customer', 0, NULL, NULL),
(128, 'keywhese', 'dallisongude83@hotmail.com', '83415391423', '$2y$10$RCLcjmjW9DLV4.cFqccK5OEbXDJ2.phzXtK9ua0gh0hyBSDVqOvBa', 'Customer', 0, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
