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
  ("1", CURRENT_TIMESTAMP, "rustic old pen", "From the 1900s", "https://images.unsplash.com/photo-1518674660708-0e2c0473e68e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTJ8fG9iamVjdHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60", 2500, 60, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "Pristine Cactus", "From Death Valley California", "https://images.unsplash.com/photo-1459411552884-841db9b3cc2a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8b2JqZWN0fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60", 100, 120, 1, "expired"),
  ("2", CURRENT_TIMESTAMP, "Classic Phone", "1980 throw back!", "https://images.unsplash.com/photo-1557180295-76eee20ae8aa?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8b2JqZWN0fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=500&q=60", 500, 120, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "Sturdy Stool", "Build with my own two hands", "https://images.unsplash.com/photo-1503602642458-232111445657?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fG9iamVjdHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=500&q=60", 1000, 240, 1, "expired"),
  ("3", CURRENT_TIMESTAMP, "Globe with no Map", "Not for the faint of heart", "https://images.unsplash.com/photo-1563219996-45f1a0ba692e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80", 10000, 3600, 1, "expired"),
  ("2", CURRENT_TIMESTAMP, "Poloroid", "Do you wan picture that will look classic even though your camera is 100 time better quality, than this is the item for you!", "https://images.unsplash.com/photo-1516962126636-27ad087061cc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80", 1500, 30, 1, "expired"),
  ("1", CURRENT_TIMESTAMP, "Herd of Blue Sheep", "It is not one but all the sheep in the phote our yours, all 6!", "https://images.unsplash.com/photo-1621863622358-c2851384f82d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=987&q=80", 2500, 480, 1, "expired");


