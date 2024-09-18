CREATE DATABASE IF NOT EXISTS appBank;
USE appBank;

-- 既存のテーブルを削除する場合
DROP TABLE IF EXISTS account_info;
DROP TABLE IF EXISTS remittance_log;
DROP TABLE IF EXISTS claim_log;

CREATE TABLE account_info (
   account_num VARCHAR(10) NOT NULL,
   user_name VARCHAR(10000) NOT NULL,
   image_path VARCHAR(100) NOT NULL,
   balance DECIMAL(10, 2) NOT NULL,
   PRIMARY KEY (account_num)
);
-- 送金ログ
CREATE TABLE remittance_log (
   id INT(10) NOT NULL AUTO_INCREMENT,
   sender VARCHAR(10000) NOT NULL,
   destination VARCHAR(100) NOT NULL,
   amount DECIMAL(10, 2) NOT NULL,
   msg VARCHAR(1000),
   dateinfo DATETIME NOT NULL,
   flag BOOLEAN NOT NULL,
   PRIMARY KEY (id)
);

-- 請求ログ
CREATE TABLE claim_log (
   id INT(10) NOT NULL  AUTO_INCREMENT,
   sender VARCHAR(10000) NOT NULL,
   destination VARCHAR(100) NOT NULL,
   amount DECIMAL(10, 2) NOT NULL,
   msg VARCHAR(1000),
   dateinfo DATETIME NOT NULL,
   flag BOOLEAN NOT NULL,
   PRIMARY KEY (id)
);

-- データの挿入
INSERT INTO account_info (account_num, user_name, image_path,balance) VALUES
('123456', 'yamada tarou','human1.png', 5000.00),
('234567', 'kikuti hanako','human2.png', 10000.00),
('345678', 'ishida jirou','human3.png', 7500.00),
('456789', 'tanaka takeshi','human4.png', 15000.00),
('567890', 'wada riki','human5.png', 3000.00),
('678901', 'suzuki tarou','human6.png', 20000.00);

INSERT INTO remittance_log (sender, destination, amount, msg, dateinfo, flag) VALUES
('123456', '234567', 500.00, "hello", '2024-09-18 14:30:00', TRUE);

INSERT INTO claim_log (sender, destination, amount, msg, dateinfo, flag) VALUES
('345678', '456789', 1500.00, "thankyou", '2024-09-18 14:30:00', TRUE);

-- データの確認
SELECT * FROM account_info;
SELECT * FROM remittance_log;
SELECT * FROM claim_log;