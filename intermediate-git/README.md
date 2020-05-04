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
Ko želimo razvijati kakšen drugačen feature, brez da bi pri tem motili glavno nit razvoja, ponavadi uporabimo
 branching. Gitov branch je preprost pointer na zadnji commit, ta pa ima pointer na predzadnji commit ... Tudi `master
 ` je čisto navaden branch. 
 ![](https://git-scm.com/book/en/v2/images/branch-and-history.png)
Ko naredimo nov branch `v1.0`, se ustvari pointer, ki kaže na zadnji commit brancha `master` (na tem smo bili, ko
 smo ustvarili nov branch). Ko ustvarjamo nove commite, se bo pointer `v1.0` premikal naprej, `master` pa bo ostal, 
 kjer je. Poznamo pa en poseben pointer, `HEAD`, ki kaže na branch, na katerem se trenutno nahajamo.

Ne glede na to, ali delamo v originalnem (skupnem) repozitoriju ali v svojem forku, bomo za vsak posamezni feature / bug
 verjetno želeli narediti nov branch. Zakaj? 
* lažje sledimo, katere spremembe se nahajajo kje
* lahko odpremo lepo urejene, vsebinsko zaključene pull requeste
* lažje prekinemo nenujno delo na featureju, da popravimo kritičen bug v produkciji
* če podjetje uporablja tickete, so branchi pogosto vezani na številko ticketa

Nov branch lokalno naredimo z ukazom:
```
git branch <ime>
```
S tem ga baziramo na branchu, na katerem se trenutno nahajamo. Ponavadi je to `master` branch, oz. v primeru, da je 
`master` branch direktno deployan na produkcijo, na vmesni `develop` branch. Vsi developerji, ki razvijajo nov feature, 
svoj branch ponavadi bazirajo na tem branchu. 

Preden začnemo dodajati spremembe na naš nov branch, se moramo nanj še premakniti, to naredimo z:
```
git checkout <ime>
```
Sedaj lahko normalno delamo spremembe, jih spravljamo v commite, ko smo z delom lokalno končali, pa nov branch 
(skupaj z vsemi commiti) pushamo na Github repozitorij
```
git push -u origin <ime>
```

### Pull requesti
Ko zaključimo z implementacijo featureja / popravljanjem buga, želimo kodo spraviti nazaj v `develop` branch. To
 naredimo tako, da pushamo svoj branch na Github repozitorij in nato na Githubu odpremo pull request. Pri tem
 ponavadi assignamo nekoga, ki bo naš pull request pregledal in ga, ko se vsi strinjajo z implementacijo in je bil
 pull request potestiran, mergal -- to pomeni, da bodo commiti iz našega brancha dodani v `develop` branch. (Če
 reviewer izbere opcijo Squash & merge, bodo namesto posameznih commitov vse spremembe, ki smo jih naredili, squashane v
 en commit, ki bo dodan na `develop` branch.)

### PR review
Preden pa lahko pull request mergamo, je treba narediti PR review. Če gre za resen projekt, je treba preveriti, da
 vse spremembe delajo in da nobena sprememba ne bo negativno vplivala na preostanek našega sistema (primer so 
 prezahtevni queryji na bazi, ki trajajo predolgo, preveč obremenijo bazo in s tem vplivajo na nek kritičen del
 našega sistema).

#### Nasveti za avtorja
Priporočljivo je delati manjše pull requeste, ki rešujejo samo en problem, saj je tako lažje narediti pregled kode.
K temu pripomore tudi urejenost pull requesta. Dobro urejen pull request s svojimi commiti pripoveduje neko zgodbo
 -- reviewerju je ob sledenju commitov očitno viden in razumljiv miselni proces za spremembami. Vsak commit naj
 predstavlja manjšo spremembo, ki jo lahko na kratko opišemo v enem stavku (to naj bo msg našega commita).

#### Nasveti za reviewerja
* Pri vsaki vrstici spremembe premislimo, ali koda deluje točno tako, kot je zamišljeno, v vseh možnih scenarijih
 (npr. ali koda deluje, če je uporabnik prijavljen, pa tudi ko ni). 
* Med pregledom smo pozorni na to, ali je koda razumljiva in berljiva. Ali bi se jo dalo kako poenostaviti?
* Če nismo prepričani, zakaj je avtor spremembo naredil na tak način, ga prosimo, da stvar utemelji. V tem primeru je
 ponavadi smiselno tudi v kodi pustiti kratek komentar z utemeljitvijo načina implementacije. 
* Ko avtor dopolni / popravi svoj pull request, ga ponovno pregledamo, in po potrebi pustimo nove komentarje.
* Ko smo s kodo pull requesta zadovoljni, ga checkoutamo lokalno in potestiramo, da vse deluje. Če je vse v redu, 
 mergamo pull request.

## Scenarij
* Dodaj opcijo, da uporabnik nakaže nekaj denarja na svoj račun. Pri tem upoštevaj trenutno kodo in DRY (Don't Repeat
 Yourself) princip. Spremembe naredi v več kot enem commitu na svojem branchu. 
* Ko si s spremembami zadovoljen, odpri pull request na Githubu in dodaj reviewerja.
* Reviewer zahteva nekaj popravkov, ki ne sodijo vsi v isti commit. Dodaj popravke v prave commite in jih pushaj. 
 (Alternativno bi spremembe lahko dodali tudi v novem commitu.)
* Vmes je nekdo v `develop` zlobno mergal nekaj sprememb, ki se dotikajo istih vrstic, kot tvoj pull request. Rebasaj
 in resolvaj conflicte.
* Checkoutaj pull request od kolega in ga potestiraj.

### Kje se lahko zatakne
* Branch začnemo iz nekega drugega brancha namesto iz masterja -- kako ga "rebasati" na masterja? 
* Commit dodamo na napačen branch -- kako ga prestaviti na pravega?
* Svoj branch želimo rebasati na zadnje spremembe `develop` brancha, vendar ponesreči pullamo -- kako razveljaviti
 pull?

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


