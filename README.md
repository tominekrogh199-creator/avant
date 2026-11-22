# AVANT · Featured Edit

Komplett magasinversjon 7, tilpasset https://avantedit.no/.

## Publisering

Filene skal ligge direkte i roten av `tominekrogh199-creator/avant`. Last opp innholdet i ZIP-filen, ikke ZIP-filen eller en ekstra overmappe. Ta med `.github/workflows/pages.yml`: den er oppdatert slik at alle artikkelsider, merkeoversikten og data blir med. På Mac kan skjulte filer vises med Cmd+Shift+punktum.

En endring på `main` starter publisering via GitHub Actions. `CNAME` beholder avantedit.no. Kontroller grønn status under Actions før du sjekker domenet. ZIP-filen i seg selv er ikke en publisering.

## Åpne lokalt

Pakk ut og åpne `index.html`. Alle bilder og video følger med. Google Fonts krever internett; ellers brukes reservefonter.

## Struktur

- `index.html` og `featured.html`: magasinets forside.
- `featured-sen-oslo.html` og `featured-klyo.html`: artiklene.
- `saker.html`, `merker.html`, `om-avant.html`: arkiv, merkeoversikt og kontakt.
- `assets/`, `css/`, `js/`: medier, utforming og funksjoner.
- `data/magasin.json`: merker og artikler.
- `editor/` og `scripts/`: maler, generator og kontroll.

## Redigering

Oppdater innholdsregisteret og legg nye artikler og bilder på plass. Kjør fra prosjektroten:

```bash
python3 scripts/build_magazine.py
python3 scripts/check_site.py
```

Generatoren oppdaterer forsiden, arkivet, merkeoversikten, Om AVANT og felles artikkelnavigasjon. Artikkeltekstene redigeres i sine HTML-filer. Endringer i genererte sider må gjøres i malene eller generatoren for å overleve neste kjøring. Ved godkjente endringer i Klyos intervjusvar må kontrollens referanse i `scripts/interview-baseline.json` også oppdateres.

Denne pakken beholder bildet med marineblå blazer og gul sløyfe, og har ingen lenker til merkenes ikke-eksisterende nettsider. Kontaktskjemaet åpner et e-postutkast og sender ingenting automatisk. Delingsmetadata peker til avantedit.no, og søkemotorindeksering er tillatt i denne publiseringspakken.
