CREATE TABLE IF NOT EXISTS user (
	pk_user_id INT auto_increment PRIMARY KEY,
    username varchar(50),
    token varchar(100), -- todo
    game_name varchar(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

CREATE TABLE IF NOT EXISTS user_info (
	pk_user_info_id INT auto_increment PRIMARY KEY,
    attribute_name varchar(50),
    info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_user_id INT,
    FOREIGN KEY (fk_user_id) REFERENCES user(pk_user_id)
);

CREATE TABLE IF NOT EXISTS play_session (
	pk_play_session_id INT auto_increment PRIMARY KEY,
    fk_user_id INT,
    FOREIGN KEY (fk_user_id) REFERENCES user(pk_user_id)
);

CREATE TABLE IF NOT EXISTS play_session_start (
	pk_play_session_start_id INT auto_increment PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_play_session_id INT,
    FOREIGN KEY (fk_play_session_id) REFERENCES play_session(pk_play_session_id)
);

CREATE TABLE IF NOT EXISTS play_session_continue (
	pk_play_session_continue_id INT auto_increment PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_play_session_id INT,
    FOREIGN KEY (fk_play_session_id) REFERENCES play_session(pk_play_session_id)
);

CREATE TABLE IF NOT EXISTS play_session_end (
	pk_play_session_end_id INT auto_increment PRIMARY KEY,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_play_session_id INT,
    FOREIGN KEY (fk_play_session_id) REFERENCES play_session(pk_play_session_id)
);

CREATE TABLE IF NOT EXISTS play_action (
	pk_play_action_id INT auto_increment PRIMARY KEY,
	action_name varchar(100),
    info TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_user_id INT,
    fk_play_session_id INT,
    FOREIGN KEY (fk_user_id) REFERENCES user(pk_user_id),
    FOREIGN KEY (fk_play_session_id) REFERENCES play_session(pk_play_session_id)
);

CREATE TABLE IF NOT EXISTS independent_point (
	pk_independent_point_id INT auto_increment PRIMARY KEY,
    attribute_name varchar(50),
    info TEXT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_user_id INT,
    FOREIGN KEY (fk_user_id) REFERENCES user(pk_user_id)
);

CREATE TABLE IF NOT EXISTS dependent_point (
    pk_dependent_point_id INT AUTO_INCREMENT PRIMARY KEY,
    attribute_name varchar(50),
    info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fk_user_id INT,
    FOREIGN KEY (fk_user_id) REFERENCES user (pk_user_id)
);


