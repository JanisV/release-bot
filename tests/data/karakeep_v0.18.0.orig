Welcome to the `0.18.0` release of Hoarder! This release introduces customizable tagging rules (aka customizing the prompt), new UI look, selective full page archives, infinite scrolling, more bulk actions and more! As usual, we'd like to welcome our first time contributors @jarednipper, @Trugamr, @cedmax and @CrypticC3s4r! We also have @Lucius346346 working behind the scene on improving the UX of Hoarder with amazing designs! And finally, we have our usual contributors @kamtschatka and @mdsaban! Also thanks to @Papierkorb for the help in suggestions to improve the LLM prompt!

We also now have a public roadmap which you can check for the features that we're planning to deliver [here](https://github.com/orgs/hoarder-app/projects/1). Go upvote the features that you're waiting for!

> If you're enjoying Hoarder, you can consider supporting it [here ☕️](https://buymeacoffee.com/mbassem).

# New Feature

* Introducing customizable tagging rules: You can now customize the prompt that we use to generate the tags to your linkings and add custom rules for the LLM to adhere to!
  * You can use this to define your tagging rules in natural language and let the LLM take care of applying it.
* If you don't want to enable "Full page archives" by default, you can now selectively archive particular pages that you want to keep forever thanks to @kamtschatka!
* You can now export your bookmarks from Hoarder and re-import them back in another instance (note: currently images and pdfs are not exported).
* You can now customize the context length of the inference model using the `INFERENCE_CONTEXT_LENGTH` flag:
  * The bigger this value is, the more of your content the model will see and will be able to give you better tagging.
  * However, the bigger the context window, the more expensive the request is for OpenAI money-wise and for ollama resource-wise.
  * The current default is `2048` tokens (~2048 words).
* Better asset tracking and management:
  * We're now currently correctly accounting for all asset sizes in the database. You can view the usage of every user now in the admin panel.
  * Old assets are not automatically accounted for and you'll have to click the new `Compact Asset` button in the admin panel to backfill that data. This button also removes assets that are dangling (aka not linked to any bookmark).
  * This work is in preparation for supporting better privacy checks in the future when we implement public and collaborative lists.
* You can now attach custom image banners to your notes.
  * Those banners will appear at the top of your notes when you expand them as well as in the `List` layout.
  * We're still figuring out a good way to render them in the grid and masonry layouts.

# UX Improvements

* We have a refreshed UI looks thanks to amazing designs by @Lucius346346!
  * We now have a sticky navbar for better experience in bulk editing thanks to @mdsaban.
  * We also have a new profile options dropdown in the header where the user and admin settings buttons got moved to.
* We now have infinite scrolling for pagination so that you no longer need to click the `Show more` button.
* Bulk actions improvements:
  * There's now a `Select all` button to select all the currently visible bookmarks.
  * `Copy links` is also a thing to bulk copy the source links of a bunch of bookmarks thanks to @kamtschatka.
* You can now trigger AI tag regeneration for all bookmarks or the ones that that failed only in the admin panel.
* When you hoard text from other webpages by the extension (by highlighting text -> right click -> add to hoarder) the source link will now be preserved with the text.
* We have a new tabbed user settings page as it was getting quite long.
* Sidebar items were not clickable around the boarder which was annoying. @Trugamr fixed that!

# Fixes
* For those who want to go all-in on Oauth, you can now set `DISABLE_PASSWORD_AUTH=true` which will forbid any password-based authentication/signup. This is implemented by @kamtschatka.
* The All Tags page was taking too long to load when you have too many tags. @kamtschatka landed some improvements to the performance of this page.
* Editing lists from the sidebar was broken, now it's fixed.
* When you wipe your hoarder's database while still logged in the browser, users were getting some confusing behavior with confusing database errors. This is now fixed, and hoarder will automatically log you out if your account is no longer there.
* @Mxrk Added docker healthchecks to the dockerfile and also source label so that hoarder's updates can be correctly reflected in stuff like renovate.


# Screenshots

## The new UI Look

<img width="1209" alt="Screenshot 2024-10-13 at 3 16 59 PM" src="https://github.com/user-attachments/assets/0b13bf69-d0a1-4afc-90ca-826f898c3ae1">

## Profile Options

<img width="272" alt="Screenshot 2024-10-13 at 3 49 02 PM" src="https://github.com/user-attachments/assets/8e5e403c-a52c-4e39-a36a-eebcf96999b8">

## AI Settings and Tagging Rules

<img width="982" alt="Screenshot 2024-10-13 at 3 18 55 PM" src="https://github.com/user-attachments/assets/d67296d1-26c3-4c55-b346-b0e3d9568d16">

## New Import/Export Buttons

<img width="1345" alt="Screenshot 2024-10-13 at 3 19 46 PM" src="https://github.com/user-attachments/assets/729bd9c6-18df-4ca3-a70c-7d612b8d1f5a">

## Num Bookmarks & Asset Sizes in Admin Panel

<img width="1327" alt="Screenshot 2024-10-13 at 3 22 13 PM" src="https://github.com/user-attachments/assets/798fb564-5cb3-4ff8-9230-8262c4642e25">

## New Admin Actions

<img width="669" alt="Screenshot 2024-10-13 at 3 22 21 PM" src="https://github.com/user-attachments/assets/4e166fdd-f872-4961-beed-779bf2a029cc">


# Upgrading

To upgrade:
* If you're using HOARDER_VERSION=release, run `docker compose pull && docker compose up -d`.
* If you're pinning it to a specific version, upgrade the version and then run `docker compose pull && docker compose up -d`. 

# All Commits

* fix: Add support for importing notes from the hoarder export - @MohamedBassem in 43ed698
* fix(web): Fix settings tab overflow on mobile layouts - @MohamedBassem in cdd0088
* fix(web): Fix profile option icon in mobile layouts - @MohamedBassem in 8741ab0
* fix(web): Fix slowness in loading the all tags UI. Fixes  #382 (#390) - @kamtschatka in 4791a53
* feature: Allow importing hoarder's own bookmark file. Fixes #527 - @MohamedBassem in de9cf0a
* feature: Support regenerating AI tags only for failed bookmarks - @MohamedBassem in 2ccc15e
* build: Use node 22 for CI - @MohamedBassem in fb57f25
* deps: Upgrade nodejs to v22 - @MohamedBassem in 1390337
* deps: Upgrade metascraper for faster docker builds - @MohamedBassem in 31bcad8
* feature(web): Implement a new profile options drop menu and move user and admin settings there - @MohamedBassem in b36eea8
* docs: Add a section to installation docs about optional features - @MohamedBassem in 0d94506
* docs: Remove the warning about ollama being new - @MohamedBassem in 5e44cfb
* fix(web): Fix react error in search input - @MohamedBassem in 6035dff
* feature: Allow customizing the inference's context length - @MohamedBassem in 1b09682
* feature: Introduce a mechanism to cleanup dangling assets - @MohamedBassem in c16173e
* feature: Allow to disable default password login after SSO is configured. Fixes #406 (#502) - @kamtschatka in 9f87207
* fix(web): Reset search query and bulk edit when navigating away from the current page - @MohamedBassem in 02a5b35
* feature(web): Introduce a new sticky navbar. Fixes 520  (#515) - @mdsaban in 1f768be
* docker: Add HEALTHCHECK to Dockerfile (#508) - @Mxrk in e2644eb
* docker: add Source Label to Dockerfile (#509) - @Mxrk in 904eb5a
* fix(web): Fix sidebar list edit dialog not working. Fixes #447 - @MohamedBassem in 09e0659
* refactor: Start tracking bookmark assets in the assets table - @MohamedBassem in 1e5c575
* refactor: Include userId in the assets table - @MohamedBassem in db2d346
* readme: Add a security policy - @MohamedBassem in e6d4ff9
* feature: Allow disabling password signups (#413) - @kamtschatka in 4a3775a
* feature: Allow attaching custom banners to notes. Fixes: #106 - @MohamedBassem in 8a13095
* fix: Drop the usage of useCursorV2 from the server - @MohamedBassem in 99c6232
* fix(mobile): Drop the floating add button. Fixes #439 - @MohamedBassem in c017328
* feature: Persevere the source URL of clipped texts from the extension. Fixes #448 - @MohamedBassem in b147c8e
* feature(web): Async validate JWT account and sign out the user if they no longer exist - @MohamedBassem in f1c956a
* feature(web): Change the settings page to be tabbed - @MohamedBassem in 3a8d197
* fix(web): Simplify the language for inference settings - @MohamedBassem in 03e938a
* fix(web): Change export format to have content as a top level key - @MohamedBassem in 1f7da9a
* docker: Fix the docker-based development env (#456) - @CrypticC3s4r in 3f22801
* docs: Fix typo in installation docs (#465) - @jarednipper in f6192da
* feature(web): Allow users to export their links and notes - @MohamedBassem in c8a3c1e
* readme: Fix installation link in the readme (#482) - @disappointingsupernova in 463d041
* feature(cli): Add ability to get all bookmark IDs of a list. Fixes #442 (#446) - @kamtschatka in 4bda7a9
* deps: Upgrade openai package - @MohamedBassem in b56655c
* feature(web): Add ability to manually trigger full page archives. Fixes #398 (#418) - @kamtschatka in 8b69cdd
* feature(web): Add ability to rerun inference on all bookmarks. Fixes 443 - @MohamedBassem in 5281531
* fix(web): Improve SidebarItem tap target accessibility (#409) - @Trugamr in 8fe1927
* feature(web): Add the ability to customize the inference prompts. Fixes #170 - @MohamedBassem in 36fb5a4
* deps: Upgrade drizzle-kit - @MohamedBassem in 57f5faa
* fix(web): Fix another hydration error in copy to clipboard - @MohamedBassem in b32a832
* feature(web): Add infinite scrolling support - @MohamedBassem in ab1c837
* fix(web): Fix some hydration errors in bulk actions - @MohamedBassem in 41f4e6b
* feature(web): Add a select all button to bulk actions - @MohamedBassem in badf697
* feature(web): Add a bulk action to copy links into clipboard. Fixes #427 (#433) - @kamtschatka in ee0aad5
