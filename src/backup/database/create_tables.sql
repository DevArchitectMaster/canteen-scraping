CREATE TABLE IF NOT EXISTS "results" (
	"id"	INTEGER NOT NULL UNIQUE,
	"scrapling_timestamp"	TEXT NOT NULL,
	"intended_date"	TEXT NOT NULL,
	"courses_type"	TEXT NOT NULL,
	"label"	TEXT NOT NULL,
	"ingredients"	TEXT,
	"icons"	TEXT,
	"price_students"	REAL NOT NULL,
	"price_staff"	REAL NOT NULL,
	"price_guests"	REAL NOT NULL,
	"price_special_fare"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)