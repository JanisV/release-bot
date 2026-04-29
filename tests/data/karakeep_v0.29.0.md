————————

📌 __*0\.29\.0*__

Welcome to the 0\.29\.0 release of Karakeep\! This release ships some of our most awaited features\. Collaborative lists, automated bookmark backups, search auto complete, highlighs are getting notes and search, and the mobile app is getting some more love\. As usual thanks to @aa\-ko, @fivestones, and everyone who shipped code, triaged bugs, or shared feedback for this release\.

>If you enjoy using Karakeep, consider supporting the project [here ☕️](https://buymeacoffee.com/mbassem) or via GitHub [here](https://github.com/sponsors/MohamedBassem)\.

[🖼️https://cdn\.buymeacoffee\.com/buttons/v2/default\-yellow\.png](https://www.buymeacoffee.com/mbassem)

And in case you missed it, we now have a ☁️ managed offering ☁️ for those who don't want to self\-host\. ~We're still in private beta \(you can signup for access [here](https://tally.so/r/wo8zzx)\) and gradually letting more and more users in\.~ We're in public beta now and you can signup [here](https://cloud.karakeep.app) 🎉\.

📌 __*New Features 🚀*__

⦁ Collaborative lists are here\! \(\#2146, \#2152\)
  ⦁ You can now invite collaborators to your lists and manage their access levels between viewers and editors\.
  ⦁ This was the most requested feature on the roadmap, and it's now here\!
⦁ Automated bookmark backups you can schedule once and forget \(\#2182\)
  ⦁ Currently it only captures non\-asset bookmarks, but I'm planning to include lists, tags, and other metadata in the future\.
⦁ Search gets autocomplete so you can find the right filters and terms faster \(\#2178\)
⦁ Highlights overhaul: notes \+ search bar on web, plus a dedicated highlights page on mobile \(\#2154, \#2155, \#2156, \#2157\)
⦁ Mobile catches up with smart list creation and an all\-tags screen \(\#2153, \#2163\)
⦁ Crawler domain rate limiting to avoid getting throttled by external sites \(\#2115\)
  ⦁ Configure it with `CRAWLER_DOMAIN_RATE_LIMIT_WINDOW_MS` and `CRAWLER_DOMAIN_RATE_LIMIT_MAX_REQUESTS`\.
⦁ Import from MyMind \(\#2138\)
📌 __*UX Improvements ✨*__

⦁ Sidebar typography and colors should feel nicer \(specially in dark mode\)\.
⦁ Page titles are now correctly displayed in the browser tabs\.
⦁ We have a friendlier 404 page for bookmarks/lists that don't exist\.
⦁ You can now see stats about the source of your bookmarks in the usage stats page \(extension, web app, mobile app, etc\)\.
📌 __*Fixes 🔧*__

⦁ Prompts lazily load `js-tiktoken` which should cut between 70\-150MB of karakeep's memory usage \(\#2176\)
⦁ The edit dialog wasn't correctly showing the extracted text from assets, this is now fixed \(\#2181\)\.
⦁ IP validation allowlisting now allows bypassing all domains by setting `CRAWLER_ALLOWED_INTERNAL_HOSTNAMES` to `.`\.
⦁ Fix a worker crash when hitting invalid URLs with proxy enabled\.
📌 __*For Developers 🛠️*__
⦁ GET `/api/version` endpoint for getting server version \(\#2167\)
⦁ More visibility: HTTP status Prometheus counters, failed\_permanent worker metric, and system metrics on web/worker containers \(\#2117, \#2107\)
⦁ Documentation updates for `LOG_LEVEL` and Raycast links \(\#2166, \#1923\) by @aa\-ko and @fivestones
📌 __*Screenshots 📸*__

✏ __*Collaborative Lists*__

🖼️https://github\.com/user\-attachments/assets/f19f9951\-c460\-413c\-9757\-6014a7ec4f7e

✏ __*Automated Backups*__

🖼️https://github\.com/user\-attachments/assets/65dc7e0e\-3ab3\-4243\-b451\-5ef3a3e7130b

✏ __*Search Autocomplete*__

🖼️https://github\.com/user\-attachments/assets/ed2f7a61\-835f\-4ee6\-8940\-657110932526

📌 __*Upgrading 📦*__

To upgrade:
⦁ If you're using `KARAKEEP_VERSION=release`, run `docker compose pull && docker compose up -d`\.
⦁ If you're pinning it to a specific version, bump the version and then run `docker compose pull && docker compose up -d`\.
📌 __*All Commits*__

⦁ i18n: fix en\_US translation \- @MohamedBassem in f01d96fd
⦁ i18n: Sync weblate translations \- @Hosted Weblate in e1ad2cfd
⦁ feat: autocomplete search terms \(\#2178\) \- @MohamedBa
\-\=SKIPPED\=\-
