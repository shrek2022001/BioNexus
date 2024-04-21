CREATE DATABASE Bionexus_db;
Use Bionexus_db;

CREATE TABLE IF NOT EXISTS articles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title TEXT,
  abstract TEXT,
  authors TEXT,
  pub_date TEXT,
  journal TEXT,
  keywords TEXT,
  doi TEXT
);


GRANT ALL PRIVILEGES ON Bionexus_db.* TO 'root'@'localhost';
SELECT * FROM articles;
SELECT * FROM articles WHERE id >= 10000 AND id <= 12000;
SELECT COUNT(*) FROM articles;




   
   DROP TABLE articles;
    DROP TABLE Author;
   DROP TABLE Keyword;
   DROP TABLE SubjectArea;
   DROP TABLE Article_Author;
   DROP TABLE Article_Keyword;
    DROP TABLE Article_SubjectArea;
    
    