# REPO STRATEGY

## Hoofaanbeveling
Gebruik `KasperAIBouer` as hoofrepo / hoofproject root, met modules binne die projekstruktuur.

## Primêre doel
Hou:
- governance
- templates
- prompts
- agents
- modules
- outputs
saam, maar logies geskei.

## Aanbevole repo naam
`KasperAIBouer`

## Aanbevole root struktuur
- governance docs by root
- `agents/`, `skills/`, `prompts/`, `templates/`, `modules/`, `references/`, `output/`, `logs/`

## Branch model
Minimum:
- `main`
- `develop`
- feature branches soos:
  - `feature/taxidermy-kickoff`
  - `feature/source-ingestion`
  - `feature/infra-review`

## Commit styl
Gebruik eenvoudige, leesbare commit prefixes:
- `docs:`
- `governance:`
- `prompt:`
- `agent:`
- `module:`
- `risk:`
- `review:`

## Release styl
Gebruik tags soos:
- `v0.1-governance-pack`
- `v0.2-taxidermy-kickoff`
- `v0.3-mvp-scope-lock`

## Lokale padkonteks
User het aangedui dat Python en code GitHub repos woon onder:
`/Volumes/data1/Yandex.Disk.localized/michiele/Programmering/Python/python_normaal/github_python_normaal`

Gebruik daardie konteks vir lokale repo-plasing of mirror-workflow, maar hou OpenClaw se werkende workspace geskei onder:
`/Users/michiele/.openclaw/workspace/KasperAIBouer`


## v0.2 additions
Also see:
- `branching_and_tags.md`
- `commit_convention.md`
