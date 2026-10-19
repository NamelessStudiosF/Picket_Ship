# Picket Ship: Android and iOS project

The game lives in `www/index.html` (one file, no internet needed). [Capacitor](https://capacitorjs.com) wraps it into real Android and iOS apps that you can install on phones and submit to Google Play and the App Store.

```
www/index.html            the game (phone-ready, offline)
assets/                   app icon and splash artwork (regenerate with scripts/make_icons.py)
capacitor.config.json     app name and ID
.github/workflows/        cloud build that produces an Android APK
PRIVACY.md                privacy policy template (stores require a public URL for one)
```

## 0. Decide these first

1. **App ID.** Open `capacitor.config.json` and change `com.example.picketship` to something unique that you own, in reverse-domain style, for example `com.yourname.picketship`. Both stores lock this in after your first upload, so choose it now.
2. **Developer accounts.** Google Play Console is a one-time fee (about 25 USD). Apple Developer Program is about 99 USD per year. Check both sites for current prices.
3. **A Mac for iOS.** Apple only lets you build and sign iOS apps with Xcode on macOS. If you do not own a Mac, see "No Mac" below.

## 1. Play it on your Android phone today (no Android Studio)

1. Create a free GitHub account and a new repository, then upload this whole folder to it.
2. Open the repository's **Actions** tab, pick **Android debug APK**, and press **Run workflow**. It takes a few minutes.
3. Open the finished run and download the `picket-ship-debug-apk` file. Unzip it, send `app-debug.apk` to your phone, and open it. Android will ask you to allow installs from that source.

A debug APK is for your own testing. The Play Store needs the signed bundle from section 3.

## 2. Build locally (Android Studio and/or Xcode)

Requirements: Node.js 20 or newer. Android Studio for Android. A Mac with Xcode for iOS.

```bash
npm install
npm run assets          # makes every icon and splash size from assets/
npx cap add android     # creates the android/ folder
npx cap add ios         # creates the ios/ folder (on a Mac)
npm run android         # syncs the game and opens Android Studio
npm run ios             # syncs the game and opens Xcode
```

Commit the `android/` and `ios/` folders to git after adding them. After any change to `www/index.html`, run `npx cap sync` before building again.

Run it on a phone:

- **Android:** turn on Developer options and USB debugging on the phone, connect it, and press Run in Android Studio.
- **iPhone:** connect it, pick it as the target in Xcode, choose your Apple ID under Signing & Capabilities, and press Run. With a free Apple ID the app expires after 7 days. A paid account removes that limit and enables TestFlight.

## 3. Publish on Google Play

1. In Android Studio: **Build > Generate Signed App Bundle / APK > Android App Bundle**. Create a new keystore when asked. **Back up the keystore file and its passwords somewhere safe.** If you lose it you cannot update the app.
2. Set the version in `android/app/build.gradle` (`versionCode` goes up by 1 with every upload, `versionName` is what players see).
3. In Play Console create the app, then complete: store listing, content rating questionnaire, target audience, **Data safety** form (the game collects no data), and the privacy policy URL.
4. Upload the `.aab` file to a release. Google currently asks new personal accounts to run a closed test with a minimum number of testers for a couple of weeks before production access, so check the console for what applies to you.
5. Required store graphics: a 512x512 icon (use `assets/icon-only.png` resized), a 1024x500 feature graphic, and at least two phone screenshots. Take screenshots from the running game.

Google raises the minimum target Android version each year. If Play Console rejects the upload for that reason, update Capacitor (`npm install @capacitor/core@latest @capacitor/android@latest @capacitor/ios@latest @capacitor/cli@latest`) and rebuild.

## 4. Publish on the App Store

1. In Xcode, open `ios/App/App.xcworkspace`. Under **Signing & Capabilities** choose your team and make sure the Bundle Identifier matches your app ID.
2. Set the version and build number on the **General** tab. The build number must go up with every upload.
3. Choose **Any iOS Device** as the target, then **Product > Archive > Distribute App > App Store Connect**.
4. In App Store Connect create the app record and fill in: description, keywords, age rating, privacy policy URL, App Privacy answers (data not collected), and screenshots at the sizes it requests.
5. Add the uploaded build to a TestFlight group to try it on your own iPhone first, then submit for review.

Apple reviews every app. A plain web page in a wrapper can be rejected, but a real game with its own gameplay, like this one, normally passes. The review notes box is a good place to say it is a self-contained game.

### No Mac?

Cloud build services such as Codemagic, or a macOS runner on GitHub Actions, can build and upload an iOS app without you owning a Mac. You still need the paid Apple Developer account, and you have to set up signing in their dashboard. Their documentation walks through it for Capacitor projects.

## 5. Changing the game

Everything is in `www/index.html`. The values near the top of the script control difficulty: `HIT` (how close a threat gets before it hits), `BEAM_HALF` (width of the radar beam), `UNLOCK` (missiles returned before submarines appear), plus speeds and hold times in `spawn()`.

## Known limits

- Sound is synthesised in the game (no audio files). On iPhone it should play with the silent switch on, but this depends on the iOS version, so test it on a real device. The speaker button in the corner, or the M key, mutes it.
- It uses each phone's built-in condensed and monospace fonts, so the title looks slightly different on Android and iPhone.
- The best score is stored on the device only.
- The app pauses when it goes to the background and asks you to tap Resume.
