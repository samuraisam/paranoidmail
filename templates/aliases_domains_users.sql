CREATE TABLE IF NOT EXISTS `aliases`
(
	`pkid`        SMALLINT(3) NOT NULL auto_increment,
	`mail`        VARCHAR(120) NOT NULL DEFAULT '',
	`destination` VARCHAR(120) NOT NULL DEFAULT '',
	`enabled`     TINYINT(1) NOT NULL DEFAULT '1',
	PRIMARY KEY (`pkid`),
	UNIQUE KEY `mail` (`mail`)
);  
CREATE TABLE IF NOT EXISTS `domains`
(
	`pkid`      SMALLINT(6) NOT NULL auto_increment,
	`domain`    VARCHAR(120) NOT NULL DEFAULT '',
	`transport` VARCHAR(120) NOT NULL DEFAULT 'virtual:',
	`enabled`   TINYINT(1) NOT NULL DEFAULT '1',
	PRIMARY KEY (`pkid`)
);  
CREATE TABLE IF NOT EXISTS `users`
(
	`id`              VARCHAR(128) NOT NULL DEFAULT '',
	`name`            VARCHAR(128) NOT NULL DEFAULT '',
	`uid`             SMALLINT(5) UNSIGNED NOT NULL DEFAULT '5000',
	`gid`             SMALLINT(5) UNSIGNED NOT NULL DEFAULT '5000',
	`home`            VARCHAR(255) NOT NULL DEFAULT '/var/spool/mail/virtual',
	`maildir`         VARCHAR(255) NOT NULL DEFAULT 'blah/',
	`enabled`         TINYINT(3) UNSIGNED NOT NULL DEFAULT '1',
	`change_password` TINYINT(3) UNSIGNED NOT NULL DEFAULT '1',
	`clear`           VARCHAR(128) NOT NULL DEFAULT 'ChangeMe',
	`crypt`           VARCHAR(128) NOT NULL DEFAULT 'sdtrusfX0Jj66',
	`quota`           VARCHAR(255) NOT NULL DEFAULT '',
	`procmailrc`      VARCHAR(128) NOT NULL DEFAULT '',
	`spamassassinrc`  VARCHAR(128) NOT NULL DEFAULT '',
	PRIMARY KEY (`id`),
	UNIQUE KEY `id` (`id`)
);