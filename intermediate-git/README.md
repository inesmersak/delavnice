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
Git je sistem za sledenje verzijam datotek (sem spadajo še npr. Subversion, Perforce), najbolj pogosto je uporabljen za sledenje spremembam v kodi.

Osnovna logična enota sprememb je commit. Vsak commit je "snapshot" stanja naših datotek. Kako pridemo do commita?
1. Modificiramo datoteko/e v svojem _working directoryju_. 
2. Spremembe dodamo v _staging area_ z `git add <datoteka>`. 
3. Commit ustvarimo iz "staged" sprememb z `git commit`. 

Commiti se shranjujejo v mapo `.git`, ki je prisotna v vsakem repozitoriju in poleg commitov vsebuje tudi podatke o tem, kaj je dodano v staging area in druge metapodatke tega repozitorija.

![](https://git-scm.com/book/en/v2/images/areas.png)

## Zakaj Git? 
* popoln pregled nad spremembami (in njihovimi avtorji)
* z lahkoto lahko preidemo na prejšnjo verzijo neke datoteke
* distribuiran sistem: vsi imamo celoten repozitorij (z vso zgodovino) pri sebi
* kljub vsemu zgornjemu repozitorij zaseda malo prostora, brskanje po zgodovini je hitro

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

## Povzetek Git ukazov
### Dodajanje commita
```
git add <datoteka1> <datoteka2> ... <datotekaN>
git commit
```

### Nov branch
```
git branch <ime>
```
Če se želimo premakniti na ta branch:
```
git checkout <ime>
```
Ustvarjanje novega brancha in premik v enem ukazu:
```
git checkout -b <ime>
```
