-- this is a jija2 template

CREATE DATABASE IF NOT EXISTS maildb;

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
	ON maildb.*
	TO 'mail'@'localhost' IDENTIFIED BY '{{password}}';

GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
	ON maildb.*
	TO 'mail'@'%' IDENTIFIED BY '{{password}}';
