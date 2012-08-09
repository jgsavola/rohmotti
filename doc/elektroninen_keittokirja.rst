========================
Elektroninen keittokirja
========================

.. contents:: Sisällysluettelo

.. raw:: pdf

  PageBreak

1. Johdanto
***********

Elektroninen keittokirja on websovellus, jonka avulla ylläpidetään
tietokantaa ruoka-aineista, resepteistä ja ateriakokonaisuuksista sekä
ruokailutilaisuuksista ja henkilöistä, jotka ovat näihin tilaisuuksiin
osallistuneet. Elektronisen keittokirjan avulla on mahdollista tehdä
ruoka-aineisiin, resepteihin, ateriakokonaisuuksiin ja henkilöihin
kohdistuvia hakuja. Sovelluksella voi myös tehdä ostoslistan reseptin
tai ateriakokonaisuuden perusteella. Resepti koostuu
ruoka-ainelistasta ja valmistusohjeesta. Ateriakokonaisuus sisältää
yhden tai useamman reseptin ja mahdolliset ruokajuomat.
Ruokailutilaisuus muodostuu ateriakokonaisuudesta, aikaleimasta ja
tilaisuuteen osallistuvista henkilöistä --- yhtenä tavoitteena onkin
olla tarjoamatta vahingossa samaa ruokalajia useampaan kerran samalle
henkilölle! Lisäksi eri kohteisiin on mahdollista liittää valokuvia ja
kommentteja.

Toimintoja
----------

a)  raaka-aineen syöttö ja muutos

b)  reseptin kirjaus ja korjaus

c)  reseptin haku

d)  reseptien katselu

e)  ostoslistan teko valitun reseptin tai ateriakokonaisuuden perusteella

f)  syöjien syöttö ja muutos

g)  käyttäjien hallinta

Ympäristö
---------

Ohjelma toteutetaan Python-ohjelmointikielellä CGI-ympäristössä.
Tietokantajärjestelmänä käytetään PostgreSQL:ää.

Ohjelman rakenne toteutetaan käyttäen Model-View-Controller-tyyliä.

Tietoturva
----------

Järjestelmän käyttäminen edellyttää tunnistautumista. Tunnistautunut
käyttäjä saa sessioavaimen, joka on voimassa määrätyn ajan
tunnistautumisesta (tai viimeisestä käyttäjän toiminnosta).

Tietokantakyselyjen muodostaminen tehdään niin, että kaikkea
käyttäjältä peräisin olevaa tietoa käsitellään huolellisesti. Tämä
tarkoittaa mm. järjestelmällistä paikanpitäjäparametrien käyttämistä
tietokantakyselyiden muodostamisessa.


2. Yleiskuva järjestelmästä
***************************

3. Käyttötapaukset
******************

4. Järjestelmän tietosisältö
****************************

5. Relaatiotietokantakaavio
***************************

6. Järjestelmän komponentit
***************************

7. Käyttöliittymä
*****************

8. Asennustiedot
****************

9. Käynnistys / käyttöohje
***************************

10. Liitteet
************

