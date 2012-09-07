BEGIN;

DROP SCHEMA IF EXISTS reseptiohjelma CASCADE;

CREATE SCHEMA reseptiohjelma;

SET search_path TO reseptiohjelma, "$user", public;

CREATE TABLE kohde(
       kohde_id serial PRIMARY KEY,
       tyyppi text NOT NULL CHECK (tyyppi IN ('RA', 'RE', 'AT', 'HE')),
       luotu timestamp with time zone NOT NULL DEFAULT now(),
       omistaja int REFERENCES henkilo (henkilo_id) -- Pitäisi olla NOT NULL
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
       valmistusohje text NOT NULL,
       tsv tsvector
);

CREATE INDEX resepti_tsv_gin_index ON resepti USING gin (tsv);

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
       aika timestamp with time zone NOT NULL DEFAULT NOW(),
       omistaja int REFERENCES henkilo (henkilo_id) -- Pitäisi olla NOT NULL
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

--
-- Funktioita
--

--
-- array_accum-aggregaattia tarvitaan tekstien koostamiseen tulos riveistä.
--
CREATE AGGREGATE array_accum (anyelement)
(
    sfunc = array_append,
    stype = anyarray,
    initcond = '{}'
);

--
-- Funktiota muodosta_reseptin_teksti käytetään tekstihaun lähtöaineena.
--
CREATE OR REPLACE FUNCTION muodosta_reseptin_teksti(resepti_id_in int) RETURNS text AS
$$
DECLARE
	koko_teksti_ text;
	valmistusohje_ text;
	ruokaaineet_ text;
	nimi_ text;
BEGIN
	koko_teksti_ := '';

	SELECT resepti.valmistusohje, resepti.nimi FROM resepti WHERE resepti.resepti_id = resepti_id_in INTO valmistusohje_, nimi_;

	koko_teksti_ := valmistusohje_;

	SELECT array_to_string(array_accum(rivi), E'\n')
	FROM (SELECT resepti_ruokaaine.maara
	     	    || ' ' || resepti_ruokaaine.mittayksikko
		    || ' ' || ruokaaine.nimi AS rivi
		    FROM resepti_ruokaaine
		        JOIN ruokaaine
			    ON resepti_ruokaaine.ruokaaine_id = ruokaaine.ruokaaine_id
                    WHERE resepti_ruokaaine.resepti_id = resepti_id_in
                    ORDER BY resepti_ruokaaine.jarjestys, resepti_ruokaaine.ruokaaine_id
              ) a
        INTO ruokaaineet_;

	RETURN nimi_ || E'\n\n' || COALESCE(ruokaaineet_, '') || COALESCE(E'\n\n' || valmistusohje_, '');
END
$$
LANGUAGE plpgsql STRICT;

-- SELECT muodosta_reseptin_teksti(10);

CREATE OR REPLACE FUNCTION resepti_tsv_trigger() RETURNS TRIGGER AS $$
BEGIN
	--
	-- Jos tsv-sarake ei muutu "resepti"-taulun päivityksessä,
	-- oletetaan että muutos on liipaisimen aiheuttama ja
	-- ohitetaan tapahtuma. Muuten joudumme rekursioansaan.
        --
        -- Tämän pitäisi olla riittävä, koska tsv-sarakkeesta ei
        -- pitäisi tulla syötettä reseptin tekstiin,
        -- ts. feedback-silmukka ei ole mahdollinen.
	--
	IF TG_TABLE_NAME = 'resepti' AND TG_OP = 'UPDATE' THEN
	        IF NEW.tsv IS NOT DISTINCT FROM OLD.tsv THEN
		        RETURN NEW;
                END IF;
        END IF;

	UPDATE resepti
            SET tsv = to_tsvector('pg_catalog.finnish',
	                          COALESCE(muodosta_reseptin_teksti(NEW.resepti_id), ''::text))
            WHERE resepti.resepti_id = NEW.resepti_id;

        RETURN NEW;
END
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tsvectorupdate ON resepti;
CREATE TRIGGER tsvectorupdate AFTER INSERT OR UPDATE
ON resepti FOR EACH ROW EXECUTE PROCEDURE resepti_tsv_trigger();

DROP TRIGGER IF EXISTS tsvectorupdate ON resepti_ruokaaine;
CREATE TRIGGER tsvectorupdate AFTER INSERT OR UPDATE
ON resepti_ruokaaine FOR EACH ROW EXECUTE PROCEDURE resepti_tsv_trigger();

--
-- FIXME: jos ruokaaineen nimi muuttuu, pitäisi resepti.tsv päivittää:
--        tarvitaan siis vielä yksi uusi liipaisinfunktio
--        ruokaaine-taululle.
--

COMMIT;
