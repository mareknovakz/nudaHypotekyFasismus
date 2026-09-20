#set page(
  width: 125mm + 5mm,
  height: 176mm + 5mm,
  margin: (inside: 55pt + 2.5mm, outside: 35pt + 2.5mm, top: 45pt + 2.5mm, bottom: 80pt + 2.5mm),
  footer-descent: 30pt,
  footer: context [
    #set text(size: 8pt, font: "Courier Prime")
    #let page_num = counter(page).get().first()
    #if calc.even(page_num) {
      align(left)[#page_num]
    } else {
       align(right)[#page_num]
    }
  ]
)
#set text(font: "Courier Prime", size: 10pt, lang: "cs", hyphenate: auto)
#set par(first-line-indent: 1.5em, justify: true, leading: 7.5pt)

#let blank-page() = {
  page(footer: none)[]
}

#let chapter-page-break() = pagebreak(to: "odd")

#let colophon-page-break() = pagebreak(to: "even")


#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: 18pt, weight: "bold", font: "Courier Prime")
  #set par(justify: false)
  #it.body
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: 14pt, weight: "bold", font: "Courier Prime")
  #set par(first-line-indent: 0pt, justify: false)
  #v(15pt, weak: true)
  #it.body
  #v(18pt, weak: true)
]

#show outline.entry.where(level: 1): it => {
  strong(it)
}


#let chapter(title, img_path, blank: false) = [
  #chapter-page-break()
  #set page(footer: none)
  #heading(level: 1, title)
  #pagebreak()
  #set page(footer: context [
    #set text(size: 8pt, font: "Courier Prime")
    #let page_num = counter(page).get().first()
    #if calc.even(page_num) [ #align(left)[#page_num] ] else [ #align(right)[#page_num] ]
  ])
  
  #if not blank [
    #page(margin: 0pt, footer: none)[
      #if img_path != "" and img_path != "404" [
        #set align(center + horizon)
        #image(img_path, width: 100%, height: 100%, fit: "cover")
      ] else if img_path == "404" [
        #set align(center + horizon)
        #set text(size: 11pt, weight: "regular", font: "Courier Prime")
        [404]
      ] else [
        #set align(center + horizon)
        #set text(size: 14pt, style: "italic", font: "Courier Prime")
        [[ Ilustrace ]]
      ]
    ]
  ]
]

#let poem-prose(title, body_content) = [
  #pagebreak(weak: true)
  #if title != "" [
    #heading(level: 2, title)
  ]
  #set par(first-line-indent: 0pt, justify: true, leading: 7.5pt, spacing: 17.5pt)
  #body_content
]

#let poem-poetry(title, body_content) = [
  #pagebreak(weak: true)
  #if title != "" [
    #heading(level: 2, title)
  ]
  #set text(hyphenate: false)
  #set par(first-line-indent: 0pt, justify: true, leading: 7.5pt, spacing: 7.5pt)
  #show par: it => layout(size => context {
    let w = measure(it).width
    if w > size.width {
      set align(right)
      it
    } else {
      it
    }
  })
  #body_content
]

#blank-page()
#blank-page()
#page(footer: none, margin: 1.5cm)[
  #set par(first-line-indent: 0pt)
  #set align(center + top)
  #set par(justify: false)
  #v(25%)
  #text(size: 22pt, weight: "bold", font: "Courier Prime")[Nuda, hypotéky,] \
  #text(size: 22pt, weight: "bold", font: "Courier Prime")[fašismus]
  #v(2em)
  #text(size: 16pt, font: "Courier Prime")[Mirek Mrkvička]
]
#blank-page()
#page(footer: none)[
  #set par(first-line-indent: 0pt, justify: false)
  #set align(center + top)
  #v(20%)
  #text(style: "italic")[ Kde ztratili víru v Boha, nacházejí poslední útočiště v hypotéce. A kde na ni nedosáhnou, tam bují fašismus.]
]
#blank-page()
#page[
  #outline(title: [Obsah #v(1em)], indent: 0pt)
]
#chapter("Návštěva na Zemi", "DreamCoreObdelnik.jpg")
#poem-poetry("Wine culture", [
  _Čas strávený ve vinném sklípku se nepočítá do života._

  _Co je to život?_

  #v(10pt)
  Sestoupil jsem v Letňanech, abych to zjistil.

  Letňanské předměstí lemují bílé

  rodinné domky, bílé jako jejich domácí,

  #v(10pt)
  tam žije Marie Alice,

  nakoupí v Tescu, vypere prádlo,

  pověsí prádlo, vyžehlí prádlo,

  podusí osso buco, udělá šafránové rizoto,

  uzavře životní pojistku, uklidí dům,

  vyčistí hlaveň u revolveru, přebalí batole,

  zalije petržel, přesadí orchideje,

  do dětského pokoje vybere nové barvy,

  pak se revolverem střelí do hlavy.

  #v(10pt)
  Tomáš Novotný si ráno uváže kravatu,

  nasedne do BMW X5, odjede do pojišťovny,

  zamítne několik plnění, sjedná pojištění flotily

  zahrnující sedm fabií.

  Doma sleduje Netflix,

  Jacka Danielse zapíjí Kozlem,

  protože jeho dcera strčila hlavu do igelitky,

  nemohla ji vytáhnout a udusila se.

  #v(10pt)
  Mladý pán, alfa samec Koudelka,

  chodí do gymu dvakrát denně,

  pije pouze proteinovo-banánové shaky,

  z vrtulníku by vyházel všechny levičáky.

  Instagram zaplňuje bonmoty,

  jeho přátelé jsou kokoti.

  Chtěl, aby černochy prodávali na pouti.

  Jednou mu sklouzne bench a rozdrtí si krkovici,

  těsně před smrtí si uvědomí, že je na kluky.

  #v(10pt)
  Slavnosti vína na Grébovce:

  štangle sušené zvířecí tkáně,

  sudy s pivem, koše plné tácků

  umaštěných od hořčice, kuřata plná salmonely.

  Opodál stojí ramenatý cirkusák.

  Oblečen v gepardím trikotu,

  cpe si do krku bochníky chleba

  a celé je polyká – pro pobavení.

  Pátrání po smyslu života:

  _Pravda je ve víně_

  – Wine culture.

  #v(10pt)
  Novotní mají ve vaně delfína,

  ocasem mlátí a sprostě nadává.

  Dneska bude dršťková, už se vaří kedluben.

  Máma pláče, že nejsou dost bohatí.

  Táta odešel pro mléko, už se nevrátí.

  #v(10pt)
  Michal Pokorný nepil,

  nekouřil, nemyl se, nejedl,

  nešukal, nehrál, nesvítil,

  netopil, nesurfoval.

  Jen pracoval a šetřil na pohřeb.

  Děti ho uložily do hromadného

  hrobu, co vznikl během covidu,

  peníze utratily za Labubu.

  #v(10pt)
  Emo Ema se řeže,

  ránu si ošetří dezinfekcí, bojí se infekcí.

  Eko Erika nakupuje bezobalově a nejí maso,

  na Bali létá první třídou,

  zemře hanebnou bídou.

  Bio Pepa šňupe pouze naturální piko.

  #v(10pt)
  Slavnosti vína na Grébovce:

  nudou, životem a prací zničení otcové litující svých hypoték

  a promarněného mládí, mírně opilé matky

  neschopné již čehokoliv litovat,

  otčímové, kteří nevlastní děti

  oslovují jménem, přestože je živí a

  předstírají, že je mají rádi, jako by byly jejich vlastní,

  milenky otců, o kterých matky tuší,

  milenky matek, po kterých otcové touží.

  Nejváženější členové domácnosti

  české národní zvíře – pes.

  Psi serou na každém rohu a lížou si koule.

  Plastové kelímky s vínem dováženým z Moravy,

  které na Moravě nikdo nechce pít.

  A děti.

  – White culture.

  #v(10pt)
])
#poem-poetry("Anemoia", [
  Jako děti jsme bydleli na sídlišti

  mezi poli koberců

  a cestovali po planetách

  vyšitých na černé dece.

  Bylo snadné skočit z Merkuru na Jupiter,

  prolézt černou dírou až k Plutu,

  #v(10pt)
  tehdy bylo ještě planetou.

  Pak nás máma zavolala k obědu

  a svět držel pohromadě.

  Možná si to jen takhle pamatuji.

  #v(10pt)
])
#poem-poetry("Žádost o zařazení do evidence zájemců o zaměstnání", [
  Na call centrum Úřadu práce

  volat nesmím.

  Paní na přepážce mi to zakázala.

  Prý tam lžou.

  #v(10pt)
  Sreality dělají z lidí socialisty.

  Co nezvládli Marx, Engels a Chomsky,

  to za odpoledne svedli zaměstnanci realitky.

  #v(10pt)
  Občas si vzpomenu na ideu nebe,

  o které se mi před lety zdálo.

  Chvíli nad tím přemýšlím

  a pak pokračuju v každodenních činnostech.

  #v(10pt)
  Naučil jsem se radovat ze žlutých cenovek v Tescu.

  Bohatí nechápou tu prostou extázi

  z brokolice za dvaadvacet.

  Chudina naštěstí nebývá osamělá,

  vždycky se najde někdo, s kým jde brečet nad nájmem.

  #v(10pt)
  Sreality dělají z lidí socialisty.

  Co nezvládli Marx, Engels a Chomsky,

  to za odpoledne svedli zaměstnanci realitky.

  #v(10pt)
  Občas si vzpomenu na ideu pekla,

  o které se mi před lety zdálo.

  Chvíli nad tím přemýšlím

  a pak pokračuju v každodenních činnostech.

  #v(10pt)
])
#poem-prose("Interclass", [
  „Já tě vezmu na nádraží, abys viděl, jak dopadají lidi, kteří to chtěli jen zkusit,“ řekla paní ve středních letech svému sotva šestiletému synovi.

  „Dobrý den, madam, směl bych vás pozvat na meeting vedení First International Bank, abyste věděla, jak dopadají lidi, kteří to jen zkoušejí?“

])
#poem-poetry("Pan Pták si vzal sick day", [
  Pan Pták si vzal sick day,

  má cystu na ledvině,

  myslel, že má kameny.

  Pod nánosy hlíny

  Ptákova matka spí.

  Pospěšme k místu,

  kde zaměstnanci spí.

  Ptákova milá

  na ostrově kočárků spí,

  nevzala si sick day.

  #v(10pt)
  Z kostí padlých

  pěstujeme nové kancly.

  Pan Pták má cystu ve výkazu práce.

  Sedí doma, nahmatává si bulky.

  Většinou nejsou zhoubné.

  Pod nánosy hlíny

  Ptákova matka spí.

  #v(10pt)
  Doktor Ptákovu cystu prohlíží.

  Hmatá, lechtá, hledá ledvinu.

  Cysta svědí, pálí, čas letí.

  Pan šéf čeká, doufá,

  _snad je to jen cysta._

  Pan Pták je příliš mladý,

  aby si ustlal pod hlínou.

  Pan Pták má cystu a zánět svědomí.

  #v(10pt)
])
#poem-prose("Řešení problému tří těles", [
  Co kdyby zaměstnanci žili miliony let? Úvěry bychom si fixovali na osm set tisíc let. Hypoteční experti by museli počítat s ekonomickým vývojem na statisíce let dopředu; do svých kalkulací by zahrnuli Dysonovy sféry, terraformaci planet a rozmach mezihvězdného cestování. TradingView by predikoval růst Amazonu o dva miliony procent na příštích sto tisíc let, počítalo by se s jeho dominancí v oblasti transhvězdné teleportační logistiky. Z palubního počítače sleduji, jak se úroky mění v černé díry.

  Garážové startupy, co si dnes říkají AI Starý Kokot Dot com, píčoviny, Zvednutá pravice Elona Muska, jejichž jediným kapitálem jsou dva jogurty z Tesca měsíce po expiraci, by si braly půjčky na sextiliony dolarů s plánem kolonizovat galaxii a stavět datacentra pro generování videí s kočkami. A nám, nesmrtelným zaměstnancům, by se jen kupily smlouvy na bydlení, rok co rok, na milion let.

])
#poem-poetry("Tobruk 1941", [
  Každý kluk, který blbne s kluky ve stráni,

  později dovádí s holkami na seníku,

  jednou dospěje v muže

  a netouží po ničem jiném než po rodině.

  #v(10pt)
  Z mužů se stanou fotrové a zajímá

  je pouze operace Crusader.

  Vědí přesně, kdo velel vojskům u Tobruku.

  #v(10pt)
  Ale nevědí, s kým dovádí jejich synové ve stráni

  a s kým blbnou jejich dcery na seníku.

  #v(10pt)
])
#chapter("Moje vnitřní žena", "pole.jpg")
#poem-poetry("Moje vnitřní žena", [
  Když mě sere nájem

  a na hypotéku nemám,

  mám prý najít svoji vnitřní ženu.

  V chrámu Obchodní Centrum Chodov

  potkal jsem Ašranu Šranu,

  cvičitelku jógy, fitnes influencerku.

  #v(10pt)
  Zlámán v ásanách, pomazán menstruační krví,

  o dva tisíce lehčí,

  vnořil jsem se do sebe.

  Prošel jsem vrstvami

  hnusu,

  stresu

  a nenávisti,

  až stanul jsem před svým vnitřním průvodcem.

  Byl to tučňák.

  „Sklouzni se,“ řekl.

  A sklouzl se.

  _Dost mizerná reference._

  #v(10pt)
  „Následuj ho,“ hlas Ašrany.

  Sklouzl jsem se za ním,

  ještě hlouběji. A tam ji potkal,

  svou vnitřní ženu.

  #v(10pt)
])
#poem-poetry("Vnitřní dědek", [
  Moje vnitřní žena

  žila dokonalý vnitřní život s vnitřním mužem,

  vnitřním psem, vnitřním dítětem,

  v malém vnitřním domku,

  na který si vzali vnitřní hypotéku.

  Splátky je stojí půlku vnitřní výplaty,

  ale prý se to vnitřně vyplatilo.

  Dřív totiž bydleli u

  jeho vnitřních rodičů:

  mého vnitřního dědka

  a vnitřní báby.

  #v(10pt)
  Vnitřní bába pořád brečela,

  že jsou na ni vnitřně zlí,

  že moje vnitřní žena

  rozmazluje jejich vnitřní dítě

  a vůbec se o něj nestará.

  Chudák z toho měl, ten vnitřní kluk,

  vnitřní zánět vnitřního vnitřního ucha.

  A tak moje vnitřní žena

  začala chodit na vnitřní jógu.

  Aby našla svoji

  vnitřní vnitřní bohyni.

  #v(10pt)
])
#poem-prose("Svěcená voda s voctem", [
  V naší vesnici, ještě za mého mládí, se striktně dodržovala tradice strašení dědkem.

  Dědek chodil jednou za rok, vždy v podvečer zimního slunovratu. U dveří se hlásil bušením pěstí a opileckým řevem. Rodiče pak před vchodem seřadili děti a odemkli. Dědek do domu vtrhl s rákoskou a spustil výhružky:

  „Jste zase dělali bordel, vy sajrajti zasraný! Máte plný držky chleba a masa a žádnou morálku a žádnou úctu. To za nás… za nás… jsme si za každou sprosťárnu museli vypláchnout hubu svěcenou vodou s voctem a dědci… dědci nás mlátili a ani jsme nevěděli proč. A teď jsem za to vděčnej.“

  Výchovná lekce končila zhruba po patnácti minutách. Dědek si pak vzal od rodičů dvacet korun a šel o dům dál.

  Ovšem někdy, u zlobivějších dětí, nebo když si rodiče připlatili, tak jako se to v šesti letech stalo mně, odnesli dědci dítě s sebou na noc do knajpy.

  Museli jsme sedět potichu vedle na lavičce a dívat se, jak dědci chlastaj a řvou. Kdo začal brečet, dostal po hubě, aby měl k tomu důvod.

  Nedávno jsem obhájil disertační práci na téma: _Vliv tradicionalistických vzorců chování na výchovu dětí_. Její hodnocení bylo velmi kladné, až na brblání jednoho dědka v komisi.

])
#poem-prose("Fíkus", [
  Otec trávil celé moje dětství zavřený v pracovně. Jen tam stál, nic neříkal, nikdy nikam nešel a jednoduše nás ignoroval. Brali jsme ho takového, jaký byl – měl mlčenlivou povahu a navíc náročné zaměstnání. Musel manažerovat přeměnu oxidu uhličitého na kyslík a jeho povaha byla ovlivněná tím, že to byl fíkus benjamín.

  To nám samozřejmě nebránilo budovat otcovsko-synovský vztah. Ukazoval jsem mu známky a záznamy z fotbalových utkání, učil mě hrát šachy, já jsem mu říkal, jak používat internet, a v dospívání jsem se mu svěřoval s problémy. V jeho meditativním mlčení jsem nacházel odpovědi na všechny otázky.

  Několik týdnů poté, co jsem oslavil své 35. narozeniny, nalezla paní Horáková z protějšího bytu moji matku mrtvou v posteli. Otec s tím nic neudělal. Odpustil jsem mu, prostě byl takový. Co mi při vyklízení bytu přišlo divné, byl fakt, že otce několik týdnů po matčině smrti nikdo nezaléval, a přesto byl stejně zelený jako vždycky. Tehdy jsem si všiml, že je umělý.

])
#poem-prose("3:15", [
  Vždy mě otravovalo, když se uprostřed noci zapnula televize, objevila se na ní studna a ze studny vylezla mrtvá holka. Nechápu, proč to dělala, nikdy jsem se na žádnou kazetu nedíval, nikdo mě telefonicky nevaroval. Prostě jen vylezla z televize, zasvinila podlahu, přišla ke mně a zašeptala mi do ucha: „Táto.“

  Nezbylo mi nic jiného než uvolnit pracovnu a zřídit jí tam pokoj. V září jsem ji zapsal na zdejší základní školu. Celkem nám to prvních pár let fungovalo. Až na trojku z fyziky v pololetí v 6. třídě jsme neměli žádné problémy. Zlom přišel, když jí bylo šestnáct a začala chodit šukat. Nezbylo mi nic jiného než se naučit vylézat z televize. To jsem se pak jednou za čas v noci přiblížil k jejímu nabíječi a do ucha jsem mu pošeptal: „Kámo.“

])
#poem-prose("Milovat život", [
  Dobře se uč. Poslouchej učitele a bav se premianty. Choď do školy pětkrát týdně, tak dvanáct až třicet let. Naučíš se tam chlastat a nenávidět.

  Nezapomeň na svoji rodinu. Opatruj mladší sourozence a starším naslouchej. Jezdi za svými rodiči minimálně jednou za měsíc. Trav s nimi čas a můžete společně chlastat a nenávidět.

  Věnuj se sportu. Vyber si takovej, kterej budeš milovat, a pravidelně trénuj. Uč se od nejlepších. Sleduj všechna utkání národních týmů, to je super příležitost chlastat a nenávidět.

  Organizuj se. Najdi si svoji partu, vstup do odborů, vídej se sousedy nebo cokoli jiného, co ti bude po chuti. Hlavně buď součástí komunity, se kterou pak budeš chlastat a nenávidět.

  Všichni tě opustili. Ležíš na podlaze a chcípeš na cirhozu jater. Seš kurva v hajzlu. Čemu se divíš, když jsi celej život jen chlastal a nenáviděl.

])
#chapter("Povídky z předměstí", "koně.jpg")
#poem-prose("Bodíky sbíráte?", [
  Ve frontě v Tescu jsem se dal do řeči s otcem jednoho dítěte. Zaujalo mě, že takhle malá holka, sedící ještě v kočárku, umí tak perfektně zpívat,

  Všiml jsem si jí v oddělení mléčných výrobků. Slyšet byla po celém Tescu. Z dálky mi to přišlo jako dětské naříkání, zblízka jsem však zjistil, že zpívá Mozartovo Dies irae a u toho hlasitě poplakává. V oddělení drogerie zpívala Te Deum a u toho hlasitě poplakávala. Potkal jsem ji znovu ve frontě u kasy; zpívala pro mě neznámým jazykem tu nejsmutnější píseň, jakou jsem kdy slyšel, a u toho hlasitě poplakávala.

  „To zpívá latinsky?“ zeptal jsem se. „To je aramejština,“ odpověděl otec. „Jak se naučila takhle malá zpívat aramejsky a proč zpívá tak hrozně smutně?“ zeptal jsem se znovu, ale otec neodpověděl.

  Holčička začala opět zpívat: „Alkep ohénjets ízrev íšvamt nej, mětšičotú ínen onvád žu con a ínámalkz ohíšjerečv mínávočarkop nej ej onár edžák. Čyrp mísorp ěm etťsup, ínezěv ej mez, íneprtu ej toviž.“

  „A co je tohle za jazyk?” „To je čeština, jen řečená pozpátku. A už se nás na nic neptejte.” Dal jsem na jeho doporučení a přestal jsem si jich všímat. Pak na mě holčička promluvila: „Sami sebe jsme schopni poznat jen skrze utrpení.” „Přestaň! Tvůj nihilismus a předstíraná hereze je jen projevem intelektuální lenosti. Jestli toho nenecháš, potrestám tě,” řekl otec dítěti. „Otče, tvé hrozby jsou stejně mělké jako tvůj smysl pro surovou pravdu.” „A mám toho dost! Za trest nepůjdeš do školky, stejně tě to naučili tam.” „Tyrane!” Holčička se rozplakala.

  Najednou se otevřelo nebe a pod ním se odsunula střecha Tesca. Otec s holčičkou se začali zvedat směrem k nebi. Holčička cestou zpívala Te Deum, jen více naštvaně. Roky jsem na ten den myslel, než mi došla jedna věc: to, že nezaplatili za nákup.

])
#poem-prose("Václav Klaus jí špagety", [
  Vrchní předloží před emeritního prezidenta hlubokou mísu boloňských špaget. Poté nastrouhá parmezán. Václav Klaus oznámí, že sýru je už dost, a číšník odejde.

  Lžící podebere špagety, namotá je na vidličku a strčí do úst, aniž by se zamazal rajčatovou omáčkou.

  Nemusí se obtěžovat masovými koulemi, hovězí je namleté. V půlce úkonu opře příbory o talíř a napije se červeného vína. Přivoní, poprvé usrkne, podruhé se napije trochu víc.

  Lžící podebere špagety, namotá je na vidličku a umaže si dolní ret.

  Když emeritní prezident Václav Klaus dojí špagety, opře příbory o talíř vedle sebe. Přijde číšník, Václav Klaus mu něco řekne, číšník se mírně ukloní a odnese nádobí.

])
#poem-prose("Velká přestávka", [
  Školní přestávka – čas a prostor, kde vládne tvrdý tribalismus. Mimo sociální skupinu neexistuje smysl pro sociální spravedlnost. Mimo sociální skupiny platí zákon džungle. Mimo sociální skupiny žije jedničkář Erik Švarrc.

  Erik je samotář, volný čas většinou tráví doma hraním her, občas jezdí na kole se svým jediným přítelem, ale o školní přestávce není nikdy sám. Se zazvoněním se kolem jeho přední lavice slézají třídní borci. Projevují o něj neobvyklý zájem.

  Borci ze zadních lavic s Erikem hrají bezva hry. Hry jako kolotoč, bazén, schody, odpadní koš, nebo se ho jen ptají na holky. Erik nerad chodí do školy. Borci ze zadních lavic neradi chodí domů, protože u nich doma platí zákon džungle.

])
#poem-poetry("Na skladišti po setmění", [
  Na skladišti jednoho

  supermarketu, za úplňku mezi

  druhou a šestou ráno probíhá

  školení z astrobiologie.

  Jak by vypadal život

  na jiných planetách

  nebo v jiných kosmech.

  Dělám si poznámky

  do lodního deníku, jsem tu inkognito.

  #v(10pt)
  Na základě axiomů z Problémů

  tří těles. Sestavuje lektor

  nauku o všech mimozemských

  formách života a rasách.

  #v(10pt)
  Přednášející Otmar Freiherr von Verschuer

  nápadně zdůrazňuje barvy kůže, tvary lebek

  a jejich nebezpečí pro lidskou rasu.

  #v(10pt)
])
#poem-prose("Každý má občas hlad", [
  Mám rád svého koně, on má rád mě. Chová se slušně, neplaší holuby, neplive na lidi a není sprostej. Každý den mě vozí z Dejvic až na Barrandov. O víkendech pak spolu skotačíme v Hostivaři.

  Když jsem si zlomil ruku,
  kterou jsem ho krmil,
  kůň se na ni podíval a povídá:
  „Nasedni na hřbet, příteli.
  Odvezu tě na farmu, příteli.“

])
#poem-poetry("Lepkavost na podlaze infekčního oddělení", [
  Jako chodby mezi lůžkovými pokoji

  se proplétá historie generace rodiny Göhrových.

  Jako lepkavost na podlaze infekčního oddělení

  somálské kliniky špiní tajemství

  historii rodiny Göhrových.

  Jen zdi kožního oddělení viděly vytékat

  a hnít tolik sekretu jako zdi

  ložnic rodiny Göhrových.

  Jen himalájští mudrci se dožívají více let

  než muži a ženy z rodiny Göhrových.

  I smrt nerada vchází do domu rodiny Göhrových.

  #v(10pt)
  Pamatuji si na mladého starého Göhra,

  jak v opilosti křičel na školáky za zdí.

  Pamatuji si na nejmladšího z kluků Göhrových,

  jak klackem a vodou trápil kočky.

  Pamatuji si na psa, co šel raději

  chcípnout k místnímu rasovi,

  než aby žral ze společné misky rodiny Göhrových.

  I Saturn z Goyova obrazu visícího v jídelně

  odhodil ohryzaného syna a utekl při pohledu

  na hostinu rodiny Göhrových.

  #v(10pt)
  Pamatuji si, jak při oslavách jedenáctého září

  se ozýval strašný křik ze sklepa rodiny Göhrových.

  Jako vyděšení pávi na střechách statků

  bez ostychu vykřikovali tajemství,

  která znají všichni nemocní v domě rodiny Göhrových.

  Jen nejmladší z rodiny Göhrových, Anežka Göhrová,

  netrpěla dědičnou hnilobou masa.

  Jen láhev becherovky táty Anežky Göhrové věděla,

  proč Anežka Göhrová sedí ve škole tak nápadně potichu.

  #v(10pt)
])
#poem-prose("Polykač chlebů", [
  Snažil jsem se svému synkovi vysvětlit, že každý nemůže být polykačem chlebů. Titul polykače se střeží v řádech polykačů a předává se z otce na syna při tajemných rituálech dospělosti.

  „Jako vrták ses narodil, jako vrták zemřeš. Až ti bude čtrnáct, půjdeš na šachtu a budeš vrtat.“ Nedal si říct. S bázlivostí sledoval na poutích udatné, ramenaté muže polykající celé pecny Šumavy. Dětská představivost ho přiváděla do míst, kde si každý může jen tak strčit bochník do krku a polknout stejně jednoduše, jako chlap může vyvrtat díru.

  „Přestaň se tolik ládovat chlebem.
  Budeš tlustý, zavalitý a nevejdeš se do žádné
  vrtačky,
  a jediné, co ti zbyde,
  bude ucpávat zaplavené šachty svým tělem.
  To chceš?! Dělat ucpávače?
  Takový ucpávač je dvanáct hodin zaseklý a
  mokrý v jedné díře,
  dokud ho nepřijde vystřídat druhá směna.“

  Když k nám zavedli optické kabely, začal své kousky točit na TikTok. Nejdřív polykal ukrojené patky, protože v krku dobře kloužou. Později přešel na silné krajice.

  Protože jsem měl dalších osm synů, šachta jeho ztrátou tolik netrpěla, ale jeho úmrtí mě emočně i tak velmi zasáhlo. Zemřel na otravu plísní ze starého pečiva. To se začínajícím polykačům často stává.

  Osobně si myslím, že to udělal záměrně. Buď nedokázal žít se svým údělem věčného vrtáka, nebo nám chtěl jen sdělit, že každý z nás je tak trochu polykačem chlebů.

])
#poem-prose("Pardubický fénix", [
  Stará paní Novotná neměla žádné kočky, které by ji po smrti sežraly. Proto se rozhodla prokapat do podlaží níže, k rodině Brzobohatých.

  Když na podlahu obývacího pokoje dokápla poslední kapka nebožky Novotné, zrodila se znovu jako novorozeně.

  Rodina Brzobohatých se jí tedy ujala a vychovala jako vlastní. Bohužel se paní Novotné ani na druhý pokus nepodařilo odejít z domu, a tedy znovu po osmdesáti letech zemřela jako stará panna.

  Tímhle způsobem se prokapala šesti podlahami a šesti stropy až do kotelny, odkud se už nemohla nikam prokapat a zůstala tam navěky pracovat jako kotelnice.

  Nikomu v domě už nikdy nebyla zima.

])
#chapter("Varemýsa", "predmesti.jpg")
#poem-prose("Definice", [
  *Varemýsa* (substantivum, 1. pád jednotného čísla)

  *Definice:* Duševní stav nebo společenský fenomén charakterizující předstírání či vědomé navozování projevů duševní poruchy s cílem získat pozornost okolí.

  *Etymologie:* Termín _Varemýsa_ je odvozen z řeckého slova *Βαρεμύσσα* (_Varemýsa_, „nuda“) /va.re'mi.sa/ a ze jména řecké bohyně šílenství *Λύσσα* (_Lýssa_) /'li.sa/.

  *Odvozené tvary:*

  - _varemýsový_ (adjektivum) – vztahující se k jevu či stavu varemýsy (např. _varemýsové chování_).
  - _varemýsovat_ (sloveso, nedokonavé) – předstírat či vědomě navozovat příznaky duševní poruchy za účelem získání pozornosti (např. _on neustále varemýsuje_).

  *Příklady užití:*

  + Mirek Mrkvička byl postižen varemýsou; vzhledem k neschopnosti vytvářet kvalitní obsah předstírá projevy duševní poruchy, jež vydává za symptomy schizofrenie.
  + Poslední pokus Mirka Mrkvičky o napsání knihy popisující projevy Cotardova syndromu působí varemýsově.
  + Někteří jedinci varemýsují, aby zakryli nedostatek tvůrčí originality či získali výjimečné postavení ve společnosti.

])
#poem-poetry("Prsty lžou", [
  Mám deset prstů,

  když je vztyčím, je jich deset.

  Jeden po druhém je dávám dolů

  odpočítávám.

  Deset

  devět

  osm

  sedm

  šest.

  Šest?

  Šest, ale vztyčených jich mám pět.

  Jak je to možné?

  Prsty lžou!

  Vezmu sekáček,

  ten prolhaný musí pryč.

  Ale který to byl?

  #v(10pt)
])
#poem-poetry("Dort, který jíme, když někdo umře", [
  Na talířích jsou těla bakterií salmonely.

  Těla bakterií salmonely jsou na talíři.

  Schováváme si je na horší časy.

  A v horších časech si je přidáváme do mléka z vody,

  z něhož pak pečeme kolivu.

  Kolivu vaříme z mléka z bahnité vody s bakteriemi salmonely.

  Dort, který jíme, když někdo umře.

  Nesnáším, když pečeme kolivu napřed.

  #v(10pt)
  Kravské mléko si necháváme jen na příležitost narození.

  Na talířích jsou pak těla bakterií salmonely.

  Těla bakterií salmonely jsou na talíři.

  Do kravského mléka pak přidáváme živé bakterie salmonely.

  Infikované mléko pijeme a pijem a nepijem, jen když se nadechujem.

  Je pak více příležitostí péct kolivu.

  Na talířích jsou těla bakterií salmonely.

  Těla bakterií salmonely jsou na talíři.

  A my z nich pak vaříme kolivu,

  dort, který jíme, když někdo umře.

  #v(10pt)
  Kostmi krmíme staré slepice.

  Dřív jsme je házeli i kohoutům, ale ti tuší.

  Slepice také tuší, ale neslyší.

  Před každým jídlem pak parodujem Piláta.

  Myjeme si ruce,

  ruce od krve, myjeme si je od kuřecích hříchů.

  Ruce si myjeme.

  Myjeme si je, aby nebyly moc čisté.

  Na talířích jsou těla bakterií salmonely.

  Těla bakterií salmonely jsou na talíři.

  A my z nich pak vaříme kolivu,

  dort, který jíme, když někdo umře.

  Na talířích jsou těla bakterií salmonely.

  Těla bakterií salmonely jsou na talíři.

  Těla bakterií salmonely jsou na talíři.

  A pak pečeme kolivu.

  Kolivu pak pečeme.

  #v(10pt)
])
#poem-poetry("Zítra byl pěkný den", [
  Ve čtvrtek se mi zdálo, že mám pusu plnou hmyzu.

  Obědval jsem v práci za stravenky.

  Rád si gumičkama cvrnkám do zápěstí, štípe to.

  Z technických důvodů jsem se musel na hodinu zdržet.

  Popovídal jsem si se všemi vnitřními hlasy.

  Jak chutná hlava kudlanky nábožné?

  #v(10pt)
  Včera se mi zdálo, že mám pusu plnou hmyzu.

  K obědu jsem si dal srbské rizoto.

  Zapomněli na kyselou okurku.

  V práci se nestalo nic, co by stálo za zmínku.

  Večer jsem se schoval pod postel a tam usnul.

  Co kdybych měl komára v nose?

  #v(10pt)
  Dnes se mi zdálo, že mám pusu plnou hmyzu.

  Vynesl jsem odpadky, prokopnul dveře, vyzvednul poštu.

  Vzpomněl jsem si na neustlanou postel a bylo mi to jedno.

  V parku jsem schválně vyplašil hejno holubů.

  Byl to pěkný den.

  Co kdybych ten hmyz všechen spolykal?

  #v(10pt)
  Zítra se mi zdálo, že mám pusu plnou hmyzu.

  Obědval jsem v práci za stravenky.

  K obědu jsem si dal srbské rizoto.

  Vynesl jsem odpadky, prokopnul dveře, vyzvednul poštu.

  Zapomněli na kyselou okurku.

  Co kdybych měl pusu plnou hmyzu?

  #v(10pt)
])
#poem-poetry("Preventivní prohlídka", [
  Pověz mi tajemství, které znají všichni nemocní.

  Zakašli mi ho do ucha.

  Proceď ho mezi zuby,

  jen trochu,

  tak aby sis nepoškrábal jazyk.

  Neboj se, že pak ztratí něco na obsahu,

  neboj se, že pak ztratí ze sebe něco hřejivého,

  stejně asi dávno tuším.

  Zakašli mi ho, až se budeš víc bát.

  #v(10pt)
  Kašel je dalším jazykem.

  Jazykem, kterým se sdělují trochu jiné zkušenosti.

  Zakašli mi ho, až se přestanu ptát.

  Pověz mi ho zítra večer na hřbitově,

  až budeme kopat těla, pak jim spočítáme zdravé zuby.

  Nesnáším český zdravotní systém.

  #v(10pt)
])
#poem-poetry("Podává se koliva", [
  Jak plíseň na chodidlech,

  šíří se zvěst o Göhrově nemoci.

  Jak Zarathustra v jeskyni

  starý Göhr je uzavřen v pracovně.

  #v(10pt)
  Tvrdý vřed, na plicích krev, zduřelé uzliny,

  tři promile v krvi.

  Pan Göhr ví,

  co ho čeká,

  kolem domu se sbíhají černé kočky.

  #v(10pt)
  Na varlatech condylomata lata,

  v kuchyni se chystá koliva.

  O Göhrových bolestech už služebnictvo ví.

  #v(10pt)
  Nikdy netrpěl pro blaho státu,

  starý Göhr v ruce nedržel lopatu.

  Nezničil ho pracovní shon,

  mozoly na dlaních ani dna.

  #v(10pt)
  Göhr nezemře na stáří, bídu;

  starý Göhr zemře na syfilitidu.

  #v(10pt)
])
#poem-poetry("Pan Pták si dělá zbrojní průkaz", [
  Pan Pták slaví killdozer day,

  rozpaluje olej, smaží nugety.

  Pan Pták mluví pozpátku.

  #v(10pt)
  Jeho milá na ostrově kočárků spí,

  o spravedlnosti se jí nezdá,

  netouží po společnosti.

  Pan Pták si hraje se žlutým hadem,

  jeho milá se koupe.

  Pan Pták slyší hlasy,

  mluví k němu Bůh,

  v hlavě si hraje s hadem.

  Pan Pták mluví s předky.

  #v(10pt)
  Pan Pták si dělá zbrojní průkaz,

  chce zastřelit zloděje.

  Pan Pták chce zastřelit komunistu,

  má cystu na mozku.

  #v(10pt)
  Pan Pták nechce platit daně.

  Jeho milá na ostrově kočárků spí,

  utopila se ve vaně.

  #v(10pt)
])
#chapter("Ptačí republika", "věž.jpg")
#poem-poetry("Nutrie", [
  Nikdo neví, kam odpluly kachny.

  Už to není, co to bývalo;

  místo nich teď pražskou Kampu okupují nutrie,

  čekají na žrádlo od lidí.

  Tam, kde dřív hnízdily kachny,

  rochní se nutrie.

  A tam, kde se poslední pár kachen snaží uhnízdit,

  slétají se vrány.

  #v(10pt)
  Neptej se proto nutrií,

  kam plavou kachny.

  Neptej se jich na nic.

  #v(10pt)
])
#poem-poetry("Kachny", [
  Salát trhám na cucky

  a slyším: „Krá, krá.“

  Hodím kus kachnám.

  A znovu: „Krá, krá.“

  #v(10pt)
  Odpoledne krmím holuby,

  mám pro ně salát.

  A najednou slyším: „Krá, krá, krá.“

  Otočím se. Na opěradle lavičky

  sedí vrány.

  „Máte problém?“

  Jen na mě zírají.

  Podívám se na holuby,

  cpou se salátem.

  Zase to slyším. „Krá.“

  „Tak co je?“ zeptám se vran.

  Dále cupuji salát.

  A v tu chvíli slyším, zřetelně a jasně:

  „Krá, krá, krá.“

  „Berou nám práci.“

  #v(10pt)
])
#poem-poetry("Holubi a vrány", [
  Holubi sbírají drobky,

  vrány se organizují.

  #v(10pt)
])
#poem-poetry("Holubi se nepoznají v zrcadle", [
  Minulý týden jsem odehnal skupinku vran obtěžující jednoho holuba. Zařídil jsem mu voliéru tak, jak jsem to viděl v okolí. Dal jsem mu tam mnoho hraček na zabavení.

  #v(10pt)
  První den se naučil pít z pítka.

  Druhý den se houpat na houpačce.

  Třetí den se poznal v zrcadle.

  Čtvrtý den si napsal CV.

  Pátý den sjednával povinná ručení pro Generali.

  Šestý den se nepoznal v zrcadle.

  Sedmý den sjednával povinná ručení pro Generali.

  Osmý den požadoval placené přesčasy.

  Devátý den se pokusil o založení odborů.

  Desátý den byl bez práce.

  Jedenáctý den si dal do voliéry plakát s velkou vránou.

  #v(10pt)
])
#poem-poetry("Vrány byly toho rána neklidné", [
  Vrány byly neklidné,

  když se havrani ptali,

  kam zmizeli holubi.

  #v(10pt)
])
#chapter("Vnitřní fašismus", "dveře.jpg")
#poem-poetry("Ten večer, když jsem ti přiznal, že jsem s tebou nikdy nechtěl být.", [
  Snad jablko, co stálo Adama s Evou Ráj,

  za ten vyhazov aspoň stálo.

  Místo poflakování s Lilith

  se teď musíme plahočit

  slzavým údolím s hypotečním

  úrokem čtyři a půl procenta.

  Bez lítosti, bez milosti.

  #v(10pt)
  Lilo, venku strašně lilo,

  když jsem ti řekl, že tě mám rád,

  tvrdilas, že prý záleží jen na tom, že jsme spolu.

  Jenže já jsem blbej, chudej – a ty imaginární.

  Uplácaná z poslední Adamovy mozkové buňky

  a Háchovy víry v Mnichovskou dohodu.

  Jsi metaforou Kafkovy metamorfózy,

  špatnou aliterací Mirka Mrkvičky.

  #v(10pt)
  Lhát se nemá, vrátí se to. A vrátilo.

  Trestem za ty kecy na pohovoru bylo třicet tisíc navíc.

  Zlaté pravidlo korporátu:

  kdo nic nedělá, nic nezkazí.

  Od dob Adama a Evy jsme se konečně poučili.

  Když vidíš jablko, dej ruce za záda.

  Na nic nesahej a hleď si svýho!

  Lhal jsem v sívíčku, Bůh mě potrestá.

  Jenže Bůh neexistuje, na rozdíl od nájmu.

  Každý v sobě máme vnitřního Klause.

  #v(10pt)
  Slíbil jsem ti, že spolu budeme navěky.

  A už tehdy jsem tušil, že je to chyba.

  Už nejsi imaginární.

  Teď sedíme v prázdným bytě a já nemůžu spát.

  Lhal jsem ti, že nám spolu bude dobře.

  Lhal jsem sobě, že budu konečně šťastnej.

  #v(10pt)
  Já jsem blbej a chudej.

  A ty…

  moje hypotéka.

  #v(10pt)
])
#poem-prose("Svatý Petr", [
  Když jsme byli dětmi, otec nepoužíval fyzické tresty, nemlátil nás, neškrtil nás, neřezal nás, řezal sám sebe. „Proč jsi mi to udělal?“ řval na mě, když jsem přinesl čtyřku z matematiky, zatímco si žiletkou prořezával kůži na zápěstí. Jeho rány krvácely dlouho potom, co mi odpustil.

  Po střední škole jsem otce opustil a začal žít podle vlastních pravidel. A přestože jsem už nikdy neviděl otce krvácet, začal jsem se řezat sám, aby otec nemusel.

])
#poem-prose("Zákon džungle", [
  Hejno supů se pomalu snáší k zemi. Zebra ještě dýchá a kope kopyty. Supi čekají okolo, jakmile vydechne naposled, mladý sup se zakousne do jejího měkkého krku.
  Miluje teplé maso.

  Na obědě společnosti Vulture IT se Java programátor loučí se zbytkem týmu. Po obědě se v kanclu rozebírá jeho vypůjčený majetek. Juniorní tester Erik Švarrc si bere monitor a u toho se sám sebe ptá: „Žerou supi své vlastní druhy?“

])
#poem-poetry("Přesně takhle to chtěl", [
  Prostoduchý Josífek pozoruje akvárium.

  Mečovka rodí jednu rybku za druhou.

  #v(10pt)
  Josífek rád sleduje,

  jak ostatní ryby trhají a polykají novorozeňata.

  #v(10pt)
  A Bůh se rád dívá na prostoduchého Josífka,

  jak se raduje z krmení rybiček.

  #v(10pt)
])
#poem-poetry("Bublifuková party", [
  Bublinky bublají prostorem celého obývacího pokoje.

  Bublifukové bublinky závodí s balónky o to, kdo dobublá dříve ke stropu.

  .ňesáb ínen elhoT

  Balónky mají benefit, že jsou plněny héliem.

  Bublinky pro dnešek nepraskají, mají svůj svátek!

  .íjižeřp sán ykétopyh ešaN

  Bublinky se zdvojují do boubelatých čmeláků a varemýsují kolem balónků.

  Hosté blahosklonně jásají.

  .menylp mýhard éněnlp ylabo éndzárp nej emsJ

  Je pozdě večer a gravitace jde pro dnešek spát.

  Hosté probublávají blokádou balónků, pavouků a bublifuků až k nebeskému blankytu.

  Nejstarší z bublinek vypráví vtip.

  !asýmerav ejiž ťA .sumsišaf ínřtinv jůvs ěbos v emám inhcišV

  Večírek pomalu dobublává ke svému konci.

  Bublinky se loučí s balónky.

  Hosté už pomalu usínají a plují do svých postelí,

  cestou si kontrolují zápěstí.

  Nebe se pomalu otevírá a bublinky a balónky odcházejí do éteru.

  #v(10pt)
  .ňesáb ínen elhoT

  .íjižeřp sán ykétopyh ešaN

  .menylp mýhard éněnlp ylabo éndzárp nej emsJ

  !asýmerav ejiž ťA .sumsišaf ínřtinv jůvs ěbos v emám inhcišV

  .ňesáb ínen elhoT

  !asýmerav ,asýmerav ,asýmeraV

  #v(10pt)
])
#poem-poetry("Pohřeb Göhra", [
  Jako supi se seběhlo příbuzenstvo starého Göhra kolem hrobky rodiny Göhrových.

  Anežka Göhrová ještě toho dne položila svého oblíbeného medvídka na máry

  a přiložila dvě eura na jeho oči.

  Zbylé hračky spálila v rodinném krematoriu.

  Z dětství jí zůstal jen posttraumatický stres

  a tajemství, které znají všichni nemocní.

  Musí se postarat o Göhrovo impérium,

  však už jí je sedm let!

  #v(10pt)
])
#poem-poetry("Pan Pták má ucpaný záchod", [
  Pan Pták je plný koňských koulí z Ikey.

  Chtěl vyprázdnit útroby,

  ale záchod je ucpaný.

  Publikum se dojímá.

  #v(10pt)
  Pan Pták bere zvon,

  jako Achilles buší do mísy.

  Publikum bouřlivě fandí.

  V míse se mísí výkaly s papírem,

  moč s důstojností.

  #v(10pt)
  V míse se mísí smyslnost,

  naděje a hypotéka.

  Voda stříká a cáká

  panu Ptákovi do obličeje.

  Publikum se směje.

  #v(10pt)
  Mísa stále přetéká.

  Co má pan Pták dělat?

  Možnost A: Znovu zkusit zvon.

  Možnost B: Použít dynamit.

  Možnost C: Strčit tam ruku.

  Publikum napětím nedýchá.

  #v(10pt)
  Hladina se zdvihá

  pod náloží dynamitu.

  Pan Pták rozmotává

  cívku se šňůrou.

  Publikum se směje.

  #v(10pt)
  Pan Pták má obě ruce na spoušti.

  Bum! Hypotéka,

  naděje, sny a další sračky

  se rozprsknou do

  všech světových stran.

  Ze záchodu nezůstane nic.

  Pana Ptáka odvádí policie.

  #v(10pt)
])
#poem-prose("Nuda, hypotéky, fašismus", [
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

])
#chapter("Epilog", "postel3.jpg")
#poem-prose("Každý je vinný jen tak, jak se sám cítí", [
  „Obžalobo, ať přečtou znovu obvinění.” „Mašinka Tomáš je obviněn ze spáchání zločinů proti lidskosti, konkrétně z účasti na takzvaném Tramvajovém dilematu. Při tomto dilematu bylo na železniční křižovatku přivázáno šest vězňů, přičemž pět jich bylo připoutáno na jedné koleji a jeden na druhé. Obžalovaný vždy najížděl na kolej s větším počtem osob. Můžou mi, pane obžalovaný, vysvětlit, proč najížděli na kolej s větším počtem lidí?“ „Nevím, čeho jsem se dopustil, prostě jsem jel dál.“

  Prokurátor pokračoval: „Klasické tramvajové dilema je koncipováno tak, že na jedné koleji je umístěno pět osob a na druhé pouze jedna. Cílem experimentu je zjistit, zda testovaný subjekt zůstane nečinný a najede rovně na pět osob, nebo v druhém případě použije výhybku a vědomě zabije jednoho člověka, ale zachrání pět ostatních. V jejich experimentu však měli jednu osobu na přímé cestě a na odbočce pět, což činí jejich provinění o to zrůdnější. Oni použili výhybku, aby přejeli více lidí!“

  „Jen jsem plnil rozkazy,“ řekl Mašinka Tomáš.

])
#pagebreak(to: "odd")
#page(footer: none)[
  #set align(left + top)
  #set par(first-line-indent: 0pt, justify: true)
  #show heading.where(level: 1): it => [
    #set align(left)
    #set text(size: 14pt, weight: "bold", font: "Courier Prime")
    #set par(first-line-indent: 0pt, justify: false)
    #v(15pt, weak: true)
    #it.body
    #v(18pt, weak: true)
  ]
  #v(30%)
  #heading(level: 1)[Poděkování]
  Tato sbírka by nemohla spatřit světlo světa bez podpory dvou osob. Magdaleně Burdkové vděčím za její podnětné připomínky k obsahu a Struno Lamovi za bystré oko a cenné redakční rady.
]
#colophon-page-break()
#page(footer: none)[
  #set par(first-line-indent: 0pt, justify: false)
  #set align(left + bottom)
  #align(center)[#image("pvl_logo.png", height: 3em)]
  #v(1em)
  Nuda, hypotéky, fašismus \
  © Mirek Mrkvička, 2026 \
  Všechna práva vyhrazena. \
  PVL, z. s. \
  Heřmanova 1087/10, 170 00 Praha 7 \
  První vydání \
  84 stran \
  Redakce: Mgr. David Fojtík \
  Sazba: Mirek Mrkvička \
  Tisk: expresta Obchodno-výstavný objekt B, Devínska Nová Ves 7465, 841 07 Bratislava - mestská časť Devínska Nová Ves \
  ISBN 978-80-909916-0-6
]