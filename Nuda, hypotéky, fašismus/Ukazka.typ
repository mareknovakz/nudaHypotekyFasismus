#set page(
  width: 110mm + 5mm,
  height: 180mm + 5mm,
  margin: (inside: 65pt + 2.5mm, outside: 45pt + 2.5mm, top: 50pt + 2.5mm, bottom: 80pt + 2.5mm),
  footer-descent: 30pt,
  footer: context [
    #set text(size: 9pt, font: "Courier Prime")
    #let page_num = counter(page).get().first()
    #if calc.even(page_num) {
      align(left)[#page_num]
    } else {
       align(right)[#page_num]
    }
  ]
)
#set text(font: "Courier Prime", size: 10pt, lang: "cs", hyphenate: auto)
#set par(first-line-indent: 1.5em, justify: true, leading: 10pt)

#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: 20pt, weight: "bold", font: "Courier Prime")
  #set par(justify: false)
  #it.body
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: 16pt, weight: "bold", font: "Courier Prime")
  #set par(first-line-indent: 0pt, justify: false)
  #v(20pt, weak: true)
  #it.body
  #v(23pt, weak: true)
]

#page(footer: none)[
  #set align(center + horizon)
  #set par(justify: false)
  #text(size: 18pt, weight: "bold", font: "Courier Prime")[Nuda, hypotéky, fašismus]
  #v(1em)
  #text(size: 12pt, font: "Courier Prime")[Mirek Mrkvička]
  #v(2em)
  #text(size: 11pt, style: "italic", font: "Courier Prime")[ukázka]
]

#page(margin: 0pt, footer: none)[
  #set align(center + horizon)
  #image("koně.jpg", width: 100%, height: 100%, fit: "cover")
]

= Přesně takhle to chtěl

#set par(first-line-indent: 0pt, justify: false, leading: 10pt)

Prostoduchý Josífek pozoruje akvárium. \
Mečovka rodí jednu rybku za druhou.

#v(1.2em)

Josífek rád sleduje, \
jak ostatní ryby trhají a polykají novorozeňata.

#v(1.2em)

A Bůh se rád dívá na prostoduchého Josífka, \
jak se raduje z krmení rybiček.

#pagebreak()

= Vnitřní dědek

#set par(first-line-indent: 0pt, justify: false, leading: 10pt)

Moje vnitřní žena \
žila dokonalý vnitřní život s vnitřním mužem, \
vnitřním psem, vnitřním dítětem, \
v malém vnitřním domku, \
na který si vzali vnitřní hypotéku. \
Splátky je stojí půlku vnitřní výplaty, \
ale prý se to vnitřně vyplatilo. \
Dřív totiž bydleli u \
jeho vnitřních rodičů: \
mého vnitřního dědka \
a vnitřní báby.

#v(1.2em)

Vnitřní bába pořád brečela, \
že jsou na ni vnitřně zlí, \
že moje vnitřní žena \
rozmazluje jejich vnitřní dítě \
a vůbec se o něj nestará. \
Chudák z toho měl, ten vnitřní kluk, \
vnitřní zánět vnitřního vnitřního ucha. \
A tak moje vnitřní žena \
začala chodit na vnitřní jógu. \
Aby našla svoji \
vnitřní vnitřní bohyni.

#pagebreak()

= Nuda, hypotéky, fašismus

#set par(first-line-indent: 0pt, justify: true, leading: 10pt, spacing: 20pt)

Lodní deník kapitána Mirka Mrkvičky, hvězdné datum [zvolte letopočet]. Volím kolonizaci vesmíru, nastaveno na rok 563.

Prolétám kolem planety Google 234. Na planetě není žádný život, jen servery, ajťáci a cloudy pro generování videí s kočkami do 30 sekund – typicky kočka padající z gauče. Cloudy na planetě Google 234 premium už umí generovat videa s kočkami do dvou minut. Cloudy pro generování videí s kočkami do 5 minut jsou na planetě Google 234 platina.

Obloukem se vyhýbám planetám, které dřív bujely životem, teď je na nich jen uhlí a ropa. Jsou to planety Shell, Čepro nebo RobinOil. Novináři zde mají vstup navždy zapovězen.

Setkávám se se sadomasochistickou sektou toužící po autokracii, říkají si lidstvo. Role si rozdělují hodem mince: panna – robotník, orel – pán.

Touží po autokracii, protože neví, jak si rozdělit práci. Zkoušeli rovnostářství, ale nikdo nic nedělal, zkoušeli si za práci platit, jenže nevěděli, kdo kolik komu má dát, a ti, co měli málo, záviděli těm, co mají hodně, a ti, co měli hodně, se styděli.

Prolétám kolem planety básníků. Jsou smutní, protože poezie spáchala sebevraždu skokem do černé díry a ta, která zůstala, zničila nakladatelství redaktorskými úpravami.

Setkávám se se sadomasochistickou sektou toužící po fašismu. Říkají si střední třída. Role si rozdělují hodem mince: panna – půjdou do táborů, orel – budou pověšeni za nohy na benzínce. Je to jejich zvířecí přirozenost, tvrdí mi. Jinak to příroda neumí.

Touží po fašismu, protože se nudí. Nudí se, protože si neumí rozproudit krev jinak než alkoholem a život neohrožujícími adrenalinovými aktivitami: každý týden nějaký event, další vernisáž, další farmářské trhy, další slavnosti vína, další kino.

Rádi by dosáhli ideálu sparťanských válečníků, o kterých jim nikdo neřekl, že ty ideály nejsou pravdivé. Jejich bitvy neprobíhají u Thermopyl, ale v excelovských tabulkách.

Touží po hypotékách. Celý život se chtějí zadlužit na 30 let, aby se cítili svobodněji a mohli se povyšovat nad ty, co nemají dluhy, anebo nad ty, co dluhy mají, ale ty špatné, protože hypotéka je ctnost. Kde ztratili víru v Boha, nacházejí poslední útočiště v hypotéce. A kde na ni nedosáhnou, tam bují fašismus.

Planeta Ikea, planeta Microsoft, planeta Burger King, planeta Foot fetish porno, planeta Nike, planeta ČEZ, planeta Adidas, planeta IBM, planeta Vulture IT.

Planeta Vulture IT, jsem na planetě Vulture IT – malá krachující IT společnost. Jedu autobusem a někdo si vedle mě čte Bibli, čte ji nahlas a já nevím, jestli se nás snaží obrátit na svou víru, nebo nás jen všechny po ránu nasrat. Přes plastovou tabuli u dveří vidím stát feťáka, je 8 hodin ráno, feťák se klepe jak rosol a tře zuby o sebe. Jsem rád, že jezdím MHD a ušetřím za vlastní auto.

Vstupuji do klece pro potkany, 12 pater proskleného kvádru. Hned v kuchyňce potkávám hlouček potkanů, probíhají mezi nimi dvě debaty: o tom, co bude k obědu, a jak ses ráno vysral. Debaty probíhají paralelně.

Jsou dvě odpoledne a já dostávám podruhé vrácený ticket na modul KDL 5.4.3, o kterém mi nikdo neřekl, jak má fungovat. Myslím na to, jak se večer vožeru, takové malé každodenní vítězství. Všichni tu zabili svoje vnitřní dítě před svými vnitřními rodinami a své vnitřní otce přinutili držet pozornost na seberozvojových kurzech. Přijde za mnou potkan a dvacet minut šišlá něco o tom, jak má fungovat KDL 5.4.3. Svůj projev zakončuje slovy: „Hele, kámo, já vlastně nevím.“ V tu chvíli si představuju, jak mám na sobě několik kilo trhaviny. _Pojď, kancelářská budovo, zahrajeme si na jedenácté září._ Říkám si, že to už je vlastně moc, možná by stačilo se vymočit do květináče nebo schovat toner od tiskárny, ale to je na revoluci strašně málo. _Už vím!_

Jdu z open space jakoby na záchod, rozhlížím se, jestli okolo není nějaký potkan. Sahám po požárním alarmu, ještě se usměju do kamery. V tu chvíli se cítím jako Kubiš, Gabčík, Opálka, Patton, Churchill, Orwell a Koněv v jedné osobě, ale jen jednu pikosekundu. Po rozvučení zvonku div se nepomočím. Běžím do open space, kde už panikaří potkani.

Všichni spořádaně, poslušně v jedné řadě po schodech, tak jak to uvádí normy, to jediné umíme. Venku už slyším houkačky a čekám na červené hasičské auto, ale jako první vidím jet policii. Prý nějaký debil spustil alarm jen tak a nic jiného se vlastně nestalo, mají ho natočeného.

Klepu se jak ratlík, zezadu na krku cítím strašné horko – jdou po mně. Potí se mi ruce a lapám po dechu. Nemůžu si stěžovat, přesně takhle jsem to chtěl.
