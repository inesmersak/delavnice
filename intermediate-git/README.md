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
Commit hash je zgeneriran iz commit objekta in zgleda takole: `a9ca2c9f4e1e0061075aa47cbb97201a43b0f66f`
Če spremenimo kaj v commitu (tudi predhodnika), se zato spremeni tudi hash. Za nanašanje se na commit je ponavadi
 dovolj kratka verzija hasha, npr. `a9ca2c9`.

### Popravljanje zadnjega commita
Naredi vse želene spremembe, jih dodaj z `git add`, nato pa namesto normalnega commita poženi  
```
git commit --amend
```
To odpre privzet editor (ponavadi Vim), kjer lahko dodatno spremenimo še sporočilo commita. 

Če sporočila ne želimo spremeniti, lahko namesto tega poženemo:
```
git commit --amend --no-edit
```
da se izognemo odpiranju in zapiranju editorja.

Alternativno lahko novo sporočilo podamo kar na ukazni vrstici:
 ```
git commit --amend -m "New commit msg"
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

### Pushanje brancha
Če želimo naš branch deliti z ostalimi (recimo, ko želimo odpreti pull request), ki delajo na istem projektu, ga lahko
 pushamo z
```
git push -u origin <ime>
```
Pri tem `origin` označuje naslov repozitorija, ki se nastavi ob klicu git clone (podobno, kot je `master` ime
 privzetega brancha, ki se naredi ob inicializaciji nekega repozitorija). Kam je usmerjen `origin`, lahko vidimo v 
 `.git/config`.
 
#### Remote branchi
Poleg origina (ki označuje remote repozitorij, ki smo ga klonirali) imamo lahko nastavljene tudi druge remote
 repozitorije (npr. fork od sodelavca). Remote branchi so podobni lokalnim, le da sledijo spremembam, ki se dogajajo
 v remote repozitoriju -- lokalno jih ne moremo premakniti (npr. ne moremo commitati), so read-only.
 Do remote brancha lahko dostopamo pod imenom `<remote>/<ime brancha>`, npr. `origin/login-feature`. Da
 posodobimo remote branche s spremembami, ki so se zgodile v remote repozitoriju (npr. nekdo je mergal
 pull request v `develop`), pokličemo 
```
git fetch <remote>
```
oziroma, če želimo posodobiti branche vseh remote repozitorijev / imamo samo en remote repozitorij:
```
git fetch
```
Ko lokalno prvič checkoutamo npr. `develop`, git ve, da v remote repozitoriju prav tako obstaja branch s takim 
 imenom, in naš lokalni branch "poveže" z remote branchem. Ko lokalno naredimo `git push` ali `git pull` na temu
 branchu, git zato ve, da naj se operaciji izvedeta na remote branchu, ki je povezan z lokalnim, in torej spremembe
 svojega lokalnega brancha pushamo remote ali pa lokalni branch posodobimo z remote spremembami. 
 (Ročno lahko povežemo tudi brancha, ki imata različni imeni.)

Opcija `-u`, ki jo uporabimo, ko prvič pushamo svoj branch (npr. na `origin` kot zgoraj) poskrbi, da bo naš lokalni
 branch povezan z remote branchem, ki smo ga ravno naredili s preostankom ukaza.

### Posodobitev brancha
Ko naredimo svoj branch iz npr. `develop` brancha in na njem delamo nekaj časa, se lahko `develop` branch vmes
 posodobi (mergajo se drugi pull requesti). Pri tem se lahko mergane spremembe prekrivajo s tistimi na našem branchu, 
 kar povzroči konflikte, ko odpremo pull request. V tem primeru (pa tudi sicer) želimo svoj branch posodobiti s
 spremembami iz `develop`. To lahko naredimo na dva načina: z ukazoma
 `merge` ali `rebase`. 
 (Pred tem poskrbimo, da lokalni `develop` branch vsebuje najnovejše spremembe s tem, da pullamo, ali pa
 mergamo / rebasamo na remote branch `origin/develop`, ki ga posodobimo s fetchom.) 

#### Merge
Spremembe iz brancha `develop` mergamo z ukazom:
```
git checkout <ime>
git merge develop
```
`merge` poišče zadnji skupni commit med branchema, ki ju mergamo, in nato poskuša avtomatsko skombinirati spremembe iz
 zadnjih commitov na obeh branchih in skupnega prednika. Pri tem ustvari nov commit na branchu, kamor mergamo, ki mu
 rečemo merge commit.
![](https://git-scm.com/book/en/v2/images/basic-merging-2.png)
Na sliki je primer merganja brancha `iss53`, ko je ta pripravljen, v branch `master`. Pri tem je nastal merge commit C6.

#### Rebase
Spremembe iz brancha `develop` lahko v svoj branch dodamo tudi z:
```
git checkout <ime>
git rebase develop
```
`rebase` doda najnovejše commite iz `develop` brancha na naš branch, commite, ki smo jih naredili na svojem branchu, pa
 prestavi za njih (dodaja enega po enega, pri čemer lahko pri vsakem pride do kakšnega konflikta, ki ga moramo rešiti
 na roke). Pri tem naše commite pravzaprav prepiše, saj imajo po rebasu drugačen hash.
![](https://git-scm.com/book/en/v2/images/basic-rebase-3.png)
Na sliki je primer rebasanje brancha `experiment` na `master`. Pri tem se commit C4, ki smo ga naredili na branchu
 `experiment` prepiše v C4'. 

### Popravljanje starejših commitov
Obstaja tudi interaktivna verzija `rebase` ukaza, s katerim lahko poleg navadnega rebasea še spremenimo commite, ki so 
 del rebasea. Ponavadi ga uporabljamo ravno za popravljanje commitov na svojem branchu, kar naredimo z ukazom:
```
git rebase -i HEAD~3
```
če želimo popraviti zadnje 3 commite. Pri tem je `HEAD` pointer na trenutni (torej naš) branch, torej zadnji commit
 na njemu, `HEAD~1` pomeni predhodnik commita, na katerega kaže `HEAD`, `HEAD~3` pa predhodnik tri commite nazaj. 
Dejansko branch rebaseamo samega nase nekaj commitov nazaj, z namenom spremembe teh commitov. 
 Pri tem moramo specificirati predhodnika najstarejšega commita, ki ga želimo popraviti.
 
 Ko ukaz poženemo, se odpre privzet editor s seznamom vseh commitov, vključenih v rebase, in dolgim seznamom navodil:
```
pick f7f3f6d Change my name a bit
pick 310154e Update README formatting and add blame
pick a5f4a0d Add cat-file

# Rebase 710f0f8..a5f4a0d onto 710f0f8
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
# .       create a merge commit using the original merge commit's
# .       message (or the oneline, if no original merge commit was
# .       specified). Use -c <commit> to reword the commit message.
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
```
Pred vsakim commitom je ukaz, ki pove, kaj želimo z njim narediti. Bolj pomembne možnosti so:
* `pick` zadrži commit brez sprememb, 
* `reword` nam omogoča spremembo commit msga, 
* `edit` pomeni, da se bo rebase ustavil, preden applyja ta commit, da ga bomo lahko amendali, 
* `squash` trenuten commit združi s prejšnjim, commit msga pa združi,
* `fixup` naredi isto kot squash, samo da zadrži le prejšnji commit msg,
* `drop` izbriše commit. 

Rebase se izvede, ko zapremo editor, po vrsti od zgornjega proti spodnjemu commitu, pri čemer se ustavi pri vsakem
 commitu, kjer smo to specificirali, ter pri tistih, ki povzročijo konflikte. Ko jih razrešimo oz. naredimo, kar smo
 želeli, rebase nadaljujemo z `git rebase --continue`. Če se odločimo, lahko rebase tudi prekličemo z `git rebase
 --abort` (če se še ni izvedel v celoti). Trenutno stanje našega repozitorija lahko kadarkoli preverimo  z ukazom
 `git status`. 

### Razveljavljanje rebasea / mergea
Če smo rebaseali ali mergali na nek branch, pa z rezultati nismo zadovoljni, nam pri razveljavljanju lahko pomaga
 `git reflog`. reflog je dnevnik vseh sprememb pointerja `HEAD`. Če npr. naredimo en commit, nato pa poženemo
  interaktiven rebase, bo reflog zgledal približno takole:
```
$ git reflog
37656e1 HEAD@{0}: rebase -i (finish): returning to refs/heads/git_reflog
37656e1 HEAD@{1}: rebase -i (start): checkout origin/master
37656e1 HEAD@{2}: commit: some WIP changes 
``` 
Če želimo rebase razveljaviti, lahko stanje repozitorija resetiramo na commit pred rebaseom z
```
git reset HEAD@{2}
```

### Spravljanje / razveljavljanje sprememb
Ko poskusimo narediti pull, merge ali rebase, se nam lahko pojavi sledeče sporočilo:
```
You have unstaged changes.
Please commit or stash them.
```
To pomeni, da imamo nekaj sprememb v _working directoryju_, ki jih moramo shraniti ali razveljaviti, preden
 nadaljujemo z mergeom ali rebaseom. Lahko jih commitamo, poleg tega pa imamo na voljo še stash za začasno
 shranjevanje in reset za zavrženje sprememb. 

#### Stash
Če želimo svoje spremembe začasno shraniti, lahko to naredimo z
```
git stash
```
Ko želimo zadnje shranjene spremembe ponovno uveljaviti in jih odstraniti iz stasha, pa uporabimo
```
git stash pop
```
Vse vnose v stashu lahko vidimo z
```
$ git stash list
stash@{0}: WIP on submit: 6ebd0e2... Update git-stash documentation
stash@{1}: On master: 9cc0589... Add git-stash
```
Starejše spremembe lahko uveljavimo z
```
git stash apply stash@{1}
```
Če jih želimo tudi odstraniti iz stasha, pa z
```
git stash pop stash@{1}
```
#### Reset
S pomočjo ukaza `reset` lahko stanje svojega repozitorija resetiramo na stanje pred zadnjim (predzadnjim ...) commitom.
Poglejmo si ga na sledeči zgodovini repozitorija, ki ga bomo resetirali na predhodnika zadnjega commita, torej
 `HEAD~`. 
![](https://git-scm.com/book/en/v2/images/reset-start.png)
Obstajajo trije načini reseta:
* `git reset --soft HEAD~` premakne glavo brancha, na katerega kaže `HEAD`, na specificiran commit; v primeru `HEAD` 
 po novem kaže na commit `9e5e6a4`,
* `git reset --mixed HEAD~` poleg tega, kar naredi `--soft`, še unstagea vse spremembe, ki so zgodile po specificiranem
 commitu oz. povzroči, da index izgleda kot nov `HEAD`; v primeru je v indexu zdaj v2 datoteke `file.txt`,
* `git reset --hard HEAD~` poleg tega, kar naredi `--mixed`, še resetira working directory, da izgleda kot nov `HEAD`;
v primeru je v working directoryju zdaj v2 datoteke `file.txt`.

Če imamo v working directoryju spremembe, ki bi se jih želeli znebiti pred rebaseom, mergeom ali pullom, potem lahko
 to naredimo z ukazom
```
git reset --hard HEAD
```
S tem resetiramo repozitorij na stanje zadnjega commita. Branch, na katerega kaže `HEAD`, se ne premakne, kakršnekoli
 staged spremembe in spremembe v working directoryju pa se zavržejo. S tem ukazom (verzijo `--hard`) je treba biti
 previden, saj ne-commitanih sprememb ne moremo dobiti nazaj.

### Odstranitev brancha
Če želimo odstraniti lokalen branch
```
git branch -d <ime>
```
Če branch ni bil nikamor mergan oziroma ima nove commite, potem je treba odstranitev forceati z
```
git branch -D <ime>
```
Za odstranitev brancha tudi v remote repozitoriju `origin`
```
git push origin --delete <ime>
```

### Zgodovina commitov
Zgodovino commitov lahko vidimo z ukazom
```
git log
```
Če želimo videti tudi spremembe, ki so bile narejene v vsakim commitu
```
git log -p 
```
Če želimo videti samo statistiko sprememb in spremenjene datoteke
```
git log --stat
```
Za bolj kompakten zapis lahko uporabimo
```
git log --pretty=oneline
```
Output lahko še posebej formatiramo
```
$ git log --pretty=format:"%h - %an, %ar : %s"
ca82a6d - Scott Chacon, 6 years ago : Change version number
085bb3b - Scott Chacon, 6 years ago : Remove unnecessary test
a11bef0 - Scott Chacon, 6 years ago : Initial commit 
```
Z opcijo `--graph` pa lahko vidimo predhodnika vsakega commita
```
$ git log --pretty=format:"%h %s" --graph
* 2d3acf9 Ignore errors from SIGCHLD on trap
*  5e3ee11 Merge branch 'master' of git://github.com/dustin/grit
|\
| * 420eac9 Add method for getting the current branch
* | 30e367c Timeout code and tests
* | 5a09431 Add timeout protection to grit
* | e1193f8 Support for heads with slashes in them
|/
* d6016bc Require time for xmlschema
*  11d191e Merge branch 'defunkt' into local 
```

#### Iskanje po zgodovini
Če želimo poiskati vse commite, kjer se spremeni število pojavitev nekega niza, npr. imena neke funkcije ali
 spremenljivke, potem lahko uporabimo
```
git log -S <ime_spremenljivke>
```
Za spremljanje razvoja (uporabe) neke funkcije znotraj specifične datoteke pa obstaja
```
$ git log -L :git_deflate_bound:zlib.c
commit ef49a7a0126d64359c974b4b3b71d7ad42ee3bca
Author: Junio C Hamano <gitster@pobox.com>
Date:   Fri Jun 10 11:52:15 2011 -0700

    zlib: zlib can only process 4GB at a time

diff --git a/zlib.c b/zlib.c
--- a/zlib.c
+++ b/zlib.c
@@ -85,5 +130,5 @@
-unsigned long git_deflate_bound(z_streamp strm, unsigned long size)
+unsigned long git_deflate_bound(git_zstream *strm, unsigned long size)
 {
-       return deflateBound(strm, size);
+       return deflateBound(&strm->z, size);
 }


commit 225a6f1068f71723a910e8565db4e252b3ca21fa
Author: Junio C Hamano <gitster@pobox.com>
Date:   Fri Jun 10 11:18:17 2011 -0700

    zlib: wrap deflateBound() too

diff --git a/zlib.c b/zlib.c
--- a/zlib.c
+++ b/zlib.c
@@ -81,0 +85,5 @@
+unsigned long git_deflate_bound(z_streamp strm, unsigned long size)
+{
+       return deflateBound(strm, size);
+}
+
```

### Prestavljanje commita
Recimo, da začnemo z delom na novem featurju, pri tem pa pozabimo narediti nov branch in ponesreči commitamo na
 branch, na katerem smo trenutno (recimo `develop`). Z `git log` lahko ugotovimo hash commita, ki ga želimo
 premakniti, `develop` branch resetiramo (za en commit nazaj), nato pa naredimo nov branch, se premaknemo nanj, 
 in uporabimo
```
git cherry-pick <hash>
```
da dodamo commit na nov branch.

