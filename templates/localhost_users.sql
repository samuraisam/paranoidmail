INSERT INTO 
		domains (domain) 
	VALUES 
		('localhost'), 
		('localhost.localdomain');
INSERT INTO 
		aliases (mail, destination) 
	VALUES 
		('postmaster@localhost','root@localhost'), 
		('sysadmin@localhost','root@localhost'), 
		('webmaster@localhost','root@localhost'), 
		('abuse@localhost','root@localhost'), 
		('root@localhost','root@localhost'), 
		('@localhost','root@localhost'), 
		('@localhost.localdomain','@localhost');

INSERT INTO users (id,name,maildir,crypt) 
	VALUES ('root@localhost','root','root/',encrypt('{{password}}') );