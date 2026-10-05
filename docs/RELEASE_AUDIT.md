# Release Audit — World Metrics App v1.0.0

## Provenance

- Grok baseline commit: `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`
- Expected source HTML Git blob: `79487b79286ce7c8dbae0685db33ddaefffdeaee`
- Bootstrap refuses to continue if the downloaded pinned source does not match that blob.

## Product checks

`npm run audit` validates 12 static/PWA invariants plus the byte-level lineage invariant.

## Android Build Gate v1 — PASS

GitHub Actions run `37260108235` completed successfully on 2026-10-05.

Passed stages:

1. Node 22 setup.
2. Java 21 setup.
3. Capacitor dependency installation.
4. Static/PWA + Grok provenance audit.
5. Android native-project generation and Capacitor sync.
6. Gradle `assembleDebug` compilation.
7. APK existence/non-empty verification.
8. APK artifact upload.
9. Promotion of `android/` plus `package-lock.json` into the PRODUCT-CANONICAL repository.

Artifact:

- GitHub Actions artifact: `world-metrics-debug-apk`
- Artifact ID: `11323399726`
- APK SHA-256: `a01f84dbafb740b17a17fc02d8a94635e82a55ccb5d138f914f5f6835f44437a`

## Native-source policy after Build Gate v1

`android/` is now version-controlled production source. Generated build outputs, Gradle caches, keystores, and signing material remain excluded. The iOS project is still generated later on macOS/Xcode and remains outside the current Android-gate scope.

## Remaining validation boundary

A successful CI build proves source integrity and Android compilability; it does not substitute for physical-device QA. The next gate is installation and functional/offline testing on a real Android device.
