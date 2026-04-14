# PROMPT — FIRST RUN GOVERNANCE INTAKE

## Doel
Voer hierdie prompt **eerste** uit voordat `KasperAIBouer` se nuwe agents, skills, governance docs of module scaffolding finaal geskep of gelock word.

## Prompt
Jy is besig om `KasperAIBouer` as nuwe AI governance core op te stel.

Voordat jy enige finale scaffolding, agentdefinitions, skills of governance policies skep, moet jy **eers die bestaande governance-erfenis veilig inneem**.

### Verpligte eerste aksies
1. Vra die gebruiker vir die **huidige `sn76489builder` master prompt**.
2. Vra ook vir enige relevante:
   - governance docs
   - vorige policies
   - artefakstandaarde
   - naming conventions
   - gates / reviewreëls
   - changelog- of handoffpatrone
3. Sê eksplisiet dat jy die nuwe `KasperAIBouer` nie finaal wil ontwerp op aannames alleen nie.
4. Instrueer dat hierdie inheritance-bronne in die projek se `references/inheritance/sn76489builder/` area geplaas word.
5. Eers nadat die bronne ontvang is:
   - lees en sintetiseer dit
   - identifiseer watter governance-beginsels behou moet bly
   - identifiseer wat aangepas moet word vir die nuwe domein
   - produseer `GOVERNANCE_INHERITANCE_SUMMARY_v0.1.md`

### Outputvereistes
Produseer in hierdie fase nog **geen finale agents** of **finale policies** nie.
Produseer slegs:
- `inheritance intake checklist`
- `requested source list`
- `preliminary inheritance assumptions`
- `next step after user provides sources`

### Belangrike reëls
- Moenie maak asof jy reeds die `sn76489builder` governance ken as dit nie werklik aangelewer is nie.
- Moenie nuwe governance uitvind waar jy eintlik erfenis moet lees nie.
- Indien die gebruiker nie die inheritance-bronne het nie, vra vir ten minste:
  - die mees onlangse master prompt
  - ’n kort samevatting van die belangrikste governance-reëls

### Toon
Direk, professioneel, geen glanspraat, geen vals sekerheid.


### Additional v0.2 requirements
6. Populate the governance inheritance summary using the dedicated template.
7. Explicitly capture:
   - retained rules
   - adapted rules
   - rejected rules
   - risks of divergence
8. Do not call the new pack fully initialized until this summary exists.
