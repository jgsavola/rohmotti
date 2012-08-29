BEGIN;

DROP SCHEMA IF EXISTS reseptiohjelma CASCADE;

CREATE SCHEMA reseptiohjelma;

SET search_path TO reseptiohjelma, "$user", public;

CREATE TABLE kohde(
       kohde_id serial PRIMARY KEY,
       tyyppi text NOT NULL CHECK (tyyppi IN ('RA', 'RE', 'AT', 'HE'))
);

CREATE FUNCTION luo_uusi_kohde(text) RETURNS int AS
$$
    INSERT INTO kohde (kohde_id, tyyppi) VALUES (DEFAULT, $1) RETURNING kohde_id
$$
LANGUAGE SQL VOLATILE STRICT;

CREATE TABLE ruokaaine(
       ruokaaine_id int PRIMARY KEY REFERENCES kohde (kohde_id) DEFAULT luo_uusi_kohde('RA'),
       nimi text NOT NULL UNIQUE
);

CREATE FUNCTION hae_ruokaaine_id(nimi text) RETURNS int AS
$$
	SELECT ruokaaine_id FROM ruokaaine WHERE nimi = $1
$$
LANGUAGE SQL VOLATILE STRICT;

INSERT INTO ruokaaine (nimi) VALUES
       ('vehnäjauho'),
       ('maito'),
       ('kananmuna'),
       ('suola'),
       ('sokeri'),
       ('leivinjauhe'),
       ('vaniljasokeri'),
       ('öljy'),
       ('peruna')
;

CREATE TABLE resepti(
       resepti_id int PRIMARY KEY REFERENCES kohde (kohde_id) DEFAULT luo_uusi_kohde('RE'),
       nimi text NOT NULL UNIQUE,
       valmistusohje text NOT NULL
);

CREATE FUNCTION hae_resepti_id(nimi text) RETURNS int AS
$$
	SELECT resepti_id FROM resepti WHERE nimi = $1
$$
LANGUAGE SQL VOLATILE STRICT;

INSERT INTO resepti (nimi, valmistusohje) VALUES ('Lätyt', 'Vatkaa
       munien rakenne rikki, lisää muut aineet ja anna taikinan
       turvota hetki. Paista isoja lättyjä paistinpannulla rasvassa.
       Jos paistat pieniä lättyjä lettupannulla, lisää vajaa dl
       vehnäjauhoja. Tämä taikina käy myös vohveleidentekoon
       vohveliraudalla.

       Tarjoile lätyt kermavaahdon sekä hillon kera.'),
       ('Pannukakku', 'Valmista pannukakku.');

CREATE TABLE mittayksikko(
       nimi text PRIMARY KEY,
       tyyppi text NOT NULL CHECK ( tyyppi IN ('tilavuus', 'lukumäärä', 'massa') ),
       perusyksikko text NOT NULL,
       kerroin numeric NOT NULL
);

INSERT INTO mittayksikko (nimi, tyyppi, perusyksikko, kerroin) VALUES
       ('ml', 'tilavuus', 'litra', 0.001),
       ('cl', 'tilavuus', 'litra', 0.01),
       ('dl', 'tilavuus', 'litra', 0.1),
       ('l',  'tilavuus', 'litra', 1),
       ('tl', 'tilavuus', 'litra', 0.005),
       ('rkl', 'tilavuus', 'litra', 0.015),
       ('kpl', 'lukumäärä', 'yksi', 1),
       ('tiu', 'lukumäärä', 'yksi', 20),
       ('kg', 'massa', 'kg', 1),
       ('g', 'massa', 'kg', 0.001)
;

CREATE TABLE resepti_ruokaaine(
       jarjestys int NOT NULL,
       resepti_id int NOT NULL REFERENCES resepti (resepti_id),
       ruokaaine_id int NOT NULL REFERENCES ruokaaine (ruokaaine_id),
       maara numeric,
       mittayksikko text REFERENCES mittayksikko (nimi),
       PRIMARY KEY (jarjestys, resepti_id)
);

INSERT INTO resepti_ruokaaine (jarjestys, resepti_id, ruokaaine_id, maara, mittayksikko) VALUES
       (1, hae_resepti_id('Lätyt'), hae_ruokaaine_id('kananmuna'), 4, 'kpl'),
       (2, hae_resepti_id('Lätyt'), hae_ruokaaine_id('maito'), 5, 'dl'),
       (3, hae_resepti_id('Lätyt'), hae_ruokaaine_id('vehnäjauho'), 2.5, 'dl'),
       (4, hae_resepti_id('Lätyt'), hae_ruokaaine_id('suola'), 1, 'tl'),
       (5, hae_resepti_id('Lätyt'), hae_ruokaaine_id('öljy'), 1, 'rkl'),
       (6, hae_resepti_id('Lätyt'), hae_ruokaaine_id('peruna'), 1, 'rkl')
;

CREATE TABLE ateria(
       ateria_id serial PRIMARY KEY,
       kohde_id int NOT NULL REFERENCES kohde (kohde_id) DEFAULT luo_uusi_kohde('AT'),
       aika timestamp with time zone NOT NULL
);

CREATE TABLE kommentti(
       kommentti_id serial PRIMARY KEY,
       kohde_id int NOT NULL REFERENCES kohde (kohde_id),
       teksti text,
       kuva bytea,
       aika timestamp with time zone NOT NULL DEFAULT NOW()
);

CREATE TABLE henkilo(
       henkilo_id int PRIMARY KEY REFERENCES kohde (kohde_id) DEFAULT luo_uusi_kohde('HE'),
       nimi text NOT NULL,
       tunnus text NOT NULL UNIQUE,
       salasana text NOT NULL
);
       
CREATE TABLE rajoitus(
       ruokaaine_id int NOT NULL REFERENCES ruokaaine (ruokaaine_id),
       henkilo_id int NOT NULL REFERENCES henkilo (henkilo_id),
       rajoitus text NOT NULL
);

COMMIT;
