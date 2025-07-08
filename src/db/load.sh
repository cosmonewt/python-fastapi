#!/bin/sh

# Load creature and explorer tables
# from their psv text files.
# Destroys any existing creature or explorer tables.

sqlite3 cryptid.db <<EOF
DROP TABLE creature;
DROP TABLE explorer;
DROP TABLE user;
DROP TABLE xuser;
CREATE TABLE creature (
    name TEXT PRIMARY KEY,
    country TEXT,
    area TEXT,
    description TEXT,
    aka TEXT
);
CREATE TABLE explorer (
    name TEXT PRIMARY KEY,
    country TEXT,
    description TEXT
);
CREATE TABLE user (
    name TEXT PRIMARY KEY,
    hash TEXT
);
CREATE TABLE xuser (
    name TEXT PRIMARY KEY,
    hash TEXT
);
.mode list
.import creature.psv creature
.import explorer.psv explorer
EOF
