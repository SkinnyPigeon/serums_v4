SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'source' AND pid <> pg_backend_pid();

\c postgres;

drop database source;
drop database data_vault;

create database source;
create database data_vault;

\c data_vault;
create schema zmc;
create schema fcrb;
create schema ustan;

ALTER DATABASE data_vault SET search_path TO fcrb, ustan, zmc, public, pg_catalog;

\c source;
create schema zmc;
create schema fcrb;
create schema ustan;
create schema ustan_ml;

ALTER DATABASE source SET search_path TO fcrb, ustan, ustan_ml, zmc, public, pg_catalog;


