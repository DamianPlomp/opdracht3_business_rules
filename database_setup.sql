CREATE TABLE profile (
profile_id varchar(255) NOT NULL,
viewed_before varchar(255),
PRIMARY KEY (profile_id)
);

CREATE TABLE buid (
buid_id varchar(255) NOT NULL,
profile_id varchar(255) NOT NULL,
PRIMARY KEY (buid_id),
FOREIGN KEY (profile_id) REFERENCES profile(profile_id)
);

CREATE TABLE session (
session_id varchar(255) NOT NULL,
buid_id varchar(255) NOT NULL,
PRIMARY KEY(session_id),
FOREIGN KEY(buid_id) REFERENCES buid(buid_id)
);

CREATE TABLE product(
product_id VARCHAR(255) NOT NULL,
category_1 VARCHAR(255),
fast_mover BOOLEAN NOT NULL,
gender VARCHAR(255) NOT NULL,
PRIMARY KEY (product_id)
);

CREATE TABLE session_product (
session_id varchar(255) NOT NULL,
product_id varchar(255) NOT NULL,
FOREIGN KEY(product_id) REFERENCES product(product_id),
FOREIGN KEY(session_id) REFERENCES session(session_id)
);