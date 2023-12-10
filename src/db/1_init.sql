CREATE DATABASE IF NOT EXISTS dice_and_die;
USE dice_and_die;

CREATE TABLE users (
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id VARCHAR(36) DEFAULT (UUID()) PRIMARY KEY UNIQUE,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL,
    is_verify BOOLEAN DEFAULT FALSE
);

CREATE TABLE ranks (
    rank_id BIGINT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE users_levels (
    user_level VARCHAR(36) DEFAULT (UUID()) PRIMARY KEY UNIQUE,
    user_id CHAR(36),
    rank_id BIGINT DEFAULT 1,
    level INTEGER DEFAULT 0,
    current_points INTEGER DEFAULT 0,
    next_level_points INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (rank_id) REFERENCES ranks(rank_id)
);

CREATE TABLE bank_accounts (
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bank_accounts VARCHAR(36) DEFAULT (UUID()) PRIMARY KEY UNIQUE,
    user_id VARCHAR(36) NOT NULL UNIQUE,
    amount DOUBLE NOT NULL DEFAULT 0
);