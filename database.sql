DROP TABLE IF EXISTS urls, urls_checks;

CREATE TABLE urls
(
    id         BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name       VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE         NOT NULL
);

CREATE TABLE urls_checks
(
    id          BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id      BIGINT,
    status_code INTEGER,
    h1          VARCHAR(255),
    title       VARCHAR(255),
    description TEXT,
    created_at  DATE DEFAULT now(),
    CONSTRAINT "urls_checks_url_id"
        FOREIGN KEY (url_id)
            REFERENCES urls (id)
);
