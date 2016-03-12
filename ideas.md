* moguce je samo primati podatke sa jednom klienta u jedno vrijeme (izbjegavamo koliziju)
* koristimo jednu socket konekciju za jednu komandu i brisemo socket nakon klienta
* GUI za biranje konekciju
* Novi nacini upravljanja se trebaju registrovati da bi se pojavili 
* Poseban API za slanje podatke (api preko socket konecije i slajna podataka na server u odredjenoj formi)
* nasumicno generisati mali string koji ce se slati prije poruke kako bi se znalo o kojem se uredjaju radi, tako da treba da postoji register funckija koja ce da ostvari konekciju sa serverom koji onda uredjaje skladisti po tom stringu.
* Clijent salje komandu serveru, on obradi posalje na robota, i onda vraca done clientu koji se potom odjavi (izbrise)

