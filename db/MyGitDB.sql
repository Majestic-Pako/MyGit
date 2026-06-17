CREATE DATABASE IF NOT EXISTS MyGitDB
## Estos son para los caracteres especiales O-O
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE MyGitDB;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS github_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    biography TEXT,
    image_profile VARCHAR(500),
    followers INT DEFAULT 0,
    following INT DEFAULT 0,
    public_repos INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS repositories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    github_profile_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    language VARCHAR(100),
    stargazers_count INT DEFAULT 0,
    forks_count INT DEFAULT 0,
    repo_created_at DATETIME,
    last_activity_at DATETIME,
    html_url VARCHAR(500) NOT NULL,

    CONSTRAINT fk_repositories_github_profile
        FOREIGN KEY (github_profile_id)
        REFERENCES github_profiles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS search_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    github_profile_id INT NOT NULL,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50) DEFAULT 'api',
    status VARCHAR(50) DEFAULT 'success',

    CONSTRAINT fk_search_history_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_search_history_github_profile
        FOREIGN KEY (github_profile_id)
        REFERENCES github_profiles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS cache_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    github_profile_id INT NOT NULL,
    raw_data_json JSON NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    status VARCHAR(50) DEFAULT 'active',

    CONSTRAINT fk_cache_entries_github_profile
        FOREIGN KEY (github_profile_id)
        REFERENCES github_profiles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS profile_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    github_profile_id INT NOT NULL UNIQUE,
    total_repositories INT DEFAULT 0,
    total_commits INT DEFAULT 0,
    total_collaborators INT DEFAULT 0,
    most_used_language VARCHAR(100),
    most_active_repository VARCHAR(150),
    last_update DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_profile_metrics_github_profile
        FOREIGN KEY (github_profile_id)
        REFERENCES github_profiles(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_repositories_profile
ON repositories(github_profile_id);

CREATE INDEX idx_search_history_user
ON search_history(user_id);

CREATE INDEX idx_search_history_profile
ON search_history(github_profile_id);

CREATE INDEX idx_cache_entries_profile
ON cache_entries(github_profile_id);