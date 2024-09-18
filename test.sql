CREATE DATABASE IF NOT EXISTS appBank;
USE appBank;

-- 既存のテーブルを削除する場合
DROP TABLE IF EXISTS account_info;

CREATE TABLE account_info (
   account_num VARCHAR(10) NOT NULL,
   user_name VARCHAR(10000) NOT NULL,
   image_path VARCHAR(100) NOT NULL,
   balance DECIMAL(10, 2) NOT NULL,
   PRIMARY KEY (account_num)
);



-- データの挿入
INSERT INTO account_info (account_num, user_name, image_path,balance) VALUES
('123456', 'yamada tarou','human1.png', 5000.00),
('234567', 'kikuti hanako','human2.png', 10000.00),
('345678', 'ishida jirou','human3.png', 7500.00),
('456789', 'tanaka takeshi','human4.png', 15000.00),
('567890', 'wada riki','human5.png', 3000.00),
('678901', 'suzuki tarou','human6.png', 20000.00);

-- データの確認
SELECT * FROM account_info;