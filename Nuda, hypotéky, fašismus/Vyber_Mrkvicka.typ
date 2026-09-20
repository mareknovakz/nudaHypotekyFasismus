#set page(
  width: 110mm + 5mm,
  height: 180mm + 5mm,
  margin: (inside: 65pt + 2.5mm, outside: 45pt + 2.5mm, top: 60pt + 2.5mm, bottom: 60pt + 2.5mm),
  footer-descent: 20pt,
  footer: none
)
#let default_footer() = context {
  set text(size: 9pt, font: "EB Garamond")
  let page_num = counter(page).at(here()).first()
  if calc.even(page_num) [ #align(left)[#page_num] ] else [ #align(right)[#page_num] ]
}
#set text(font: "EB Garamond", size: 10.5pt, lang: "cs", hyphenate: false)
#set par(justify: true, leading: 8.5pt)
#show heading.where(level: 1): it => [
  #set align(center + horizon)
  #set text(size: 20pt, weight: "bold", font: "EB Garamond")
  #set par(justify: false)
  #it.body
]

#show heading.where(level: 2): it => [
  #set align(left)
  #set text(size: 15pt, weight: "bold", font: "EB Garamond")
  #set par(first-line-indent: 0pt, justify: false)
  #v(20pt, weak: true)
  #it.body
  #v(15pt, weak: true)
]
#set align(center + horizon)
#text(size: 24pt, weight: "bold", font: "EB Garamond")[Nuda, hypotéky, \ fašismus]
#v(1.5em)
#text(size: 14pt, style: "italic", font: "EB Garamond")[Autorský výběr básní]
#v(2em)
#text(size: 16pt, weight: "medium", font: "EB Garamond")[Mirek Mrkvička]
#pagebreak()
#set page(footer: none)
#set align(center + horizon)
#text(size: 16pt, weight: "bold", font: "EB Garamond")[Úvod]
#v(1.5em)
#set align(left + horizon)
#set par(first-line-indent: 1.5em, leading: 10pt)
#text(size: 11.5pt, style: "italic", font: "EB Garamond")[Dobrý večer, jsem Mirek Mrkvička a~přečtu vám něco ze své sbírky Nuda, hypotéky, fašismus. Sbírku píšu, protože věřím, že každý z~nás má v~sobě kousek svého vnitřního fašismu a~že lidská nátura má přirozené sklony k~nekrofilnímu sadismu.]
#pagebreak(to: "odd")
#set page(footer: default_footer())
#set align(left + top)
#heading(level: 2, [Pan Pták si vzal sick day])
#set par(first-line-indent: 0pt, justify: true, leading: 8.5pt)
  #v(5pt)
  Pan Pták si vzal sick day, \
  má cystu na ledvině, \
  myslel, že má kameny. \
  Pod nánosy hlíny \
  Ptákova matka spí. \
  Pospěšme k~místu, \
  kde spí zaměstnanci. \
  Ptákova milá \
  na ostrově kočárků spí, \
  nevzala si sick day. \
  #v(16pt)
  Z~kostí padlých \
  pěstujeme nové kancly. \
  Pan Pták má cystu ve výkazu práce. \
  Sedí doma, nahmatává si bulky. \
  Většinou nejsou zhoubné. \
  Pod nánosy hlíny \
  Ptákova matka spí. \
  #v(16pt)
  Doktor Ptákovu cystu prohlíží. \
  Hmatá, lechtá, hledá ledvinu. \
  Cysta svědí, pálí, čas letí. \
  Pan šéf čeká, doufá, \
  _snad je to jen cysta._ \
  Pan Pták je příliš mladý, \
  aby si ustlal pod hlínou. \
  Pan Pták má cystu a~zánět svědomí. \
  #v(16pt)
#pagebreak(weak: true)
#heading(level: 2, [Přesně takhle to chtěl])
#set par(first-line-indent: 0pt, justify: true, leading: 8.5pt)
  #v(5pt)
  Prostoduchý Josífek pozoruje akvárium. \
  Mečovka rodí jednu rybku za druhou. \
  #v(16pt)
  Josífek rád sleduje, \
  jak ostatní ryby trhají a~polykají novorozeňata. \
  #v(16pt)
  A~Bůh se rád dívá na Josífka, \
  jak se raduje z~krmení rybiček. \
  #v(16pt)
#pagebreak(weak: true)
#heading(level: 2, [Pan Pták si dělá zbrojní průkaz])
#set par(first-line-indent: 0pt, justify: true, leading: 8.5pt)
  #v(5pt)
  Pan Pták slaví killdozer day, \
  rozpaluje olej, smaží nugety. \
  Pan Pták mluví pozpátku. \
  #v(16pt)
  Jeho milá na ostrově kočárků spí, \
  o~spravedlnosti se jí nezdá, \
  netouží po společnosti. \
  Pan Pták si hraje se žlutým hadem, \
  jeho milá se koupe. \
  Pan Pták slyší hlasy, \
  mluví k~němu Bůh, \
  v~hlavě si hraje s~hadem. \
  Pan Pták mluví s~předky. \
  #v(16pt)
  Pan Pták si dělá zbrojní průkaz, \
  chce zastřelit zloděje. \
  Pan Pták chce zastřelit komunistu, \
  má cystu na mozku. \
  #v(16pt)
  Pan Pták nechce platit daně. \
  Jeho milá na ostrově kočárků spí, \
  utopila se ve vaně. \
  #v(16pt)
#pagebreak(weak: true)
#heading(level: 2, [Bodíky sbíráte?])
#set par(first-line-indent: 0pt, justify: true, leading: 8.5pt)
  #v(5pt)
  Ve frontě v~Tescu jsem se dal do řeči s~otcem jednoho dítěte. Zaujalo mě, že takhle malá holka, sedící ještě v~kočárku, umí tak perfektně zpívat, \
  #v(16pt)
  Všiml jsem si jí v~oddělení mléčných výrobků. Slyšet byla po celém Tescu. Z~dálky mi to přišlo jako dětské naříkání, zblízka jsem však zjistil, že zpívá Mozartovo Dies irae a~u~toho hlasitě poplakává. V~oddělení drogerie zpívala Te Deum a~u~toho hlasitě poplakávala. Potkal jsem ji znovu ve frontě u~kasy; zpívala pro mě neznámým jazykem tu nejsmutnější píseň, jakou jsem kdy slyšel, a~u~toho hlasitě poplakávala. \
  #v(16pt)
  „To zpívá latinsky?“ zeptal jsem se. „To je aramejština,“ odpověděl otec. „Jak se naučila takhle malá zpívat aramejsky a~proč zpívá tak hrozně smutně?“ zeptal jsem se znovu, ale otec neodpověděl. \
  #v(16pt)
  Holčička začala opět zpívat: „Alkep ohénjets ízrev íšvamt nej, mětšíčotú ínen onvád žu con a~ínámalkz ohíšjerečv míňavočarkop nej ej onár edžák. Čyrp mísorp ěm etťsup, ínezěv ej mez, íneprtu ej toviž.“ \
  #v(16pt)
  „A~co je tohle za jazyk?“ \
  „To je čeština, jen řečená pozpátku. A~už se nás \
  na nic neptejte.“ \
  Dal jsem na jeho doporučení a~přestal jsem si \
  jich všímat. Pak na mě holčička promluvila: \
  „Sami sebe jsme schopni poznat jen skrze \
  utrpení.“ \
  „Přestaň! Tvůj nihilismus a~předstíraná hereze je \
  jen projevem intelektuální lenosti. Jestli toho \
  nenecháš, potrestám tě,“ řekl otec dítěti. \
  „Otče, tvé hrozby jsou stejně mělké jako tvůj \
  smysl pro surovou pravdu.“ \
  „A~mám toho dost! Za trest nepůjdeš do školky, \
  stejně tě to naučili tam.“ \
  „Tyrane!“ Holčička se rozplakala. \
  #v(16pt)
  Najednou se otevřelo nebe a~pod ním se odsunula střecha Tesca. Otec s~holčičkou se začali zvedat směrem k~nebi. Holčička cestou zpívala Te Deum, jen více naštvaně. Roky jsem na ten den myslel, než mi došla jedna věc: To, že nezaplatili za nákup. \
  #v(16pt)
#pagebreak(weak: true)