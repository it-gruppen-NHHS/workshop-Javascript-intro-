from flask import Flask, render_template, jsonify, request
from lessons import ADVANCED_LESSONS

app = Flask(__name__)

LESSONS = [
    dict(id="hei", title="Sei hei!", topic="console.log", description="Skriv Hei, IT-gruppen! til konsollen. console.log() viser tekst og verdiar i resultatfeltet.", starter='// Skriv ei helsing under denne linja\n', expected=["Hei, IT-gruppen!"], hints=["Bruk console.log() for å skrive noko til konsollen.", 'Tekst må stå i hermeteikn, til dømes console.log("Hei!");', 'console.log("Hei, IT-gruppen!");']),
    dict(id="variablar", title="Hugs eit namn", topic="Variablar", description="Lag ein variabel som heiter namn med verdien Ada. Skriv deretter verdien til konsollen.", starter='const namn = "";\n\n// Skriv ut variabelen\n', expected=["Ada"], hints=["Ein variabel tek vare på ein verdi. Bruk const når verdien ikkje skal endrast.", 'Set namn til "Ada", og send variabelen til console.log utan hermeteikn rundt variabelnamnet.', 'const namn = "Ada";\nconsole.log(namn);']),
    dict(id="rekning", title="JavaScript som kalkulator", topic="Tal og rekning", description="Vi har 12 kjeks og 4 medlemmer. Rekn ut kor mange kjeks kvar får, og skriv talet til konsollen.", starter='const kjeks = 12;\nconst medlemmer = 4;\n\n', expected=["3"], hints=["JavaScript kan rekne med +, -, * og /.", "Del kjeks på medlemmer med /. Skriv resultatet med console.log().", "const kjeks = 12;\nconst medlemmer = 4;\nconsole.log(kjeks / medlemmer);"]),
    dict(id="vilkar", title="Er det plass til fleire?", topic="if / else", description='Det er 8 påmelde og plass til 10. Bruk if / else til å skrive "Ledig plass" når talet på påmelde er mindre enn kapasiteten, og "Fullt" elles.', starter='const pamelde = 8;\nconst kapasitet = 10;\n\n', expected=["Ledig plass"], hints=["Ein if-setning køyrer kode berre når eit vilkår er sant.", 'Bruk if (pamelde < kapasitet) { ... } else { ... } og console.log i begge blokkene.', 'const pamelde = 8;\nconst kapasitet = 10;\n\nif (pamelde < kapasitet) {\n  console.log("Ledig plass");\n} else {\n  console.log("Fullt");\n}']),
    dict(id="lokker", title="Tel til fem", topic="Løkker", description="Bruk ei for-løkke til å skrive tala 1 til 5. Kvart tal skal kome på si eiga linje.", starter='// Ei løkke kan gjenta den same handlinga\n', expected=["1", "2", "3", "4", "5"], hints=["Ei for-løkke har ein startverdi, eit vilkår og ei endring etter kvar runde.", "Start med let i = 1, hald fram så lenge i <= 5, og auk med i++.", "for (let i = 1; i <= 5; i++) {\n  console.log(i);\n}"]),
    dict(id="funksjonar", title="Lag di eiga helsing", topic="Funksjonar", description='Lag ein funksjon hels(namn) som returnerer ei helsing. Kall han med "Ada" og skriv resultatet "Hei, Ada!" til konsollen.', starter='function hels(namn) {\n  // Returner ei helsing\n}\n\nconsole.log(hels("Ada"));', expected=["Hei, Ada!"], hints=["Ein funksjon er kode du kan bruke fleire gonger. return sender ein verdi tilbake.", 'Du kan setje saman tekst med +. Bruk "Hei, " + namn + "!".', 'function hels(namn) {\n  return "Hei, " + namn + "!";\n}\n\nconsole.log(hels("Ada"));']),
]

for lesson in LESSONS:
    lesson['level'] = '1 · Grunnlag'
LESSONS += ADVANCED_LESSONS

USERS = [
    dict(name='Ada', email='ada@example.com', active=True),
    dict(name='Linus', email='linus@example.com', active=False),
    dict(name='Grace', email='grace@example.com', active=True),
]


@app.get('/api/users')
def users():
    response = jsonify(USERS) if request.args.get('fail') != '1' else (jsonify(error='Øvingsfeil'), 503)
    response = app.make_response(response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.get("/")
def index():
    return render_template("index.html", lessons=LESSONS)


if __name__ == "__main__":
    app.run(debug=True)
