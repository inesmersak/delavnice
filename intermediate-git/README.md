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
Do sedaj ste verjetno delali v istem repozitoriju z največ tremi, štirimi drugimi za potrebe kakšnega projekta na faksu (razen, če ste opravljali kakšno študentsko delo v malo večjem podjetju), ali pa ste imeli svoj repozitorij za kakšen projekt, seminarsko ali diplomsko delo. Postopek je verjetno zgledal nekako tako: naredili ste neke spremembe, jih commitali, in pushali. Pred tem ste kolegom zabičali, naj ne pushajo nič novega, da ne bo konfliktov :) 

Pri tem ste implicitno ves čas živeli na privzetem `master` branchu. Če so se konflikti slučajno zgodili, ker vas je kolega prehitel, ste naredili pull, ga razrešili, in ponovno pushali. 

Če pa v istem repozitoriju dela nekaj deset programerjev na resnem projektu, to ne zadostuje več. Zakaj? 
* Ne želimo nedokončane kode v `master` branchu; ta gre morda direktno live.
* Preden spravimo kodo do stranke, jo želimo pregledati, potestirati, da deluje tako, kot je potrebno.

Zato ima vsak programer ponavadi nek svoj "prostor", kjer razvija feature / odpravlja bug, ki mu je bil dodeljen. Ponavadi dela na svojem branchu v skupnem repozitoriju ali pa ima fork skupnega repozitorija. 

### Forki
Fork repozitorija je uporabnikova kopija originalnega repozitorija, in se obnaša tako kot normalen repozitorij, ki bi ga naredil uporabnik, le da lahko naš fork posodabljamo s spremembami, ki so se zgodile v originalnem repozitoriju. Forki so posebej uporabni, če želimo veliko eksperimentirati, pa ne želimo zasmetiti originalnega repozitorija, ali pa v primeru odprto-kodnih projektov, ki ga želimo razširiti za našo uporabo, vendar razširitev morda ne sodi v core projekt. 

Kako narediti fork? Če želimo klonirati npr. repozitorij ul-fmf/nadlogar, potem stisnemo na gumb `Fork`, potrdimo in ustvari se repozitorij <uporabnik>/nadlogar, ki je (zaenkrat) po vsebini identičen originalnemu. Sedaj lahko po mili volji dodajamo spremembe, jih pushamo, in če se nam zdi, da bi bila katera od sprememb koristna tudi za originalen projekt, naredimo pull request (iz nekega brancha svojega forka).
  
Če za developanje v večji skupini programerjev uporabljamo svoj fork, ponavadi še vedno za vsak feature / bug naredimo svoj branch in odpremo pull request iz tega na originalni repozitorij, nato pa `master` branch na svojemu forku posodobimo s sprejetimi spremembami. Večina postopka je torej podobna, kot če bi delali s svojimi branchi znotraj originalnega repozitorija. 

### Branchi
Ne glede na to, ali delamo v originalnem (skupnem) repozitoriju ali v svojem forku, bomo za vsak feature / bug verjetno želeli narediti nov branch. Zakaj? 
* lažje sledimo, katere spremembe se nahajajo kje
* lahko odpremo lepo urejene, vsebinsko zaključene pull requeste
* lažje prekinemo nenujno delo na featureju, da popravimo kritičen bug v produkciji

Nov branch lokalno naredimo z ukazom:
```
git branch <ime>
```
Preden začnemo dodajati spremembe na ta branch, se moramo nanj še premakniti, to naredimo z:
```
git checkout <ime>
```
Sedaj lahko normalno delamo spremembe, jih spravljamo v commite, ko smo z delom lokalno končali, pa nov branch (skupaj z vsemi commiti) pushamo na github repozitorij z:
```
git push -u origin <ime>
```

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


