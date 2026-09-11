CREATE ROLE shda_readonly
    LOGIN
    PASSWORD 'shda_readonly_password';

GRANT CONNECT
    ON DATABASE ai_knowledge
    TO shda_readonly;

GRANT USAGE
    ON SCHEMA public
    TO shda_readonly;

GRANT SELECT
    ON ALL TABLES
    IN SCHEMA public
    TO shda_readonly;

ALTER DEFAULT PRIVILEGES
    IN SCHEMA public
    GRANT SELECT ON TABLES
    TO shda_readonly;