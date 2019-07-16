-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 25, 2019 at 12:50 AM
-- Server version: 10.3.15-MariaDB
-- PHP Version: 7.3.6

Create database geek_text;
Use geek_text;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `geek_text`
--

-- --------------------------------------------------------

--
-- Table structure for table `authors`
--

CREATE TABLE `authors` (
  `AuthorID` int(11) NOT NULL,
  `AuthorName` varchar(50) DEFAULT NULL,
  `AuthorBio` varchar(10000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `authors`
--

INSERT INTO `authors` (`AuthorID`, `AuthorName`, `AuthorBio`) VALUES
(1, 'George R. R. Martin', 'Born in 1948, fantasy writer George R. R. Martin grew up in Bayonne, New Jersey. He developed a love for writing early on. His first novel, Dying of the Light, debuted in 1977. In 1996, he published his first installment of the A Song of Ice and Fire series. Martin became a best-selling author in 2005 with the fourth title A Feast for Crows and again in 2011 with the fifth A Dance with Dragons.'),
(2, 'J. K. Rowling', 'Joanne Rowling, writing under the pen names J. K. Rowling and Robert Galbraith, is a British novelist, philanthropist, film and television producer and screenwriter best known for writing the Harry Potter fantasy series.'),
(3, 'Aldous Huxley', 'Aldous Leonard Huxley was an English writer, novelist, philosopher, and prominent member of the Huxley family. He graduated from Balliol College at the University of Oxford with a first-class honours degree in English literature. The author of nearly fifty books, Huxley was best known for his novels (among them Brave New World, set in a dystopian future); for nonfiction works, such as The Doors of Perception, in which he recalls his experiences taking psychedelic drugs; and for his wide-ranging essays. Early in his career, Huxley published short stories and poetry, and edited the literary magazine Oxford Poetry. He went on to publish travel writing, film stories, satire, and screenplays. He spent the latter part of his life in the United States, living in Los Angeles from 1937 until his death.'),
(4, 'J. R. R. Tolkien', 'John Ronald Reuel Tolkien was an English writer, poet, philologist, and university professor who is best known as the author of the classic high fantasy works The Hobbit, The Lord of the Rings, and The Silmarillion.'),
(5, 'Edgar Allen Poe', 'Edgar Allan Poe was an American writer, editor, and literary critic. Poe is best known for his poetry and short stories, particularly his tales of mystery and the macabre. He is widely regarded as a central figure of Romanticism in the United States and American literature as a whole, and he was one of the country earliest practitioners of the short story. Poe is generally considered the inventor of the detective fiction genre and is further credited with contributing to the emerging genre of science fiction. He was the first well-known American writer to try to earn a living through writing alone, resulting in a financially difficult life and career.');

-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE `book` (
  `id` int(11) NOT NULL,
  `image_path` varchar(128) DEFAULT NULL,
  `title` varchar(128) DEFAULT NULL,
  `description` varchar(128) DEFAULT NULL,
  `price` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `book`
ADD authorName varchar(50);

ALTER TABLE `book`
ADD publisher varchar(128);

ALTER TABLE `book`
ADD genre varchar(32);

INSERT INTO `book` (`id`, `publisher`, `genre`, `image_path`, `title`, `authorName`, `description`, `price`) VALUES
(1, 'Bantam Spectra', 'Fantasy', 'https://github.com/GustavoPT/GeekTextImages/blob/master/cover_gameofthrones01.jpg?raw=true', 'A Game of Thrones', 'George R. R. Martin', 'A Game of Thrones is the first novel in A Song of Ice and Fire, a series of fantasy novels', '19.99'),
(2, 'Bloomsbury', 'Fantasy', 'https://github.com/GustavoPT/GeekTextImages/blob/master/HP_SS.jpg?raw=true','Harry Potter and the Sorcerer''s Stone', 'J. K. Rowling', 'Harry finds himself drawn deep inside a mystical world he never knew existed and closer to his own noble destiny.','9.99'),
(3, 'Chatto & Windus', 'Science Fiction', 'https://github.com/GustavoPT/GeekTextImages/blob/master/BNW.jpg?raw=true','Brave New World', 'Aldous Huxley', 'masterpiece ... one of the most prophetic dystopian works of the 20th century.','14.99'),
(4, 'Allen & Unwin', 'Fantasy', 'https://github.com/GustavoPT/GeekTextImages/blob/master/TFotR.jpg?raw=true','The Fellowship of the Ring', 'J. R. R. Tolkien', 'The first volume in J.R.R. Tolkien''s epic adventure THE LORD OF THE RINGS', '11.99'),
(5, 'Simon & Schuster', 'Mystery', 'https://github.com/GustavoPT/GeekTextImages/blob/master/EAP.jpg?raw=true','Edgar Allan Poe: Complete Tales and Poems', 'Edgar Allan Poe', 'His complete early and miscellaneous poetic masterpieces.', '10.99');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `BookID` int(11) NOT NULL,
  `BookTitle` varchar(255) DEFAULT NULL,
  `BookDescription` varchar(10000) DEFAULT NULL,
  `AuthorID` int(11) DEFAULT NULL,
  `PublisherID` int(11) DEFAULT NULL,
  `ReleaseDate` date DEFAULT NULL,
  `Genre` varchar(20) DEFAULT NULL,
  `Price` decimal(16,2) DEFAULT NULL,
  `BookCover` varchar(200) DEFAULT NULL,
  `BookRating` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




-- --------------------------------------------------------

--
-- Table structure for table `book_copies`
--

CREATE TABLE `book_copies` (
  `user_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `book_genres`
--

CREATE TABLE `book_genres` (
  `BookGenreID` int(11) NOT NULL,
  `Genre` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `book_genres`
--

INSERT INTO `book_genres` (`BookGenreID`, `Genre`) VALUES
(1, 'Science fiction'),
(2, 'Satire'),
(3, 'Drama'),
(4, 'Action and Adventure'),
(5, 'Romance'),
(6, 'Mystery'),
(7, 'Horror'),
(8, 'Self help'),
(9, 'Health'),
(10, 'Guide'),
(11, 'Travel'),
(12, 'Children'),
(13, 'Religion, Spirituality & New Age'),
(14, 'Science'),
(15, 'History'),
(16, 'Math'),
(17, 'Anthology'),
(18, 'Poetry'),
(19, 'Encyclopedias'),
(20, 'Dictionaries'),
(21, 'Comics'),
(22, 'Art'),
(23, 'Cookbooks'),
(24, 'Diaries'),
(25, 'Journals'),
(26, 'Prayer books'),
(27, 'Series'),
(28, 'Trilogy'),
(29, 'Biographies'),
(30, 'Autobiographies'),
(31, 'Fantasy');

-- --------------------------------------------------------

--
-- Table structure for table `book_ratings`
--

CREATE TABLE `book_ratings` (
  `BookRatingID` int(11) NOT NULL,
  `BookID` int(11) DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL,
  `Rating` int(11) DEFAULT NULL,
  `Comment` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `publishers`
--

CREATE TABLE `publishers` (
  `PublisherID` int(11) NOT NULL,
  `PublisherName` varchar(255) DEFAULT NULL,
  `PublisherDescription` varchar(10000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `publishers`
--

INSERT INTO `publishers` (`PublisherID`, `PublisherName`, `PublisherDescription`) VALUES
(1, 'Bantam Spectra', 'Bantam Spectra is an American publishing house owned entirely by parent company Random House, a subsidiary of Penguin Random House; it is an imprint of the Random House Publishing Group. Well known for publishing the Game of Thrones books.'),
(2, 'Bloomsbury Publishing', 'Bloomsbury Publishing is a leading independent publishing house established in 1986. It has companies in London, New York, Sydney and New Delhi.');

-- --------------------------------------------------------

--
-- Table structure for table `saveforlater`
--

CREATE TABLE `saveforlater` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `UserName` varchar(50) NOT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Hash` varchar(2000) DEFAULT NULL,
  `Salt` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_cards`
--

CREATE TABLE `user_cards` (
  `UserID` int(11) NOT NULL,
  `CreditCardNum` int(11) NOT NULL,
  `ExpMonth` int(11) NOT NULL,
  `ExpYear` int(11) NOT NULL,
  `NameOnCard` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_detail`
--

CREATE TABLE `user_detail` (
  `UserID` int(11) NOT NULL,
  `RealName` varchar(50) DEFAULT NULL,
  `HomeAddr` varchar(255) DEFAULT NULL,
  `HomeCity` varchar(2000) DEFAULT NULL,
  `HomeState` varchar(2000) DEFAULT NULL,
  `HomeZIP` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_purchased`
--

CREATE TABLE `user_purchased` (
  `UserID` int(11) NOT NULL,
  `BookID` int(11) NOT NULL,
  `DatePurchased` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user_shippings`
--

CREATE TABLE `user_shippings` (
  `UserID` int(11) NOT NULL,
  `ShippingAddr` varchar(255) NOT NULL,
  `ShippingCity` varchar(2000) NOT NULL,
  `ShippingState` varchar(2000) NOT NULL,
  `ShippingZIP` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`AuthorID`);

--
-- Indexes for table `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`BookID`),
  ADD KEY `FK` (`AuthorID`,`PublisherID`);

--
-- Indexes for table `book_copies`
--
ALTER TABLE `book_copies`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `book_genres`
--
ALTER TABLE `book_genres`
  ADD PRIMARY KEY (`BookGenreID`);

--
-- Indexes for table `book_ratings`
--
ALTER TABLE `book_ratings`
  ADD PRIMARY KEY (`BookRatingID`),
  ADD KEY `FK` (`BookID`,`UserID`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `publishers`
--
ALTER TABLE `publishers`
  ADD PRIMARY KEY (`PublisherID`);

--
-- Indexes for table `saveforlater`
--
ALTER TABLE `saveforlater`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`,`UserName`);

--
-- Indexes for table `user_cards`
--
ALTER TABLE `user_cards`
  ADD PRIMARY KEY (`UserID`,`CreditCardNum`);

--
-- Indexes for table `user_detail`
--
ALTER TABLE `user_detail`
  ADD PRIMARY KEY (`UserID`);

--
-- Indexes for table `user_purchased`
--
ALTER TABLE `user_purchased`
  ADD PRIMARY KEY (`BookID`,`UserID`);

--
-- Indexes for table `user_shippings`
--
ALTER TABLE `user_shippings`
  ADD PRIMARY KEY (`UserID`,`ShippingAddr`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `book`
--
ALTER TABLE `book`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `book_ratings`
--
ALTER TABLE `book_ratings`
  MODIFY `BookRatingID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `saveforlater`
--
ALTER TABLE `saveforlater`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `book_copies`
--
ALTER TABLE `book_copies`
  ADD CONSTRAINT `book_copies_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `book_copies_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);

--
-- Constraints for table `category`
--
ALTER TABLE `category`
  ADD CONSTRAINT `category_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `book` (`id`);

--
-- Constraints for table `saveforlater`
--
ALTER TABLE `saveforlater`
  ADD CONSTRAINT `saveforlater_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `saveforlater_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
