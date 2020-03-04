# Napredna Git delavnica: kako odpreti lepo urejen pull request
11. marec 2020

V ekipi večih razvijalcev, ki resno delajo na nekem produktu, osnovni git ukazi ne zadostujejo več, prav tako pa ne zadostuje pushanje kode na `master` branch. Če želimo zagotoviti pravilnost, robustnost in berljivost (ter s tem olajšati vzdrževanje) kode, je potrebno poskrbeti tudi za kvalitetne peer reviewje sprememb, predpogoj za to pa so lepo urejeni pull requesti. Cilj delavnice je osvojiti nekatere (malo bolj) napredne git ukaze, ki nam bodo pomagali pri procesu razvijanja in reviewjanja kode.

Pogledali si bomo: 
* delo z branchi, med drugim rebase, rebase interactive, cherry pick; 
* razveljavljanje sprememb, med drugim amend, reset in reflog; 
* kako odpreti in popraviti pull request (ter se dotaknili urejenih commitov in kvalitetnih pull request reviewjev).

Potrebno je predznanje osnovnih git ukazov (add, commit, pull, push). 

Kdor bo imel svoj računalnik, naj si vnaprej namesti Git, splošna navodila za vse operacijske sisteme so na voljo tukaj: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git. 

## Kaj je Git?
Malo opisa o tem, kako Git deluje -- ne preveč. 

## Zakaj Git? 

## Delo v skupnem repozitoriju

### Branchi

### Forki

### Pull requesti
Moja koda dela -- želimo jo spraviti live.

Še preden pa jo mergamo, je potrebno narediti pull request review. 

### PR review

#### Nasveti za avtorja
Dobro urejen pull request s svojimi commiti pripoveduje neko zgodbo -- reviewerju je ob sledenju commitov očitno viden in razumljiv miselni proces za spremembami.

#### Nasveti za reviewerja

## Zanimivi scenariji
* Branch si začel iz nekega drugega brancha namesto iz masterja -- kako ga "rebasati" na masterja? 
* Dodal si commit na napačen branch -- kako ga prestaviti na pravega?
* Svoj branch si želel rebasati na latest master, vendar si ponesreči pullal -- kako razveljaviti pull?

## Jedrnat povzetek uporabnih Git ukazov
