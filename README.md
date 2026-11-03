# AVANT

**Nye norske merker. Unge skapere. Ett fellesskap.**

Nettsiden til AVANT (tidligere KANT) – et studentprosjekt fra BI Oslo. AVANT løfter små og nye norske motemerker og unge skapere, og bygger et kreativt fellesskap for unge.

- Live: https://avantedit.no/
- Featured Edit: https://avantedit.no/featured.html
- Instagram: [@avant_edit](https://www.instagram.com/avant_edit/) · TikTok: [@avant_edit](https://www.tiktok.com/@avant_edit)

Siden er ren HTML, CSS og JavaScript (ingen byggesteg). Hver gang noe endres på `main`, publiseres siden automatisk på nytt med GitHub Actions (`.github/workflows/pages.yml`). Det tar som regel 1–2 minutter.

## Filer

| Fil | Hva |
| --- | --- |
| `index.html` | Forside: hero, Featured Edit, Om oss, Vår visjon, Kontakt |
| `featured.html` | Featured Edit – det digitale magasinet |
| `featured.json` | **Alle plaggene i Featured Edit** – det er bare denne du trenger å endre |
| `js/config.js` | E-post og lenker til Instagram/TikTok |
| `assets/plagg/` | Bilder av plagg |
| `css/style.css` | Design |

## Slik legger du til et nytt plagg

Alt kan gjøres direkte i GitHub i nettleseren – du trenger ikke installere noe.

1. **Last opp bildet.** Gå til repoet på GitHub → åpne mappen `assets/plagg` → **Add file → Upload files**. Gi bildet et enkelt navn uten mellomrom og æøå, f.eks. `merkenavn-jakke.jpg`. Stående bilde (4:5) blir finest. Prøv å holde bildet under ca. 500 kB. Trykk **Commit changes**.
2. **Åpne `featured.json`** og trykk på blyanten (✏️ *Edit this file*).
3. **Kopier malen.** Øverst i filen ligger `_mal_for_nytt_plagg`. Kopier alt mellom `{` og `}` og lim det inn som et nytt element i listen `"plagg": [ ... ]`. Legg det **øverst** i listen hvis det nyeste plagget skal vises først. Husk komma mellom elementene.
4. **Fyll inn feltene:**
   - `id` – kort og unik, bare små bokstaver, tall og bindestrek (f.eks. `merkenavn-jakke`). Denne blir lenken: `https://avantedit.no/featured.html#merkenavn-jakke`
   - `utgave` – f.eks. `Utgave 01`
   - `plagg`, `merke`, `skaper` (Instagram-navnet til skaperen, kan stå tomt `""`), `tekst`
   - `bilde` – stien til bildet, f.eks. `assets/plagg/merkenavn-jakke.jpg`, og `bildeAlt` – en kort beskrivelse av bildet
   - `merkeNettside`, `merkeInstagram`, `innleggInstagram`, `innleggTiktok` – fulle lenker som starter med `https://`. Tomme felt (`""`) vises ikke.
5. **Fjern plassholdere** du ikke vil ha lenger (elementene med `"plassholder": true`). Du kan også skjule et plagg midlertidig med `"vis": false`.
6. Trykk **Commit changes**. Etter 1–2 minutter er plagget live. Sjekk gjerne fanen **Actions** – grønn hake betyr at det er publisert. Rødt kryss betyr som regel en skrivefeil i JSON (manglende komma eller anførselstegn).
7. **Lenk begge veier:** Lim inn plagglenken (`featured.html#din-id`) i Instagram-/TikTok-innlegget (eller i bio-lenken), og lim inn lenken til innlegget i `innleggInstagram` / `innleggTiktok`. På nettsiden har hvert plagg en «Kopier lenke»-knapp.

Eksempel på et ferdig plagg:

```json
{
  "id": "merkenavn-jakke",
  "utgave": "Utgave 01",
  "plagg": "Navn på plagget",
  "merke": "Navn på merket",
  "skaper": "@skaperens-brukernavn",
  "tekst": "To–tre setninger om plagget og merket.",
  "bilde": "assets/plagg/merkenavn-jakke.jpg",
  "bildeAlt": "Skaperen har på seg jakken utendørs i Oslo.",
  "merkeNettside": "https://...",
  "merkeInstagram": "https://www.instagram.com/...",
  "innleggInstagram": "https://www.instagram.com/p/...",
  "innleggTiktok": ""
}
```

> Tips: Lim inn hele filen i [jsonlint.com](https://jsonlint.com) før du lagrer hvis du er usikker på om kommaene stemmer.

## Instagram og TikTok

AVANT heter `@avant_edit` på begge. Lenkene står direkte i `index.html` og `featured.html` (kontakt, Om oss og bunnteksten), og URL-ene ligger også i `js/config.js`. Bytter dere brukernavn, oppdater `@avant_edit`-teksten i HTML-en og URL-ene i `js/config.js`.

## Domene

Siden ligger på https://avantedit.no/ (filen `CNAME`). DNS hos domeneregistraren må peke til GitHub Pages:

- `@` (apex) A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- `@` (apex) AAAA (valgfritt): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
- `www` CNAME: `tominekrogh199-creator.github.io`

Når DNS virker: slå på «Enforce HTTPS» under Settings → Pages.

## Bilder

Stemningsbildene i `assets/img/` er AI-genererte. Bytt dem gjerne ut med egne bilder senere.

---

© 2026 AVANT · Et studentprosjekt fra BI Oslo · Kontakt: Tominekrogh199@gmail.com
