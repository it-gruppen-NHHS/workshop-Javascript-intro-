# Kodeverkstaden

Ein nybyrjarverkstad i JavaScript for nye medlemmer i IT-gruppen. Python og Flask serverer sida og oppgåvene, medan JavaScript handterer kodekøyring, hint og framdrift i nettlesaren.

## Kom i gang

Krev Python 3.10 eller nyare. Køyr frå prosjektmappa:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python app.py
```

Opne http://127.0.0.1:5000. Stopp serveren med Ctrl+C. Utviklingsserveren er meint for lokal bruk.

## Slik fungerer det

- 16 oppgåver i fire nivå: grunnlag; funksjonar og lister; interaktive nettsider; API og miniprosjekt. Stien startar lett og sluttar med ein medlemstabell med feilhandtering.
- Tre gradvise hint per oppgåve. Det tredje viser ei full løysing.
- Køyr koden med knappen eller Ctrl+Enter (Cmd+Enter på Mac).
- Koden blir køyrd utan samanlikning med fasit. All utskrift blir vist. Køyringsfeil og console.error gir «Det er noko feil». Funksjonar må kallast frå koden din; knappar prøver du sjølv i førehandsvisinga.
- Kode, opna hint og fullførte oppgåver blir lagra lokalt i nettlesaren. Start på nytt nullstiller kode og hint for den aktive oppgåva, men beheld fullført-status.
- Konsolloppgåver køyrer i ein Web Worker som blir stoppa etter to sekund. DOM-oppgåver køyrer i ein iframe med sandbox="allow-scripts" og viser ei interaktiv førehandsvising. API-kontrollar får ti sekund. Ei synkron endelaus løkke i ein iframe kan likevel blokkere nettlesarfana; tidsgrensa garanterer ikkje avbrot der. Dette er ein lokal øvingsarena for eigen kode.
- Flask serverer fiktive medlemmer frå `/api/users`. `/api/users?fail=1` gir HTTP 503 for øving på feilhandtering. API-et tillèt lesing frå førehandsvisinga sin isolerte origin og treng ikkje eksterne tenester.

Grunnoppgåvene ligg i `app.py`, og dei vidaregåande i `lessons.py`. Kvar oppgåve har tre hint, og fasiten er siste hint. Utsjånaden ligg i `static/style.css`, og nettlesarfunksjonane i `static/app.js`. Google Fonts er valfritt; sida bruker reservefontar utan nettilgang.
