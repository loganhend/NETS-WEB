-- Initialize the database.
-- Drop any existing data and create empty tables.
DROP TABLE IF EXISTS seasons;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS people;

CREATE TABLE seasons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img text unique,
  num INTEGER UNIQUE NOT NULL,
  name TEXT UNIQUE NOT NULL,
  info TEXT,
  unique (name)
);

CREATE TABLE characters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img text unique,
  name TEXT UNIQUE NOT NULL,
  played_by INTEGER UNIQUE NOT NULL,
  info TEXT,
  foreign key (played_by) references people (id),
  unique (name)
);

CREATE TABLE people (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img text unique,
  name TEXT UNIQUE NOT NULL,
  info TEXT,
  unique (name)
);

CREATE TABLE episodes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  img text unique,
  num INTEGER NOT NULL,
  name TEXT UNIQUE NOT NULL,
  date_released TEXT NOT NULL,
  season_id INTEGER NOT NULL,
  written_by TEXT UNIQUE NOT NULL,
  directed_by TEXT UNIQUE NOT NULL,
  info TEXT,
  FOREIGN KEY (season_id) references seasons (id),
  FOREIGN KEY (written_by) references people (id),
  FOREIGN KEY (directed_by) references people (id),
  unique (name)
);