CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);

CREATE TABLE sqlite_sequence(name, seq);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE transactions (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    time_stamp NUMERIC DEFAULT CURRENT_TIMESTAMP NOT NULL,
    symbol TEXT NOT NULL,
    name TEXT NOT NULL,
    shares INTEGER NOT NULL,
    price REAL NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);