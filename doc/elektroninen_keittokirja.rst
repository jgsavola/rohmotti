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

Hakutoiminnoissa voidaan hyödyntää PostgreSQL:n Full Text Search
-ominaisuutta.


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

6. Järjestelmän komponentit
***************************

7. Käyttöliittymä
*****************

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

