**CI Report:**

N/A

**LinuxServer Changes:**

**Full Changelog**: https://github.com/linuxserver/docker-mastodon/compare/v4.5.2-ls170...v4.5.2-ls171

**Remote Changes:**

<h1><picture>
  <source media="(prefers-color-scheme: dark)" srcset="./lib/assets/wordmark.dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="./lib/assets/wordmark.light.png?raw=true">
  <img alt="Mastodon" src="./lib/assets/wordmark.light.png?raw=true" height="34">
</picture></h1>

## Upgrade overview

This release contains upgrade notes that deviate from the norm:

ℹ️ Requires assets recompilation

For more information, view the complete release notes and scroll down to the upgrade instructions section.

## Changelog

### Changed

- Change private quote education modal to not show up on self-quotes (#36926 by @ClearlyClaire)

### Fixed

- Fix missing fallback link in CW-only quote posts (#36963 by @ClearlyClaire)
- Fix statuses without text being hidden while loading (#36962 by @ClearlyClaire)
- Fix `g` + `h` keyboard shortcut not working when a post is focused (#36935 by @diondiondion)
- Fix quoting overwriting current content warning (#36934 by @ClearlyClaire)
- Fix scroll-to-status in threaded view being unreliable (#36927 by @ClearlyClaire)
- Fix path resolution for emoji worker (#36897 by @ChaosExAnima)
- Fix `tootctl upgrade storage-schema` failing with `ArgumentError` (#36914 by @shugo)
- Fix cross-origin handling of CSS modules (#36890 by @ClearlyClaire)
- Fix error with remote tags including percent signs (#36886 and #36925 by @ChaosExAnima and @ClearlyClaire)
- Fix bogus quote approval policy not always being replaced correctly (#36885 by @ClearlyClaire)
- Fix hashtag completion not being inserted correctly (#36884 by @ClearlyClaire)
- Fix Cmd/Ctrl + Enter in the composer triggering confirmation dialog action (#36870 by @diondiondion)

## Upgrade notes

To get the code for v4.5.2, use `git fetch && git checkout v4.5.2`.

> [!NOTE]
> As always, make sure you have backups of the database before performing any upgrades. If you are using docker-compose, this is how a backup command might look: `docker exec mastodon_db_1 pg_dump -Fc -U postgres postgres > name_of_the_backup.dump`

### Dependencies

External dependencies have not changed since v4.5.0.

- Ruby: 3.2 or newer
- PostgreSQL: 14 or newer
- Elasticsearch (recommended, for full-text search): 7.x (OpenSearch should also work)
- LibreTranslate (optional, for translations): 1.3.3 or newer
- Redis: 7.0 or newer
- Node: 20.19 or newer
- libvips (optional, instead of ImageMagick): 8.13 or newer
- ImageMagick (optional if using libvips): 6.9.7-7 or newer

### Update steps

The following instructions are for updating from 4.5.1.

If you are upgrading directly from an earlier release, please carefully read the upgrade notes for the skipped releases as well, as they often require extra steps such as database migrations. In particular, it is very important to read the [4.5.0 release notes](https://github.com/mastodon/mastodon/releases/tag/v4.5.0).

### Non-Docker

> [!TIP]
> The `charlock_holmes` gem may fail to build on some systems with recent versions of gcc.
If you run into this issue, try `BUNDLE_BUILD__CHARLOCK_HOLMES="--with-cxxflags=-std=c++17" bundle install`.

1. Install dependencies with `bundle install` and `yarn install --immutable`
2. Precompile the assets: `RAILS_ENV=production bundle exec rails assets:precompile`
3. Restart all Mastodon processes.

### When using Docker

1. Restart all Mastodon processes.