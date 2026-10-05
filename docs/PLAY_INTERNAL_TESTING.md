# Google Play Internal Testing — World Metrics v1.0.3

## Release candidate

Use only the final upload-key-signed bundle:

- Application ID: `app.worldmetrics.mobile`
- Version name: `1.0.3`
- Version code: `4`
- File: `world-metrics-v1.0.3-signed.aab`
- SHA-256: `161650b129340d43c064d738a083c5df10bd7a618e3815e2aa5cfb736b890c0b`

Do not upload the debug APK or the earlier unsigned/intermediate bundles to the Play release track.

## 1. Create/open the app in Play Console

Open Google Play Console and create or select **World Metrics**. Ensure the package/application ID is `app.worldmetrics.mobile`.

For a new app, Google Play uses Play App Signing. Keep the developer **upload key** private; it is used only to authenticate future bundle uploads.

## 2. Open Internal testing

In Play Console go to:

**Test and release → Testing → Internal testing**

Create or manage the internal-test track, then choose **Create new release**.

Google Play currently supports up to 100 internal testers per app and recommends internal testing as the first QA distribution track.

## 3. Upload the bundle

Upload:

`world-metrics-v1.0.3-signed.aab`

Confirm Play recognizes:

- package: `app.worldmetrics.mobile`
- version code: `4`
- version name: `1.0.3`
- target SDK: `36`

If Play reports a signing-certificate mismatch, stop rather than generating another key. Compare the upload certificate fingerprints with the release audit and recover the canonical upload keystore.

## 4. Release metadata

Suggested release name:

`1.0.3-internal-1`

Suggested release notes:

> Initial internal test of World Metrics: offline country metrics, Flat/Globe map modes, country search, portrait/landscape support, optimized touch gestures, and Android Back handling.

## 5. Add testers

Create/select an email list under Internal testing and add the Google accounts that will install the test. Start with the developer's own Play-enabled Google account, then add additional trusted testers as needed.

Save the tester list and copy the tester opt-in/share link provided by Play Console.

## 6. Review and roll out

Review Play Console warnings and errors. Resolve blocking errors before continuing.

Then choose the action to roll out/start the release to **Internal testing**. Do not promote directly to Production in this gate.

## 7. Play-delivered smoke test

Install World Metrics from the internal-test Play Store link rather than sideloading an APK.

Verify at minimum:

1. app installs and launches;
2. branded launcher icon and splash screen appear correctly;
3. all five metrics remain visible in portrait;
4. Flat and Globe modes render;
5. country search/select works;
6. pinch/zoom/drag remains responsive;
7. Portrait ↔ Landscape control works both ways;
8. Back closes country details before root exit;
9. root double-Back exit works;
10. cold launch works with network disabled.

If all ten pass, record **Play Internal Testing smoke test = PASS** before moving to broader testing or production.

## Security / signing rule

Never commit or upload any of the following to this public repository:

- upload keystore (`.jks` / `.keystore`);
- keystore password;
- key password;
- private signing-key material.

Back up the canonical upload keystore and its credentials in at least two secure locations. Losing the upload key is recoverable through Play's upload-key reset process, but preserving the canonical key avoids unnecessary release disruption.

## Official references

- Internal testing: https://support.google.com/googleplay/android-developer/answer/9845334
- Prepare/roll out releases: https://support.google.com/googleplay/android-developer/answer/9859348
- Play App Signing: https://support.google.com/googleplay/android-developer/answer/9842756
- Target API requirements: https://support.google.com/googleplay/android-developer/answer/11926878
