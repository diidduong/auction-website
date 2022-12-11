-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS bid;
DROP TABLE IF EXISTS notification;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    total_fund INTEGER DEFAULT 0 NOT NULL,
    held_fund INTEGER DEFAULT 0 NOT NULL
);


-- status 'available','bidding','sold'
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  image TEXT NOT NULL,
  price INTEGER NOT NULL,
  duration INTEGER NOT NULL,
  disabledBid INTEGER NOT NULL,
  best_ask_price INTEGER,
  best_bid_id INTEGER,
  status TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
  FOREIGN KEY (best_bid_id) REFERENCES bid (id)
);

-- status 'successful', 'outbidded', 'failed'
CREATE TABLE bid (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ask_price INTEGER NOT NULL,
  status TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (post_id) REFERENCES post (id)
);

CREATE TABLE notification (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  message TEXT,
  unread INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (post_id) REFERENCES post (id)
);

INSERT INTO user (username, password, firstname, lastname, total_fund, held_fund) VALUES
  ("testuser1", "123", "Test", "User1", "0", "0"),
  ("testuser2", "123", "Test", "User2", "0", "0"),
  ("testuser3", "123", "Test", "User3", "0", "0");

INSERT INTO post (author_id, created, title, description, image, price, duration, disabledBid, status) VALUES
  ("1", CURRENT_TIMESTAMP, "title1", "description", "image", 2500, 60, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "title1", "description", "image", 100, 120, 1, "expired"),
  ("2", CURRENT_TIMESTAMP, "title1", "description", "image", 500, 120, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "title1", "description", "image", 1000, 240, 1, "expired"),
  ("3", CURRENT_TIMESTAMP, "title1", "description", "image", 10000, 3600, 1, "expired"),
  ("2", CURRENT_TIMESTAMP, "title1", "description", "image", 1500, 30, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "title1", "description", "image", 2500, 480, 1, "expired");


