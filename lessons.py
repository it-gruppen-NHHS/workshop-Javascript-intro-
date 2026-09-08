"""Oppgåver som byggjer vidare frå grunnlag til ei lita API-nettside."""

ADVANCED_LESSONS = [
    dict(id='gjennomsnitt', level='2 · Funksjonar og lister', title='Frå Python til JavaScript', topic='Parametrar og return',
         description='I Python: def average(a, b): return (a + b) / 2. Skriv den tilsvarande JavaScript-funksjonen average(a, b). Han skal returnere gjennomsnittet, også for negative tal. Du kan bruke function eller ein pilfunksjon.',
         starter='// Lag average(a, b) her\n', expected=[],
         hints=['Ein funksjon tek imot parameterar og sender tilbake ein verdi med return.', 'Bruk parentes rundt a + b før du deler på 2. Ei pilfunksjon kan skrivast const average = (a, b) => ...;', 'const average = (a, b) => (a + b) / 2;']),
    dict(id='partal', level='2 · Funksjonar og lister', title='Partal eller oddetal?', topic='Modulo og ternær operator',
         description='Lag checkNumber(n) som returnerer "Partal" for partal og "Oddetal" elles. Bruk % for å finne resten etter deling. Prøv gjerne den ternære operatoren vilkår ? verdiA : verdiB.',
         starter='const checkNumber = (n) => {\n  // Returner rett tekst\n};', expected=[],
         hints=['Eit partal har rest 0 når det blir delt på 2.', 'Test n % 2 === 0. Med ternær operator kjem svaret for sant før kolon og svaret for usant etter.', 'const checkNumber = (n) => n % 2 === 0 ? "Partal" : "Oddetal";']),
    dict(id='sortering', level='2 · Funksjonar og lister', title='Rydd i poenglista', topic='filter · sort · forEach',
         description='Lag visPoeng(poeng). Vel berre tal større enn 3, sorter dei numerisk frå minst til størst, og skriv kvart tal med console.log. Ikkje endre den opphavlege lista.',
         starter='function visPoeng(poeng) {\n  // Filtrer, sorter og skriv ut\n}', expected=['4','10','20','5','8'],
         hints=['filter lagar ei ny liste. sort utan samanlikningsfunksjon sorterer tala som tekst.', 'Bruk filter(n => n > 3), deretter sort((a, b) => a - b), og forEach for å skrive ut.', 'function visPoeng(poeng) {\n  poeng.filter(n => n > 3)\n    .sort((a, b) => a - b)\n    .forEach(n => console.log(n));\n}']),
    dict(id='medlemsliste', level='2 · Funksjonar og lister', title='Finn aktive medlemmer', topic='Objekt · filter · map · every',
         description='Lag aktiveNamn(medlemmer) som returnerer namna til aktive medlemmer, alfabetisk sortert med localeCompare(..., "nb"). Lag også alleAktive(medlemmer) som returnerer true berre når alle er aktive. For ei tom liste skal alleAktive returnere true, slik every gjer.',
         starter='function aktiveNamn(medlemmer) {\n}\n\nfunction alleAktive(medlemmer) {\n}', expected=[],
         hints=['Kvart medlem er eit objekt med namn og aktiv. filter vel objekt, medan map hentar ut namna.', 'Kjed filter(m => m.aktiv), map(m => m.namn) og sort((a, b) => a.localeCompare(b, "nb")). Bruk every i den andre funksjonen.', 'function aktiveNamn(medlemmer) {\n  return medlemmer.filter(m => m.aktiv).map(m => m.namn)\n    .sort((a, b) => a.localeCompare(b, "nb"));\n}\n\nfunction alleAktive(medlemmer) {\n  return medlemmer.every(m => m.aktiv);\n}']),
    dict(id='domtekst', level='3 · Interaktive nettsider', title='Endre innhaldet på sida', topic='DOM · textContent', mode='dom',
         description='HTML-en under er ferdig. Finn avsnittet med id="tekst" og endre teksten til "Velkomen til IT-gruppen!" med JavaScript. Sjå resultatet i førehandsvisinga.',
         html='<p id="tekst">Dette er ein tekst</p>', starter='// Finn elementet og endre teksten\n',
         hints=['document representerer HTML-sida. Eit element kan finnast ved hjelp av id-en sin.', 'Bruk document.getElementById("tekst"), og set textContent på elementet.', 'const el = document.getElementById("tekst");\nel.textContent = "Velkomen til IT-gruppen!";']),
    dict(id='domstil', level='3 · Interaktive nettsider', title='Gi teksten ein ny stil', topic='DOM · style', mode='dom',
         description='Gjer teksten blå (blue), bakgrunnen gul (yellow) og skriftstorleiken 24px. Bruk style på elementet med id="tekst". CSS-eigenskapen background-color heiter backgroundColor i JavaScript.',
         html='<p id="tekst">JavaScript kan endre utsjånaden!</p>', starter='const el = document.getElementById("tekst");\n',
         hints=['style lar deg setje CSS-verdiar frå JavaScript. Verdiane er tekststrengar.', 'Set el.style.color, el.style.backgroundColor og el.style.fontSize. Hugs px på storleiken.', 'const el = document.getElementById("tekst");\nel.style.color = "blue";\nel.style.backgroundColor = "yellow";\nel.style.fontSize = "24px";']),
    dict(id='domklikk', level='3 · Interaktive nettsider', title='La eit klikk gjere jobben', topic='addEventListener · querySelectorAll', mode='dom',
         description='Når knappen blir klikka, skal alle tre avsnitta med class="msg" få teksten "Oppdatert!". Teksten skal vere uendra før klikket.',
         html='<p class="msg">Første melding</p><p class="msg">Andre melding</p><p class="msg">Tredje melding</p><button id="btn">Endre tekst</button>', starter='// Legg ein klikklyttar på knappen\n',
         hints=['Legg handlinga inni ein funksjon som blir køyrd ved click, i staden for å køyre henne med ein gong.', 'Bruk addEventListener("click", () => { ... }). Inni lyttaren: querySelectorAll(".msg") og forEach.', 'document.getElementById("btn").addEventListener("click", () => {\n  document.querySelectorAll(".msg").forEach(el => {\n    el.textContent = "Oppdatert!";\n  });\n});']),
    dict(id='teljar', level='3 · Interaktive nettsider', title='Bygg ein klikk-teljar', topic='Tilstand · funksjonar · hendingar', mode='dom',
         description='Pluss-knappen skal auke teljaren med 1 for kvart klikk. Nullstill-knappen skal setje han tilbake til 0. Oppdater avsnittet #count etter kvart klikk.',
         html='<p id="count">0</p><button id="plus">+1</button> <button id="resetCount">Nullstill</button>', starter='let count = 0;\n// Kople til begge knappane\n',
         hints=['Bruk let for ein verdi som endrar seg. Begge knappane må bruke den same variabelen.', 'Auk count med count++ i pluss-lyttaren. Set count = 0 i nullstill-lyttaren. Oppdater textContent begge stader.', 'let count = 0;\nconst output = document.getElementById("count");\ndocument.getElementById("plus").addEventListener("click", () => {\n  count++;\n  output.textContent = count;\n});\ndocument.getElementById("resetCount").addEventListener("click", () => {\n  count = 0;\n  output.textContent = count;\n});']),
    dict(id='api', level='4 · API og miniprosjekt', title='Hent medlemmer frå eit API', topic='fetch · async / await · JSON', mode='dom',
         description='Lag async function lastBrukarar(url). Hent URL-en med fetch, sjekk response.ok og les JSON med await response.json(). Vis "Lasta 3 brukarar" i #msg ved suksess og "Kunne ikkje hente data" ved feil. Flask sitt øvings-API gir ei liste med name, email og active. API_URL er ferdig definert.',
         html='<p id="msg">Klar til å hente data</p>', starter='async function lastBrukarar(url) {\n  const msg = document.getElementById("msg");\n  // Hent data med try / catch\n}',
         hints=['fetch og json() er asynkrone. Bruk await inni ein async-funksjon og fang feil med try / catch.', 'fetch kastar ikkje automatisk ein feil ved HTTP 503. Skriv if (!res.ok) throw new Error(...), og bruk users.length i meldinga.', 'async function lastBrukarar(url) {\n  const msg = document.getElementById("msg");\n  try {\n    const res = await fetch(url);\n    if (!res.ok) throw new Error("HTTP-feil");\n    const users = await res.json();\n    msg.textContent = `Lasta ${users.length} brukarar`;\n  } catch (error) {\n    msg.textContent = "Kunne ikkje hente data";\n  }\n}']),
    dict(id='apitabell', level='4 · API og miniprosjekt', title='Miniprosjekt: medlemstabell', topic='API · DOM · lister · feilhandtering', mode='dom',
         description='Bygg async function lastBrukarar(url) vidare: Hent API-data og lag ei rad per brukar i #userTable med namn, e-post og status (Aktiv eller Inaktiv). Vis "Lasta 3 brukarar" i #msg. Tøm gamle rader før kvar lasting, og vis "Kunne ikkje hente data" ved feil. Bruk createElement og textContent.',
         html='<p id="msg">Klar til å hente data</p><table><thead><tr><th>Namn</th><th>E-post</th><th>Status</th></tr></thead><tbody id="userTable"></tbody></table>', starter='async function lastBrukarar(url) {\n  const tableBody = document.getElementById("userTable");\n  const msg = document.getElementById("msg");\n  // Kombiner API-kall, løkke og DOM\n}',
         hints=['Del problemet opp: tøm tabellen, hent JSON, lag rader, oppdater meldinga. Bygg vidare på førre oppgåve.', 'Bruk tableBody.replaceChildren(). For kvar brukar lagar du ein tr, og ein td for kvar av dei tre verdiane. Bruk user.active ? "Aktiv" : "Inaktiv".', 'async function lastBrukarar(url) {\n  const tableBody = document.getElementById("userTable");\n  const msg = document.getElementById("msg");\n  tableBody.replaceChildren();\n  try {\n    const res = await fetch(url);\n    if (!res.ok) throw new Error("HTTP-feil");\n    const users = await res.json();\n    users.forEach(user => {\n      const row = document.createElement("tr");\n      [user.name, user.email, user.active ? "Aktiv" : "Inaktiv"].forEach(value => {\n        const cell = document.createElement("td");\n        cell.textContent = value;\n        row.appendChild(cell);\n      });\n      tableBody.appendChild(row);\n    });\n    msg.textContent = `Lasta ${users.length} brukarar`;\n  } catch (error) {\n    msg.textContent = "Kunne ikkje hente data";\n  }\n}']),
]

# Synlege døme som elevane sjølve kan endre og køyre.
EXAMPLES = {
    'gjennomsnitt': 'console.log(average(2, 8));',
    'partal': 'console.log(checkNumber(7));',
    'sortering': 'visPoeng([20, 2, 10, 4, 3]);',
    'medlemsliste': 'const medlemmer = [{namn: "Ada", aktiv: true}, {namn: "Linus", aktiv: false}];\nconsole.log(aktiveNamn(medlemmer));\nconsole.log(alleAktive(medlemmer));',
    'api': 'await lastBrukarar(API_URL);',
    'apitabell': 'await lastBrukarar(API_URL);',
}
for lesson in ADVANCED_LESSONS:
    if lesson['id'] in EXAMPLES:
        example = EXAMPLES[lesson['id']]
        lesson['starter'] += '\n\n' + example
        lesson['hints'][2] += '\n\n' + example
        lesson['description'] += ' Køyr funksjonen sjølv, til dømes: ' + example
