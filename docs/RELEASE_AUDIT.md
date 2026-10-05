# Release Audit — World Metrics App v1.0.0

## Provenance

- Grok baseline commit: `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`
- Expected source HTML Git blob: `79487b79286ce7c8dbae0685db33ddaefffdeaee`
- Bootstrap refuses to continue if the downloaded pinned source does not match that blob.

## Product checks

`npm run audit` validates 12 static/PWA invariants plus the byte-level lineage invariant.

## Native build boundary

Capacitor source/configuration is canonical here. Android and iOS native projects are generated on development machines because Android SDK/Xcode toolchains are not committed in this v1.0.0 lineage.
