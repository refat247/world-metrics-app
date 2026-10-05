# World Metrics App

**Role:** PRODUCT CANONICAL  
**Version:** 1.0.3

World Metrics is a focused, offline-first country-statistics explorer for people who want a fast global snapshot rather than a full statistical research system.

**Core user promise:** pick a country and, within seconds, see where it sits globally across five headline indicators — GDP per capita, life expectancy, population, CO₂ per capita, and internet access — with reporting year, global rank, map context, and an offline-capable mobile experience.

## Why this app exists

World Bank and Our World in Data already provide much broader statistical systems. World Metrics does **not** try to replace them. Its v1 advantage is deliberate compression:

- one screen rather than a data portal;
- five immediately understandable indicators rather than hundreds or thousands;
- map + globe context instead of table-first exploration;
- country search and tap-to-profile;
- reporting year and stale-data warning;
- works offline after installation;
- no account required for the core experience.

The intended v1 user is a student, teacher, news reader, traveler, presenter, or generally curious person asking a quick question such as: **“How does this country compare with the rest of the world?”**

For historical series, deep indicator research, downloadable datasets, or policy-grade analysis, use the underlying primary data systems instead.

See `docs/PRODUCT_VALUE_AUDIT.md` for the audited product rationale, competitive gap analysis, and v1.1 priorities.

## Repository authority

- Grok reference canonical: `refat247/world-metrics`
- Frozen Grok baseline: `archive/grok-canonical-v1.0`
- Baseline commit: `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`
- Canonical HTML Git blob: `79487b79286ce7c8dbae0685db33ddaefffdeaee`
- Active production canonical: this repository, `refat247/world-metrics-app`

`artifacts/original/world-metrics.html` is fetched only from that pinned commit during bootstrap and is accepted only if its Git blob SHA matches the expected canonical value.

## Audit

```bash
npm run audit
```

## Browser / PWA

```bash
python -m http.server 4173 --directory www
```

Open `http://localhost:4173`.

## Android

Android Build Gate v1 and Physical Device QA v2 have passed. The generated `android/` project and `package-lock.json` are version-controlled production source.

On Windows, after installing Node.js 22+ and Android Studio, double-click `SETUP_ANDROID_WINDOWS.bat`. It uses `npm ci`, synchronizes the canonical web assets into the committed Android project, and opens Android Studio. If `android/` is ever missing, the script can regenerate it as a recovery path.

The current Play release candidate is documented in `docs/RELEASE_AUDIT.md`; the next external gate is Google Play Internal Testing.

## iOS

Requires macOS + Xcode. Run `SETUP_IOS_MAC.command` when the iOS gate begins.

## Design rule

Do not merge Grok/App-Builder infrastructure into this repository merely because it exists upstream. Product features belong here; the Grok repository remains the preserved comparison/reference lineage.
