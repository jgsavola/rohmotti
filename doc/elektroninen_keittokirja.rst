========================
Elektroninen keittokirja
========================

.. contents:: Sisällysluettelo

.. raw:: pdf

  PageBreak

1. Johdanto
***********

Elektroninen keittokirja on websovellus, jonka avulla ylläpidetään
tietokantaa ruoka-aineista, resepteistä ja aterioista sekä
henkilöistä, jotka ovat aterioille osallistuneet. Elektronisen
keittokirjan avulla on mahdollista tehdä ruoka-aineisiin, resepteihin,
aterioihin ja henkilöihin kohdistuvia hakuja. Sovelluksella voi myös
tehdä ostoslistan reseptin tai aterian perusteella. Resepti koostuu
ruoka-ainelistasta ja valmistusohjeesta. Ateria sisältää yhden tai
useamman reseptin ja mahdolliset ruokajuomat. Ateriaan liittyy myös
aika, paikka ja aterialle osallistuneet henkilöt — yhtenä tavoitteena
onkin olla tarjoamatta vahingossa samaa ruokalajia useampaan kerran
samalle henkilölle! Henkilöihin voi liittää tietoja rajoituksista
kuten ruokavalioista tai ruoka-aineallergioista. Lisäksi eri
kohteisiin on mahdollista liittää valokuvia ja kommentteja.

Ympäristö
---------

Ohjelma toteutetaan Python-ohjelmointikielellä CGI-ympäristössä.
Tietokantajärjestelmänä käytetään PostgreSQL:ää.

Ohjelman rakenne toteutetaan käyttäen Model-View-Controller-tyyliä.

Järjestelmän käyttäminen edellyttää tunnistautumista. Tunnistautunut
käyttäjä saa sessioavaimen, joka on voimassa määrätyn ajan
tunnistautumisesta (tai viimeisestä käyttäjän toiminnosta).

Tietokantakyselyjen muodostaminen tehdään niin, että kaikkea
käyttäjältä peräisin olevaa tietoa käsitellään huolellisesti. Tämä
tarkoittaa mm. järjestelmällistä parametroitujen kyselyjen hyödyntämistä.

Hakutoiminnoissa hyödynnetään PostgreSQL:n Full Text Search
-ominaisuutta.

Ohjelman riippuvuudet ovat tarkoituksellisesti minimaaliset:
PostgreSQL, Python + standardimodulit, Psycopg2, PyCrypto.


2. Yleiskuva järjestelmästä
***************************

3. Käyttötapaukset
******************

a)  raaka-aineen syöttö ja muutos

b)  reseptin kirjaus ja korjaus

c)  reseptin haku

d)  reseptien katselu

e)  ostoslistan teko valitun reseptin tai ateriakokonaisuuden perusteella

f)  henkilöiden syöttö ja muutos

g)  käyttäjien hallinta


4. Järjestelmän tietosisältö
****************************

.. image:: kuvat/kasitekaavio_luonnos.jpg

5. Relaatiotietokantakaavio
***************************

.. image:: dbdoc/rohmotti.png

6. Järjestelmän komponentit
***************************

6.1. Pääohjelma
---------------

rohmotti.py
    Sovelluksen CGI-standardia tukeva pääohjelma, joka on vastuussa
    CGI-parametrien tulkitsemisesta ja oikean modulin lataamisesta ja
    suorittamisesta.

6.2. Tietokanta-abstraktio
--------------------------

db/DatabaseObject.py
    Tietokantaoliomallin pääluokka, joka huolehtii lähinnä
    tietokantayhteysolion säilyttämisestä luokka-attribuuttina.

db/SimpleDatabaseObject.py
    Yksinkertainen tietokanta-abstraktio, joka huolehtii SQL-lauseiden
    muodostamisesta ja suorittamisesta. SimpleDatabaseObject tukee
    INSERT, UPDATE, DELETE ja SELECT-operaatioita yksinkertaisten
    rajapintojen kautta. Periytyvien luokkien attribuutit tuotetaan
    dynaamisesti käyttäen Pythonin metaluokkafunktioita getattr-
    ja setattr.

db/Kohde.py
    SimpleDatabaseObject-luokasta periytyvä abstraktio
    kaikille tauluille, joiden pääavaimesta on viittaus
    "kohde"-tauluun. Tämä luokka auttaa "kohde"-taulun
    tietojen lukemissa ja päivittämisessä atomisesti varsinaisen
    taulun kanssa.

db/Mittayksikko.py
    SimpleDatabaseObject-luokasta periytyvä abstraktio
    "mittayksikko"-taululle.

db/Kommentti.py
    SimpleDatabaseObject-luokasta periytyvä abstraktio
    "kommentti"-taululle. Tässä luokassa on ylikirjoitettu joitakin
    metodeja bytea-muotoisen kuva-sarakkeen tukemiseksi.

db/Rajoitus.py
    SimpleDatabaseObject-luokasta periytyvä abstraktio
    "rajoitus"-taululle.

db/Ruokaaine.py
    Kohde-luokasta periytyvä abstraktio "ruokaaine"-taululle.

db/Resepti.py
    Kohde-luokasta periytyvä abstraktio "resepti"-taululle.

db/Ateria.py
    Kohde-luokasta periytyvä abstraktio "ateria"-taululle.

db/Henkilo.p
    Kohde-luokasta periytyvä abstraktio "henkilo"-taululle.

db/ReseptiRuokaaine.py
    DatabaseObject-luokasta periytyvä abstraktio liitostaululle
    "resepti_ruokaaine". Pitäisi päivittää SimpleDatabaseObject:ksi.

db/test_mittayksikko.py
    Testiohjelma "mittayksikko"-luokalle.

db/test_reseptiruokaaine.py
    Testiohjelma "reseptiruokaaine"-luokalle.

db/test_resepti2.py
    Testiohjelma "Resepti"-luokalle.

db/test_resepti.py
    Testiohjelma "Resepti"-luokalle.

db/test_ruokaaine.py
    Testiohjelma "Ruokaaine"-luokalle.

db/test_kommentti.py
    Testiohjelma "Kommentti"-luokalle.

6.3. HTTP-pyynnön käsittelyluokkia
----------------------------------

webapp/handlers/basehandler.py
    Perusluokka BaseHandler HTTP-pyynnön käsittelyyn. Sisältää lähinnä
    alustuksen ja redirect_after_post-apumetodin.

webapp/handlers/basehandlerwithsession.py
    BaseHandler-luokasta periytyvä BaseHandlerWithSession lisää
    sessio-attribuutin ja authorized-metodin pääsynhallintaan.

webapp/handlers/kirjautuminen.py
    Kirjautumis-kyselyjen käsittelijä. Huolehtii käyttäjän
    tunnistautumisesta, uusien käyttäjien (henkilöiden) ja
    istuntoevästeiden luomisesta.

webapp/handlers/rajoitus.py
    Rajoitus-kyselyjen käsittelijä. Toteutettuna tällä hetkellä vain
    POST ja DELETE.

webapp/handlers/henkilo.py
    Henkilö-kyselyjen käsittelijä. Huolehtii henkilökohtaisten
    rajoitusten lisäämisen käyttöliittymästä ja henkilölistan ja
    henkilökohtaisten sivujen luomisesta.

webapp/handlers/haku.py
    Haku-kyselyjen käsittelijä. Huolehtii hakulomakkeen tuottamisesta,
    tekee tietokantaan tekstihakuja ja luo hakutulossivun.

webapp/handlers/kuva.py
    Kuva-kyselyjen käsittelijä. Hakee GET-kyselyllä tietokannasta
    kuvan "kommentti"-taulusta ja tulostaa sen sellaisenaan. Ei tuota
    lomakkeita eikä HTML:ää.

webapp/handlers/resepti_1.py
    Resepti-kohtaisten kyselyjen käsittelijä ja resepti-sivun
    tuottaja. Huolehtii ruoka-aineiden lisäämisestä resepteihin ja
    resepti-kohtaisten kommenttien lomakkeesta.

webapp/handlers/kommentti.py
    Kommenttikyselyjen käsittelijä. Vastaanottaa kommenttien lisäys-
    ja poistopyyntöjä, mutta ei luo sivuja.

webapp/handlers/reseptiruokaaine.py
    Reseptin ruoka-aine -kyselujen käsittelijä. Huolehtii
    ruoka-aineiden lisäämisestä ja poistamisesta resepteissä.

webapp/handlers/ruokaaine.py
    Ruoka-aine-kyselyjen käsittelijä. Huolehtii ruoka-ainelistauksen
    näyttämisestä ja ruoka-aineen lisäys-lomakkeen tuottamisesta.

webapp/handlers/resepti.py
    Resepti-kyselyjen käsittelijä. Huolehtii reseptilistauksen
    näyttämisestä ja reseptin lisäys-lomakkeen tuottamisesta.

webapp/handlers/ruokaaine_1.py
    Ruoka-ainekohtaisten kyselyjen käsittelijä. Huolehtii
    ruoka-aineisiin liittyvien rajoitusten lomakkeesta, ruoka-aineiden
    poistamisesta ja ruoka-ainekohtaisen kommenttilomakkeen tuottamisesta.

6.4. Apuluokkia
---------------

util/salasana.py
    Apuluokka suolallisen SHA1-tarkistussumman tuottamiseen. Käytetään
    salasanojen tietokantaan tallentamiseen.

util/salaus.py
    Apuluokka AES-salakirjoitukseen, jota käytetään salakirjoitettujen
    istuntoevästeiden salaamiseen ja purkamiseen. Salatekstin alkuun
    liitetään satunnainen 16-tavuinen alustusvektori.

util/sessio.py
    Apuluokka salakirjoitetun istuntoevästeen koodaamiseen ja
    purkamiseen. Tässä versiossa istunnon tilatieto on kokonaisuudessaan
    salakirjoitetussa evästeessä. Tilatieto sisältää vain käyttäjän
    IP-osoitteen, henkilo_id:n ja evästeen luomisen aikaleiman.
    Evästeen ainoa tarkoitus on tunnistaa kirjautunut käyttäjä
    istuntokohtaisesti.

util/html_parser.py
    Apuluokka HTML-tekstin suodattamiseen niin, että hyväksytään vain
    määrätyt HTML-tagit. Käytetään käyttäjän syötteen suodattamiseen
    niin, että käyttäjällä on käytössä tietyt turvalliset HTML-tagit.

6.5. Muut
---------

html_templates/
    HTML-mallineet käyttöliittymän sivujen pohjaksi. Käytössä on 
    Pythonin string.Templaten tukemat tekstinkorvaustavat.

static/images/
    Käyttöliittymän kuvat.

static/styles/
    Käyttöliittymän CSS-tyyli.

sql/
    Tietokannan koodi.

doc/
    Projektin dokumentaatio.


7. Käyttöliittymä
*****************

.. figure:: kayttoliittyma.png
    :alt: Käyttöliittymän siirtymät.

    Käyttöliittymän siirtymät.

.. figure:: rest-operaatiot.png
    :alt: Käyttöliittymän toiminnot / REST-operaatiot

    Käyttöliittymän toiminnot / REST-operaatiot


8. Asennustiedot
****************

8.0. Vaatimukset
----------------

Rohmotilla on seuraavat vaatimukset:

* Linux / \*NIX (testattu Debian, Ubuntu)
* PostgreSQL 8.4+ (testattu PostgreSQL 8.4, 9.1)
* Python 2.6+ (testattu Python 2.7)
* psycopg2 (Debianissa tai Ubuntussa paketti python-psycopg2)
* WWW-palvelin, jolla voi ajaa CGI-ohjelmia (testattu Apache 2.X)


8.1. Lähdekoodi
---------------

Pura toimituspaketti tai hae koodi gitistä::

    git clone git://github.com/jgsavola/rohmotti.git

8.2. Tietokanta
---------------

Rohmotti toimii PostgreSQL:n versiossa 8.4 tai uudemmassa (testattu
9.1). Asennuksen kohteena olevassa tietokannassa pitää olla
asennettuna "plpgsql"-kieli::

    CREATE LANGUAGE plpgsql;

Rohmotin tietokantaosat asennetaan kokonaisuudessaan omaan kaavioon
(schema), joten sen voi asentaa olemassa olevaan tietokantaan ilman
että se häiritsee muiden sovellusten toimintaa. Oletuskaavio on
"rohmotti", mutta tämän voi muuttaa.

PostgreSQL samalla koneella (socket-yhteys, ident-autentikaatio,
oletustietokanta, oletuskäyttäjä, oletusportti)::

    psql --quiet --set ON_ERROR_STOP=1 -f sql/db.sql

PostgreSQL verkossa (TCP/IP-yhteys)::

    psql --quiet --set ON_ERROR_STOP=1 -h dbhost -p dbport -U dbuser -d dbname -f sql/db.sql

Jos tulee virheitä, kannattaa ottaa --quiet pois ja yrittää uudelleen.
Asennus tehdään yhden transaktion sisällä ja on idempotentti (*varo!
asennus hävittää olemassa olevan kaavion kaikkine tietoineen*).

Jos haluat muuttaa oletuskaaviota, vaihda kaavion nimet db.sql:n
ensimmäisillä riveillä. *Huom! muista muuttaa "search_path" myös
rohmotti.py:ssä.*

Rohmotin tietokantafunktiot toimivat vain, jos (sessiokohtaisessa)
"search_path"-asetuksessa on Rohmotin asennuskaavio::

    SET search_path TO rohmotti, "$user", public;

Pysyvä, tietokantakohtainen asetus::

    ALTER DATABASE dbname SET search_path TO rohmotti, "$user", public;

8.3. WWW-sovellus
-----------------

Rohmotin tämä versio toimii pelkästään CGI-ohjelmana. Rohmotissa on
vain yksi CGI-ohjelma, rohmotti.py.

CGI-ohjelman voi asentaa monella tavalla. Jos käytössä on Apache,
yksinkertainen tapa on tehdä uusi hakemisto (WWWDIR) johonkin Apachen
palvelemaan hakemistoon ja luoda samaan hakemistoon
.htaccess-tiedosto::

    ASENNUSHAKEMISTO=/src/rohmotti
    WWWDIR=/joku/hakemisto/rohmotti
    
    mkdir -p $WWWDIR
    echo "AddHandler cgi-script py" >$WWWDIR/.htaccess
    cp $ASENNUSHAKEMISTO/src/rohmotti.py $WWWDIR/

Rohmotti tarvitsee myös seuraavia WWW-palvelimen tarjoilemia
staattisia tiedostoja::

    cp -a $ASENNUSHAKEMISTO/static/* $WWWDIR/

Python-moduulit toimivat, jos Pythonin hakupolussa on $ASENNUSHAKEMISTO/src.

Muokkaa asetuksia rohmotti.py:n alussa:

APP_ROOT_URI
    staattisten tiedostojen sijainti www-selaimen
    saavutettavissa

PYTHON_MODULE_PATH
    Rohmotin modulien sijainti ($ASENNUSHAKEMISTO/src)

HTML_TEMPLATE_PATH
    HTML-mallineitten sijainti ($ASENNUSHAKEMISTO/html_templates)

DSN
    tietokantayhteyden parametrit

DBSCHEMA
    tietokantaosien asennuskaavio (rohmotti)


9. Käynnistys / käyttöohje
***************************

Sovelluksen sijainti: http://jgsavola.users.cs.helsinki.fi/rohmotti/src/rohmotti.py

Rohmottiin voi tehdä käyttäjätunnuksen kirjautumissivulla.

10. Liitteet
************

