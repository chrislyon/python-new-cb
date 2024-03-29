
--
-- BASE DE TEST
--

use TEST;


--
-- TABLE DOSSIERS
--

DROP TABLE IF EXISTS DOSSIERS;

CREATE TABLE DOSSIERS  (
	ID int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
	DAT_CRE timestamp NOT NULL default current_timestamp COMMENT 'Date creation',
	DOSSIER INT NOT NULL COMMENT 'No de Dossier',
	BANQUE VARCHAR(5) NOT NULL COMMENT 'Code Banque',
	QTE INT NOT NULL DEFAULT 0 COMMENT 'Qte Dossier',
	NBFOLIO INT NOT NULL DEFAULT 0 COMMENT 'Nb feuillet',
	STATUT INT NOT NULL DEFAULT 0 COMMENT 'Statut du dossier',
	NB_OP INT NOT NULL DEFAULT 0 COMMENT 'Nbre operations',
	UNIQUE KEY K_DOS (DOSSIER)
	);

INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1000, 'BNP', 1000, 1, 4);
INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1001, 'CDC', 1500, 3, 2);
INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1002, 'CA', 2000, 2, 2);
INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1003, 'CIC', 8000, 3, 3);
INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1004, 'BQE', 5000, 1, 2);
INSERT INTO DOSSIERS ( DOSSIER, BANQUE, QTE, NBFOLIO, NB_OP) VALUES ( 1005, 'CDC', 2500, 1, 2);

--
-- TABLE OPERATIONS
--

DROP TABLE IF EXISTS OPERATIONS;

CREATE TABLE OPERATIONS  (
	ID int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
	DAT_CRE timestamp NOT NULL default current_timestamp COMMENT 'Date creation',
	DOSSIER INT NOT NULL COMMENT 'No de Dossier',
	OPENUM INT NOT NULL COMMENT 'No Operation',
	ETAPE INT NOT NULL default 0 COMMENT 'Etape',
	SUSPENDU INT NOT NULL default 0 COMMENT 'Suspendu O=1/N=0',
	TEMPS INT NOT NULL default 0 COMMENT 'Etape',
	DAT_DEB timestamp NOT NULL default '0000-00-00'  COMMENT 'Date debut operation',
	DAT_FIN timestamp NOT NULL default '0000-00-00'  COMMENT 'Date debut fin operation',
	POSTE VARCHAR(15) NOT NULL COMMENT 'Poste',
	UTILIS VARCHAR(15) NOT NULL default '' COMMENT 'Utilisateur',
	NUMBO1 VARCHAR(15) NOT NULL default '' COMMENT 'Bobine no1',
	NUMBO2 VARCHAR(15) NOT NULL default '' COMMENT 'Bobine no2',
	NUMBO3 VARCHAR(15) NOT NULL default '' COMMENT 'Bobine no3',
	NUMBO4 VARCHAR(15) NOT NULL default '' COMMENT 'Bobine no4',
	NUMBO5 VARCHAR(15) NOT NULL default '' COMMENT 'Bobine no5',
	CERTIF VARCHAR(15) NOT NULL default 'AUC' COMMENT 'Certification Papier',
	UNIQUE KEY K_DOS (DOSSIER, OPENUM)
	);

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1000, 1, 0, 'PLQ' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1000, 2, 0, 'CMM' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1000, 3, 0, 'RMM' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1000, 4, 0, 'ASS' );

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1001, 1, 0, 'RIS' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1001, 2, 0, 'HPL' );

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1002, 1, 0, 'RIS' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1002, 2, 0, 'HPL' );

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1003, 1, 0, 'PLQ' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1003, 2, 0, 'CMM' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1003, 3, 0, 'ASS' );

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1004, 1, 0, 'RIS' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1004, 2, 0, 'HPL' );

INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1005, 1, 0, 'RIS' );
INSERT INTO OPERATIONS ( DOSSIER, OPENUM, ETAPE, POSTE ) values ( 1005, 2, 0, 'HPL' );

CREATE OR REPLACE VIEW HISTOCB as 
	select OP.DOSSIER, OPENUM, ETAPE, UTILIS, POSTE, BANQUE, QTE, NBFOLIO, SUSPENDU, TEMPS, DAT_DEB, DAT_FIN
	from OPERATIONS OP, DOSSIERS DO
	Where OP.DOSSIER = DO.DOSSIER
	order by DOSSIER, OPENUM;

--
-- TABLE UTILIS
--

DROP TABLE IF EXISTS UTILIS;
CREATE TABLE UTILIS (
	ID int NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique ID',
	NOM VARCHAR(30) NOT NULL default '' COMMENT 'Nom Utilisateur',
	ACTIF INT NOT NULL default 0 COMMENT 'Actif O=1/N=0',
	CODE VARCHAR(5) NOT NULL default '' COMMENT 'Code User',
	UNIQUE KEY K_CODE (CODE(5))
);

INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U01', 'User 1', 1);
INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U02', 'User 2', 1);
INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U03', 'User 3', 0);
INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U04', 'User 4', 1);
INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U05', 'User 5', 0);
INSERT INTO UTILIS ( CODE, NOM, ACTIF ) values ( 'U06', 'User 6', 1);
