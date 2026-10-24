# Profile: app-store

**Dated:** 2026-10-22, from Apple's App Review Guidelines
(https://developer.apple.com/app-store/review/guidelines/) and App Store Connect rules as known then. **Apple
changes these**, so each audit checks the live page and reports the differences as checklist drift (the skill's
step 3). Section numbers below are Apple's as of this date; trust the live page where they differ.

**Picked when:** the project builds an Apple-platform app headed for the App Store or TestFlight (an `.xcodeproj`
or `Package.swift` with an app target, an `Info.plist`, StoreKit code, App Store copy in the repository).

The auditor is two strangers at once: **the person who downloads the app**, and **Apple's reviewer**. The core
checks in `repo.md` apply to the app and its store page: "fresh install" means a clean build on a clean
simulator reaching the app's first useful screen.

## Completeness (2.1)

1. **No placeholder content** anywhere a user or reviewer can reach: icons, art, text, sample data, "TODO",
   "Lorem ipsum", debug or developer toggles left visible.
2. **No crashes or dead ends** on a first run through every tab and the main flows, on the oldest OS version the
   app supports and on the newest.
3. **A reviewer can reach everything.** If any part needs an account or a purchase, the review notes say how
   (a demo account, or that the paid part can be tested in the sandbox).

## Store page and metadata (2.3)

4. **Screenshots show the real app**, as it is in this build, at the sizes App Store Connect asks for.
5. **Name, subtitle, description and keywords are accurate**: no feature the build lacks, no other company's
   trademark used to attract searches, no prices in the text.
6. **Age rating** answers match what the app contains.
7. **Support URL** works and leads to a way to reach the developer; a **marketing URL** works if one is given.

## Payments (3.1)

8. **Digital unlocks use in-app purchase** (StoreKit) by default (3.1.1). An outside purchase link is allowed only
   where Apple's guidelines allow it for that storefront (3.1.1(a)): on the United States storefront with no
   entitlement needed; in the other storefronts Apple names, only with a StoreKit External Purchase Link
   Entitlement (or, for music streaming, the Music Streaming Services Entitlement) and only to a destination Apple
   permits. In every other storefront, nothing in the app or its
   store text may point to another way to pay. Check which storefronts the app is offered in: a link that is fine
   in one is a finding in another. A few kinds of app have their own exceptions (3.1.3, such as "reader" apps);
   read the live page.
9. **Restore Purchases** exists and works for non-consumable unlocks.
10. **The paid tier is described honestly** before purchase: what it unlocks and the price as StoreKit shows it.

## Privacy (5.1)

11. **A privacy policy** is linked in App Store Connect and reachable inside the app, and it says plainly what is
    collected (or that nothing is).
12. **The privacy "nutrition label"** in App Store Connect matches what the app and every SDK in it actually do.
13. **A privacy manifest** (`PrivacyInfo.xcprivacy`) is in the app, declares a reason for every required-reason API
    the app uses, and each third-party SDK that needs its own manifest has one.
14. **Permission prompts** (camera, photos, location…) appear only when needed, with purpose strings that say why.
15. **Account deletion** inside the app, if the app lets people make an account.

## Rights and legal (5.2, 5.3)

16. **Trademarks and names**: other companies' product names, logos and console or device images are used only as
    plain references, never as the app's own branding, and nothing suggests an endorsement that does not exist.
17. **Data and content the app ships** (databases, images, guides) is the developer's own or used with permission,
    and its sources are credited where their terms ask.
18. **Disclaimers** the app relies on (technical, legal, safety) are where a user sees them before acting on the
    advice.

## Build and submission

19. **Built with the Xcode and SDK version Apple currently requires** for new submissions (check the live page).
20. **App icon** at every required size, with no transparency; a launch screen that is not blank.
21. **Export compliance**: the encryption question is answered (`ITSAppUsesNonExemptEncryption` in `Info.plist`
    saves asking on every upload).
22. **EU distribution**: the trader status declaration is made if the app is offered in the European Union.
23. **Sign in with Apple** offered alongside any third-party or social login (4.8).

## End user, beyond Apple

24. **The first five minutes**: what a new user sees first, whether it is clear what to do, and whether the app
    works offline if it says it does.
25. **Accessibility**: Dynamic Type, VoiceOver labels on the main controls, contrast in light and dark mode. Not a
    review rule, but the end user's.
