CREATE TABLE "pb_server" (
    "server_id" SERIAL PRIMARY KEY,
    "server_name" VARCHAR NULL
);
CREATE TABLE "pb_bot" (
    "bot_id" SERIAL NOT NULL,
    "bot_Name" VARCHAR NOT NULL,
    "server_id" INTEGER NOT NULL,
    PRIMARY KEY (bot_id),
    FOREIGN KEY (server_id) REFERENCES pb_server(server_id)
);
CREATE TABLE "pb_user" (
    "user_id" SERIAL PRIMARY KEY,
    "user_name" VARCHAR NULL
);
CREATE TABLE "pb_quotes" (
    "quote_id" SERIAL,
    "quotes_content" TEXT NULL,
    "quotes_date" DATE NULL,
    "quotes_author" VARCHAR NULL,
    "user_id" INTEGER NOT NULL,
    "server_id" INTEGER NOT NULL,
    PRIMARY KEY (quote_id),
    FOREIGN KEY (server_id) REFERENCES pb_server(server_id),
    FOREIGN KEY (user_id) REFERENCES pb_user(user_id)

);
CREATE TABLE "pb_permissions" (
    "perm_id" SERIAL,
    "user_id" INTEGER NOT NULL,
    "server_id" INTEGER NOT NULL,
    "perm_permission" VARCHAR NULL,
    PRIMARY KEY (perm_id),
    FOREIGN KEY (server_id) REFERENCES pb_server(server_id),
    FOREIGN KEY (user_id) REFERENCES pb_user(user_id)
);
