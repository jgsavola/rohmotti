BEGIN;

DROP SCHEMA IF EXISTS reseptiohjelma CASCADE;

CREATE SCHEMA reseptiohjelma;

SET search_path TO reseptiohjelma, "$user", public;

CREATE TABLE ruokaaine(
       nimi text PRIMARY KEY
);

INSERT INTO ruokaaine (nimi) VALUES
       ('vehnäjauho'),
       ('maito'),
       ('kananmuna'),
       ('suola'),
       ('sokeri'),
       ('leivinjauhe'),
       ('vaniljasokeri'),
       ('öljy');

CREATE TABLE ruokalaji(
       nimi text PRIMARY KEY,
       valmistusohje text NOT NULL
);

INSERT INTO ruokalaji (nimi, valmistusohje) VALUES
       ('Lätyt', 'Vatkaa munien rakenne rikki, lisää muut aineet ja anna taikinan turvota hetki. Paista isoja lättyjä paistinpannulla rasvassa.Jos paistat pieniä lättyjä lettupannulla, lisää vajaa dl vehnäjauhoja.Tämä taikina käy myös vohveleidentekoon vohveliraudalla.

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

CREATE TABLE ruokalaji_ruokaaine(
       jarjestys int NOT NULL,
       ruokalaji text NOT NULL REFERENCES ruokalaji (nimi),
       ruokaaine text NOT NULL REFERENCES ruokaaine (nimi),
       maara numeric,
       mittayksikko text REFERENCES mittayksikko (nimi),
       PRIMARY KEY (jarjestys, ruokalaji)
);

INSERT INTO ruokalaji_ruokaaine (jarjestys, ruokalaji, ruokaaine, maara, mittayksikko) VALUES
       (1, 'Lätyt', 'kananmuna', 4, 'kpl'),
       (2, 'Lätyt', 'maito', 5, 'dl'),
       (3, 'Lätyt', 'vehnäjauho', 2.5, 'dl'),
       (4, 'Lätyt', 'suola', 1, 'tl'),
       (5, 'Lätyt', 'öljy', 1, 'rkl');
       
COMMIT;
