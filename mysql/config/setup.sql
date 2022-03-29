CREATE TABLE db.gps_log (time BIGINT UNSIGNED, tid VARCHAR(2),lat DECIMAL(10, 8) NOT NULL, lon DECIMAL(11, 8) NOT NULL, accuracy SMALLINT UNSIGNED, at_home BOOLEAN, distance_home DOUBLE, PRIMARY KEY (time, tid));
CREATE TABLE db.test (distance_home DOUBLE, PRIMARY KEY (distance_home));
