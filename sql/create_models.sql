CREATE TABLE IF NOT EXISTS models (
    id      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title   TEXT NOT NULL,
    car     TEXT NOT NULL,
    slug    TEXT,
    FOREIGN KEY (car) REFERENCES cars(carsid)
);