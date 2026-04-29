**LinuxServer Changes:**

Rebase to Alpine 3.20, enable [Active Record Encryption](https://github.com/mastodon/mastodon/pull/29831/files). Existing users should update their nginx confs to avoid http2 deprecation warnings.

**mastodon Changes:**

<h1><picture>
  <source media="(prefers-color-scheme: dark)" srcset="./lib/assets/wordmark.dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="./lib/assets/wordmark.light.png?raw=true">
  <img alt="Mastodon" src="./lib/assets/wordmark.light.png?raw=true" height="34">
</picture></h1>

## Upgrade overview

This release contains upgrade notes that deviate from the norm:

‼️ Requires new encryption secrets environment variables\
:warning: The minimal supported version for PostgreSQL has been bumped to 12\
:warning: The minimal supported version for Ruby has been bumped to 3.1\
:warning: The minimal supported version for Node.js has been bumped to 18\
:warning: Requires rebuilding Elasticsearch accounts index\
:warning: We switched from yarn 1 to yarn 4, and recommend using corepack\
:warning: The Docker image has been split in two separate images\
:warning: Rolling updates from versions earlier than Mastodon 4.2 are not supported\
:warning: StatsD integration has been removed, replaced by OpenTelemetry integration\
:warning: ImageMagick is being deprecated and may be removed in a future version\
ℹ️ Requires streaming API restart\
ℹ️ Requires database migrations\
ℹ️ The logging format of the streaming server has changed

For more information, scroll down to the upgrade instructions section.

## Changelog

The following changelog entries focus on changes visible to users, administrators, client developers or federated software developers, but there has also been a lot of code modernization, refactoring, and tooling work, in particular by @mjankowski.

### Security

- **Add confirmation interstitial instead of silently redirecting logged-out visitors to remote resources** (#27792, #28902, and #30651 by @ClearlyClaire and @Gargron)\
  This fixes a longstanding open redirect in Mastodon, at the cost of added friction when local links to remote resources are shared.
- Fix ReDoS vulnerability on some Ruby versions ([GHSA-jpxp-r43f-rhvx](https://github.com/mastodon/mastodon/security/advisories/GHSA-jpxp-r43f-rhvx))
- Change `form-action` Content-Security-Policy directive to be more restrictive (#26897 and #32241 by @ClearlyClaire)
- Update dependencies

### Added

- **Add server-side notification grouping** (#29889, #30576, #30685, #30688, #30707, #30776, #30779, #30781, #30440, #31062, #31098, #31076, #31111, #31123, #31223, #31214, #31224, #31299, #31325, #31347, #31304, #31326, #31384, #31403, #31433, #31509, #31486, #31513, #31592, #31594, #31638, #31746, #31652, #31709, #31725, #31745, #31613, #31657, #31840, #31610, #31929, #32089, #32085, #32243, #32179 and #32254 by @ClearlyClaire, @Gargron, @mgmn, and @renchap)\
  Group notifications of the same type for the same target, so that your notifications no longer get cluttered by boost and favorite notifications as soon as a couple of your posts get traction.\
  This is done server-side so that clients can efficiently get relevant groups without having to go through numerous pages of individual notifications.\
  As part of this, the visual design of the entire notifications feature has been revamped.\
  This feature is intended to eventually replace the existing notifications column, but for this first beta, users will have to enable it in the “Experimental features” section of the notifications column settings.\
  The API is not final yet, but it consists of:
  - a new `group_key` attribute to `Notification` entities
  - `GET /api/v2/notifications`: https://docs.joinmastodon.org/methods/grouped_notifications/#get-grouped
  - `GET /api/v2/notifications/:group_key`: https://docs.joinmastodon.org/methods/grouped_notifications/#get-notification-group
  - `GET /api/v2/notifications/:group_key/accounts`: https://docs.joinmastodon.org/methods/grouped_notifications/#get-group-accounts
  - `POST /api/v2/notifications/:group_key/dimsiss`: https://docs.joinmastodon.org/methods/grouped_notifications/#dismiss-group
  - `GET /api/v2/notifications/:unread_count`: https://docs.joinmastodon.org/methods/grouped_notifications/#unread-group-count
- **Add notification policies, filtered notifications and notification requests** (#29366, #29529, #29433, #29565, #29567, #29572, #29575, #29588, #29646, #29652, #29658, #29666, #29693, #29699, #29737, #29706, #29570, #29752, #29810, #29826, #30114, #30251, #30559, #29868, #31008, #31011, #30996, #31149, #31220, #31222, #31225, #31242, #31262, #31250, #31273, #31310, #31316, #31322, #31329, #31324, #31331, #31343, #31342, #31309, #31358, #31378, #31406, #31256, #31456, #31419, #31457, #31508, #31540, #31541, #31723, #32062 and #32281 by @ClearlyClaire, @Gargron, @TheEssem, @mgmn, @oneiros, and @renchap)\
  The old “Block notifications from non-followers”, “Block notifications from people you don't follow” and “Block direct messages from people you don't follow” notification settings have been replaced by a new set of settings found directly in the notification column.\
  You can now separately filter or drop notifications from people you don't follow, people who don't follow you, accounts created within the past 30 days, as well as unsolicited private mentions, and accounts limited by the moderation.\
  Instead of being outright dropped, notifications that you chose to filter are put in a separate “Filtered notifications” box that you can review separately without it clogging your main notifications.\
  This adds the following REST API endpoints:

  - `GET /api/v2/notifications/policy`: https://docs.joinmastodon.org/methods/notifications/#get-policy
  - `PATCH /api/v2/notifications/policy`: https://docs.joinmastodon.org/methods/notifications/#update-the-filtering-policy-for-notifications
  - `GET /api/v1/notifications/requests`: https://docs.joinmastodon.org/methods/notifications/#get-requests
  - `GET /api/v1/notifications/requests/:id`: https://docs.joinmastodon.org/methods/notifications/#get-one-request
  - `POST /api/v1/notifications/requests/:id/accept`: https://docs.joinmastodon.org/methods/notifications/#accept-request
  - `POST /api/v1/notifications/requests/:id/dismiss`: https://docs.joinmastodon.org/methods/notifications/#dismiss-request
  - `POST /api/v1/notifications/requests/accept`: https://docs.joinmastodon.org/methods/notifications/#accept-multiple-requests
  - `POST /api/v1/notifications/requests/dismiss`: https://docs.joinmastodon.org/methods/notifications/#dismiss-multiple-requests
  - `GET /api/v1/notifications/requests/merged`: https://docs.joinmastodon.org/methods/notifications/#requests-merged

  In addition, accepting one or more notification requests generates a new streaming event:

  - `notifications_merged`: an event of this type indicates accepted notification requests have finished merging, and the notifications list should be refreshed

- **Add notifications of severed relationships** (#27511, #29665, #29668, #29670, #29700, #29714, #29712, and #29731 by @ClearlyClaire and @Gargron)\
  Notify local users when they lose relationships as a result of a local moderator blocking a remote account or server, allowing the affected user to retrieve the list of broken relationships.\
  Note that this does not notify remote users.\
  This adds the `severed_relationships` notification type to the REST API and streaming, with a new [`relationship_severance_event` attribute](https://docs.joinmastodon.org/entities/Notification/#relationship_severance_event).
- **Add hover cards in web UI** (#30754, #30864, #30850, #30879, #30928, #30949, #30948, #30931, and #31300 by @ClearlyClaire, @Gargron, and @renchap)\
  Hovering over an avatar or username will now display a hover card with the first two lines of the user's description and their first two profile fields.\
  This can be disabled in the “Animations and accessibility” section of the preferences.
- **Add "system" theme setting (light/dark theme depending on user system preference)** (#29748, #29553, #29795, #29918, #30839, and #30861 by @nshki, @ErikUden, @mjankowski, @renchap, and @vmstan)\
  Add a “system” theme that automatically switch between default dark and light themes depending on the user's system preferences.\
  Also changes the default server theme to this new “system” theme so that automatic theme selection happens even when logged out.
- **Add timeline of public posts about a trending link** (#30381 and #30840 by @Gargron)\
  You can now see public posts mentioning currently-trending articles from people who have opted into discovery features.\
  This adds a new REST API endpoint: https://docs.joinmastodon.org/methods/timelines/#link
- **Add author highlight for news articles whose authors are on the fediverse** (#30398, #30670, #30521, #30846, #31819, #31900 and #32188 by @Gargron, @mjankowski and @oneiros)\
  This adds a mechanism to [highlight the author of news articles](https://blog.joinmastodon.org/2024/07/highlighting-journalism-on-mastodon/) shared on Mastodon.\
  Articles hosted outside the fediverse can indicate a fediverse author with a meta tag:
  ```html
  <meta name="fediverse:creator" content="username@domain" />
  ```
  On the API side, this is represented by a new `authors` attribute to the `PreviewCard` entity: https://docs.joinmastodon.org/entities/PreviewCard/#authors\
  Users can allow arbitrary domains to use `fediverse:creator` to credit them by visiting `/settings/verification`.\
  This is federated as a new `attributionDomains` property in the `http://joinmastodon.org/ns` namespace, containing an array of domain names: https://docs.joinmastodon.org/spec/activitypub/#properties-used-1
- **Add in-app notifications for moderation actions and warnings** (#30065, #30082, and #30081 by @ClearlyClaire)\
  In addition to email notifications, also notify users of moderation actions or warnings against them directly within the app, so they are less likely to miss important communication from their moderators.\
  This adds the `moderation_warning` notification type to the REST API and streaming, with a new [`moderation_warning` attribute](https://docs.joinmastodon.org/entities/Notification/#moderation_warning).
- **Add domain information to profiles in web UI** (#29602 by @Gargron)\
  Clicking the domain of a user in their profile will now open a tooltip with a short explanation about servers and federation.
- **Add support for Redis sentinel** (#31694, #31623, #31744, #31767, and #31768 by @ThisIsMissEm and @oneiros)\
  See https://docs.joinmastodon.org/admin/scaling/#redis-sentinel
- **Add ability to reorder uploaded media before posting in web UI** (#28456 and #32093 by @Gargron)
- Add “A Mastodon update is available.” message on admin dashboard for non-bugfix updates (#32106 by @ClearlyClaire)
- Add ability to view alt text by clicking the ALT badge in web UI (#32058 by @Gargron)
- Add preview of followers removed in domain block modal in web UI (#32032 and #32105 by @ClearlyClaire and @Gargron)
- Add reblogs and favourites counts to statuses in ActivityPub (#32007 by @Gargron)
- Add moderation interface for searching hashtags (#30880 by @ThisIsMissEm)
- Add ability for admins to configure instance favicon and logo (#30040, #30208, #30259, #30375, #30734, #31016, and #30205 by @ClearlyClaire, @FawazFarid, @JasonPunyon, @mgmn, and @renchap)\
  This is also exposed through the REST API: https://docs.joinmastodon.org/entities/Instance/#icon
- Add `api_versions` to `/api/v2/instance` (#31354 by @ClearlyClaire)\
  Add API version number to make it easier for clients to detect compatible features going forward.\
  See API documentation at https://docs.joinmastodon.org/entities/Instance/#api-versions
- Add quick links to Administration and Moderation Reports from Web UI (#24838 by @ThisIsMissEm)
- Add link to `/admin/roles` in moderation interface when changing someone's role (#31791 by @ClearlyClaire)
- Add recent audit log entries in federation moderation interface (#27386 by @ThisIsMissEm)
- Add profile setup to onboarding in web UI (#27829, #27876, and #28453 by @Gargron)
- Add prominent share/copy button on profiles in web UI (#27865 and #27889 by @ClearlyClaire and @Gargron)
- Add optional hints for server rules (#29539 and #29758 by @ClearlyClaire and @Gargron)\
  Server rules can now be broken into a short rule name and a longer explanation of the rule.\
  This adds a new [`hint` attribute](https://docs.joinmastodon.org/entities/Rule/#hint) to `Rule` entities in the REST API.
- Add support for PKCE in OAuth flow (#31129 by @ThisIsMissEm)
- Add CDN cache busting on media deletion (#31353 and #31414 by @ClearlyClaire and @tribela)
- Add the OAuth application used in local reports (#30539 by @ThisIsMissEm)
- Add hint to user that other remote statuses may be missing (#26910, #31387, and #31516 by @Gargron, @audiodude, and @renchap)
- Add lang attribute on preview card title (#31303 by @c960657)
- Add check for `Content-Length` in `ResponseWithLimitAdapter` (#31285 by @c960657)
- Add `Accept-Language` header to fetch preview cards in the server's default language (#31232 by @c960657)
- Add support for PKCE Extension in OmniAuth OIDC through the `OIDC_USE_PKCE` environment variable (#31131 by @ThisIsMissEm)
- Add API endpoints for unread notifications count (#31191 by @ClearlyClaire)\
  This adds the following REST API endpoints:
  - `GET /api/v1/notifications/unread_count`: https://docs.joinmastodon.org/methods/notifications/#unread-count
- Add `/` keyboard shortcut to focus the search field (#29921 by @ClearlyClaire)
- Add button to view the Hashtag on the instance from Hashtags in Moderation UI (#31533 by @ThisIsMissEm)
- Add list of pending releases directly in mail notifications for version updates (#29436 and #30035 by @ClearlyClaire)
- Add “Appeals” link under “Moderation” navigation category in moderation interface (#31071 by @ThisIsMissEm)
- Add badge on account card in report moderation interface when account is already suspended (#29592 by @ClearlyClaire)
- Add admin comments directly to the `admin/instances` page (#29240 by @tribela)
- Add ability to require approval when users sign up using specific email domains (#28468, #28732, #28607, and #28608 by @ClearlyClaire)
- Add banner for forwarded reports made by remote users about remote content (#27549 by @ClearlyClaire)
- Add support HTML ruby tags in remote posts for east-asian languages (#30897 by @ThisIsMissEm)
- Add link to manage warning presets in admin navigation (#26199 by @vmstan)
- Add volume saving/reuse to video player (#27488 by @thehydrogen)
- Add Elasticsearch index size, ffmpeg and ImageMagick versions to the admin dashboard (#27301, #30710, #31130, and #30845 by @vmstan)
- Add `MASTODON_SIDEKIQ_READY_FILENAME` environment variable to use a file for Sidekiq to signal it is ready to process jobs (#30971 and #30988 by @renchap)\
  In the official Docker image, this is set to `sidekiq_process_has_started_and_will_begin_processing_jobs` so that Sidekiq will touch `tmp/sidekiq_process_has_started_and_will_begin_processing_jobs` to signal readiness.
- Add `S3_RETRY_LIMIT` environment variable to make S3 retries configurable (#23215 by @smiba)
- Add `S3_KEY_PREFIX` environment variable (#30181 by @S0yKaf)
- Add support for multiple `redirect_uris` when creating OAuth 2.0 Applications (#29192 by @ThisIsMissEm)
- Add Interlingue and Interlingua to interface languages (#28630 and #30828 by @Dhghomon and @renchap)
- Add Kashubian, Pennsylvania Dutch, Vai, Jawi Malay, Mohawk and Low German to posting languages (#26024, #26634, #27136, #29098, #27115, and #27434 by @EngineerDali, @HelgeKrueger, and @gunchleoc)
- Add option to use native Ruby driver for Redis through `REDIS_DRIVER=ruby` (#30717 by @vmstan)
- Add support for libvips in addition to ImageMagick (#30090, #30590, #30597, #30632, #30857, #30869, #30858 and #32104 by @ClearlyClaire, @Gargron, and @mjankowski)\
  Server admins can now use libvips as a faster and lighter alternative to ImageMagick for processing user-uploaded images.\
  This requires libvips 8.13 or newer, and needs to be enabled with `MASTODON_USE_LIBVIPS=true`.\
  This is enabled by default in the official Docker images, and is intended to completely replace ImageMagick in the future.
- Add validations to `Web::PushSubscription` (#30540 and #30542 by @ThisIsMissEm)
- Add anchors to each authorized application in `/oauth/authorized_applications` (#31677 by @fowl2)
- Add active animation to header settings button (#30221, #30307, and #30388 by @daudix)
- Add OpenTelemetry instrumentation (#30130, #30322, #30353, #30350 and #31998 by @julianocosta89, @renchap, @robbkidd and @timetinytim)\
  See https://docs.joinmastodon.org/admin/config/#otel for documentation
- Add API to get multiple accounts and statuses (#27871 and #30465 by @ClearlyClaire)\
  This adds `GET /api/v1/accounts` and `GET /api/v1/statuses` to the REST API, see https://docs.joinmastodon.org/methods/accounts/#index and https://docs.joinmastodon.org/methods/statuses/#index
- Add support for CORS to `POST /oauth/revoke` (#31743 by @ClearlyClaire)
- Add redirection back to previous page after site upload deletion (#30141 by @FawazFarid)
- Add RFC8414 OAuth 2.0 server metadata (#29191 by @ThisIsMissEm)
- Add loading indicator and empty result message to advanced interface search (#30085 by @ClearlyClaire)
- Add `profile` OAuth 2.0 scope, allowing more limited access to user data (#29087 and #30357 by @ThisIsMissEm)
- Add the role ID to the badge component (#29707 by @renchap)
- Add diagnostic message for failure during CLI search deploy (#29462 by @mjankowski)
- Add pagination `Link` headers on API accounts/statuses when pinned true (#29442 by @mjankowski)
- Add support for specifying custom CA cert for Elasticsearch through `ES_CA_FILE` (#29122 and #29147 by @ClearlyClaire)
- Add groundwork for annual reports for accounts (#28693 by @Gargron)\
  This lays the groundwork for a “year-in-review”/“wrapped” style report for local users, but is currently not in use.
- Add notification email on invalid second authenticator (#28822 by @ClearlyClaire)
- Add date of account deletion in list of accounts in the admin interface (#25640 by @tribela)
- Add new emojis from `jdecked/twemoji` 15.0 (#28404 by @TheEssem)
- Add configurable error handling in attachment batch deletion (#28184 by @vmstan)\
  This makes the S3 batch size configurable through the `S3_BATCH_DELETE_LIMIT` environment variable (defaults to 1000), and adds some retry logic, configurable through the `S3_BATCH_DELETE_RETRY` environment variable (defaults to 3).
- Add VAPID public key to instance serializer (#28006 by @ThisIsMissEm)
- Add support for serving JRD `/.well-known/host-meta.json` in addition to XRD host-meta (#32206 by @c960657)
- Add `nodeName` and `nodeDescription` to nodeinfo `metadata` (#28079 by @6543)
- Add Thai diacritics and tone marks in `HASHTAG_INVALID_CHARS_RE` (#26576 by @ppnplus)
- Add variable delay before link verification of remote account links (#27774 by @ClearlyClaire)
- Add support for invite codes in the registration API (#27805 by @ClearlyClaire)
- Add HTML lang attribute to preview card descriptions (#27503 by @srapilly)
- Add display of relevant account warnings to report action logs (#27425 by @ClearlyClaire)
- Add validation of allowed schemes on preview card URLs (#27485 by @mjankowski)
- Add token introspection without read scope to `/api/v1/apps/verify_credentials` (#27142 by @ThisIsMissEm)
- Add support for cross-origin request to `/nodeinfo/2.0` (#27413 by @palant)
- Add variable delay before link verification of remote account links (#27351 by @ClearlyClaire)
- Add PWA shortcut to `/explore` page (#27235 by @jake-anto)

### Changed

- **Change icons throughout the web interface** (#27385, #27539, #27555, #27579, #27700, #27817, #28519, #28709, #28064, #28775, #28780, #27924, #29294, #29395, #29537, #29569, #29610, #29612, #29649, #29844, #27780, #30974, #30963, #30962, #30961, #31362, #31363, #31359, #31371, #31360, #31512, #31511, #31525, #32153, and #32201 by @ClearlyClaire, @Gargron, @arbolitoloco1, @mjankowski, @nclm, @renchap, @ronilaukkarinen, and @zunda)\
  This changes all the interface icons from FontAwesome to Material Symbols for a more modern look, consistent with the official Mastodon Android app.\
  In addition, better care is given to pixel alignment, and icon variants are used to better highlight active/inactive state.
- **Change design of compose form in web UI** (#28119, #29059, #29248, #29372, #29384, #29417, #29456, #29406, #29651, #29659, #31889 and #32033 by @ClearlyClaire, @Gargron, @eai04191, @hinaloe, and @ronilaukkarinen)\
  The compose form has been completely redesigned for a more modern and consistent look, as well as spelling out the chosen privacy setting and language name at all times.\
  As part of this, the “Unlisted” privacy setting has been renamed to “Quiet public”.
- **Change design of modals in the web UI** (#29576, #29614, #29640, #29644, #30131, #30884, #31399, #31555, #31752, #31801, #31883, #31844, #31864, and #31943 by @ClearlyClaire, @Gargron, @tribela and @vmstan)\
  The mute, block, and domain block confirmation modals have been completely redesigned to be clearer and include more detailed information on the action to be performed.\
  They also have a more modern and consistent design, along with other confirmation modals in the application.
- **Change colors throughout the web UI** (#29522, #29584, #29653, #29779, #29803, #29809, #29808, #29828, #31034, #31168, #31266, #31348, #31349, #31361, #31510 and #32128 by @ClearlyClaire, @Gargron, @mjankowski, @renchap, and @vmstan)
- **Change onboarding prompt to follow suggestions carousel in web UI** (#28878, #29272, and #31912 by @Gargron)
- **Change email templates** (#28416, #28755, #28814, #29064, #28883, #29470, #29607, #29761, #29760, #29879, #32073 and #32132 by @c960657, @ClearlyClaire, @Gargron, @hteumeuleu, and @mjankowski)\
  All emails to end-users have been completely redesigned with a fresh new look, providing more information while making them easier to read and keeping maximum compatibility across mail clients.
- **Change follow recommendations algorithm** (#28314, #28433, #29017, #29108, #29306, #29550, #29619, and #31474 by @ClearlyClaire, @Gargron, @kernal053, @mjankowski, and @wheatear-dev)\
  This replaces the “past interactions” recommendation algorithm with a “friends of friends” algorithm that suggests accounts followed by people you follow, and a “similar profiles” algorithm that suggests accounts with a profile similar to your most recent follows.\
  In addition, the implementation has been significantly reworked, and all follow recommendations are now dismissable.\
  This change deprecates the `source` attribute in `Suggestion` entities in the REST API, and replaces it with the new [`sources` attribute](https://docs.joinmastodon.org/entities/Suggestion/#sources).
- Change account search algorithm (#30803 by @Gargron)
- **Change streaming server to use its own dependencies and its own docker image** (#24702, #27967, #26850, #28112, #28115, #28137, #28138, #28497, #28548, #30795, #31612, and #31615 by @TheEssem, @ThisIsMissEm, @jippi, @renchap, @timetinytim, and @vmstan)\
  In order to reduce the amount of runtime dependencies, the streaming server has been moved into a separate package and Docker image.\
  The `mastodon` image does not contain the streaming server anymore, as it has been moved to its own `mastodon-streaming` image.\
  Administrators may need to update their setup accordingly.
- Change how content warnings and filters are displayed in web UI (#31365, and #31761 by @Gargron)
- Change preview card processing to ignore `undefined` as canonical url (#31882 by @oneiros)
- Change embedded posts to use web UI (#31766, #32135 and #32271 by @Gargron)
- Change inner borders in media galleries in web UI (#31852 by @Gargron)
- Change design of media attachments and profile media tab in web UI (#31807, #32048, #31967, #32217, #32224 and #32257 by @ClearlyClaire and @Gargron)
- Change labels on thread indicators in web UI (#31806 by @Gargron)
- Change label of "Data export" menu item in settings interface (#32099 by @c960657)
- Change responsive break points on navigation panel in web UI (#32034 by @Gargron)
- Change cursor to `not-allowed` on disabled buttons (#32076 by @mjankowski)
- Change OAuth authorization prompt to not refer to apps as “third-party” (#32005 by @Gargron)
- Change Mastodon to issue correct HTTP signatures by default (#31994 by @ClearlyClaire)
- Change zoom icon in web UI (#29683 by @Gargron)
- Change directory page to use URL query strings for options (#31980, #31977 and #31984 by @ClearlyClaire and @renchap)
- Change report action buttons to be disabled when action has already been taken (#31773, #31822, and #31899 by @ClearlyClaire and @ThisIsMissEm)
- Change width of columns in advanced web UI (#31762 by @Gargron)
- Change design of unread conversations in web UI (#31763 by @Gargron)
- Change Web UI to allow viewing and severing relationships with suspended accounts (#27667 by @ClearlyClaire)\
  This also adds a `with_suspended` parameter to `GET /api/v1/accounts/relationships` in the REST API.
- Change preview card image size limit from 2MB to 8MB when using libvips (#31904 by @ClearlyClaire)
- Change avatars border radius (#31390 by @renchap)
- Change counters to be displayed on profile timelines in web UI (#30525 by @Gargron)
- Change disabled buttons color in light mode to make the difference more visible (#30998 by @renchap)
- Change design of people tab on explore in web UI (#30059 by @Gargron)
- Change sidebar text in web UI (#30696 by @Gargron)
- Change "Follow" to "Follow back" and "Mutual" when appropriate in web UI (#28452, #28465, and #31934 by @ClearlyClaire, @Gargron and @renchap)
- Change media to be hidden/blurred by default in report modal (#28522 by @ClearlyClaire)
- Change order of the "muting" and "blocking" list options in “Data Exports” (#26088 by @fixermark)
- Change admin and moderation notes character limit from 500 to 2000 characters (#30288 by @ThisIsMissEm)
- Change mute options to be in dropdown on muted users list in web UI (#30049 and #31315 by @ClearlyClaire and @Gargron)
- Change out-of-band hashtags design in web UI (#29732 by @Gargron)
- Change design of metadata underneath detailed posts in web UI (#29585, #29605, and #29648 by @ClearlyClaire and @Gargron)
- Change action button to be last on profiles in web UI (#29533 and #29923 by @ClearlyClaire and @Gargron)
- Change confirmation prompts in trending moderation interface to be more specific (#19626 by @tribela)
- Change “Trends” moderation menu to “Recommendations & Trends” and move follow recommendations there (#31292 by @ThisIsMissEm)
- Change irrelevant fields in account cleanup settings to be disabled unless automatic cleanup is enabled (#26562 by @c960657)
- Change dropdown menu icon to not be replaced by close icon when open in web UI (#29532 by @Gargron)
- Change back button to always appear in advanced web UI (#29551 and #29669 by @Gargron)
- Change border of active compose field search inputs (#29832 and #29839 by @vmstan)
- Change instances of Nokogiri HTML4 parsing to HTML5 (#31812, #31815, #31813, and #31814 by @flavorjones)
- Change link detection to allow `@` at the end of an URL (#31124 by @adamniedzielski)
- Change User-Agent to use Mastodon as the product, and http.rb as platform details (#31192 by @ClearlyClaire)
- Change layout and wording of the Content Retention server settings page (#27733 by @vmstan)
- Change unconfirmed users to be kept for one week instead of two days (#30285 by @renchap)
- Change maximum page size for Admin Domain Management APIs from 200 to 500 (#31253 by @ThisIsMissEm)
- Change database pool size to default to Sidekiq concurrency settings in Sidekiq processes (#26488 by @sinoru)
- Change alt text to empty string for avatars (#21875 by @jasminjohal)
- Change Docker images to use custom-built libvips and ffmpeg (#30571, #30569, and #31498 by @vmstan)
- Change external links in the admin audit log to plain text or local administration pages (#27139 and #27150 by @ClearlyClaire and @ThisIsMissEm)
- Change YJIT to be enabled when available (#30310 and #27283 by @ClearlyClaire and @mjankowski)\
  Enable Ruby's built-in just-in-time compiler. This improves performances substantially, at the cost of a slightly increased memory usage.
- Change `.env` file loading from deprecated `dotenv-rails` gem to `dotenv` gem (#29173 and #30121 by @mjankowski)\
  This should have no effect except in the unlikely case an environment variable included a newline.
- Change “Panjabi” language name to the more common spelling “Punjabi” (#27117 by @gunchleoc)
- Change encryption of OTP secrets to use ActiveRecord Encryption (#29831, #28325, #30151, #30202, #30340, and #30344 by @ClearlyClaire and @mjankowski)\
  This requires a manual step from administrators of existing servers. Indeed, they need to generate new secrets, which can be done using `bundle exec rails db:encryption:init`.\
  Furthermore, there is a risk that the introduced migration fails if the server was misconfigured in the past. If that happens, the migration error will include the relevant information.
- Change `/api/v1/announcements` to return regular `Status` entities (#26736 by @ClearlyClaire)
- Change imports to convert case-insensitive fields to lowercase (#29739 and #29740 by @ThisIsMissEm)
- Change stats in the admin interface to be inclusive of the full selected range, from beginning of day to end of day (#29416 and #29841 by @mjankowski)
- Change materialized views to be refreshed concurrently to avoid locks (#29015 by @Gargron)
- Change compose form to use server-provided post character and poll options limits (#28928 and #29490 by @ClearlyClaire and @renchap)
- Change streaming server logging from `npmlog` to `pino` and `pino-http` (#27828 by @ThisIsMissEm)\
  This changes the Mastodon streaming server log format, so this might be considered a breaking change if you were parsing the logs.
- Change media “ALT” label to use a specific CSS class (#28777 by @ClearlyClaire)
- Change streaming API host to not be overridden to localhost in development mode (#28557 by @ClearlyClaire)
- Change cookie rotator to use SHA1 digest for new cookies (#27392 by @ClearlyClaire)\
  Note that this requires that no pre-4.2.0 Mastodon web server is running when this code is deployed, as those would not understand the new cookies.\
  Therefore, zero-downtime updates are only supported if you're coming from 4.2.0 or newer. If you want to skip Mastodon 4.2, you will need to completely stop Mastodon services before updating.
- Change preview card deletes to be done using batch method (#28183 by @vmstan)
- Change `img-src` and `media-src` CSP directives to not include `https:` (#28025 and #28561 by @ClearlyClaire)
- Change self-destruct procedure (#26439, #29049, and #29420 by @ClearlyClaire and @zunda)\
  Instead of enqueuing deletion jobs immediately, `tootctl self-destruct` now outputs a value for the `SELF_DESTRUCT` environment variable, which puts a server in self-destruct mode, processing deletions in the background, while giving users access to their export archives.

### Removed

- Remove unused E2EE messaging code and related `crypto` OAuth scope (#31193, #31945, #31963, and #31964 by @ClearlyClaire and @mjankowski)
- Remove StatsD integration (replaced by OpenTelemetry) (#30240 by @mjankowski)
- Remove `CacheBuster` default options (#30718 by @mjankowski)
- Remove home marker updates from the Web UI (#22721 by @davbeck)\
  The web interface was unconditionally updating the home marker to the most recent received post, discarding any value set by other clients, thus making the feature unreliable.
- Remove support for Ruby 3.0 (reaching EOL) (#29702 by @mjankowski)
- Remove setting for unfollow confirmation modal (#29373 by @ClearlyClaire)\
  Instead, the unfollow confirmation modal will always be displayed.
- Remove support for Capistrano (#27295 and #30009 by @mjankowski and @renchap)

### Fixed

- **Fix link preview cards not always preserving the original URL from the status** (#27312 by @Gargron)
- Fix log out from user menu not working on Safari (#31402 by @renchap)
- Fix various issues when in link preview card generation (#28748, #30017, #30362, #30173, #30853, #30929, #30933, #30957, #30987, and #31144 by @adamniedzielski, @oneiros, @phocks, @timothyjrogers, and @tribela)
- Fix handling of missing links in Webfinger responses (#31030 by @adamniedzielski)
- Fix error when accepting an appeal for sensitive posts deleted in the meantime (#32037 by @ClearlyClaire)
- Fix error when encountering reblog of deleted post in feed rebuild (#32001 by @ClearlyClaire)
- Fix Safari browser glitch related to horizontal scrolling (#31960 by @Gargron)
- Fix unresolvable mentions sometimes preventing processing incoming posts (#29215 by @tribela and @ClearlyClaire)
- Fix too many requests caused by relationship look-ups in web UI (#32042 by @Gargron)
- Fix links for reblogs in moderation interface (#31979 by @ClearlyClaire)
- Fix the appearance of avatars when they do not load (#31966 and #32270 by @Gargron and @renchap)
- Fix spurious error notifications for aborted requests in web UI (#31952 by @c960657)
- Fix HTTP 500 error in `/api/v1/polls/:id/votes` when required `choices` parameter is missing (#25598 by @danielmbrasil)
- Fix security context sometimes not being added in LD-Signed activities (#31871 by @ClearlyClaire)
- Fix cross-origin loading of `inert.css` polyfill (#30687 by @louis77)
- Fix wrapping in dashboard quick access buttons (#32043 by @renchap)
- Fix recently used tags hint being displayed in profile edition page when there is none (#32120 by @mjankowski)
- Fix checkbox lists on narrow screens in the settings interface (#32112 by @mjankowski)
- Fix the position of status action buttons being affected by interaction counters (#32084 by @renchap)
- Fix the summary of converted ActivityPub object types to be treated as HTML (#28629 by @Menrath)
- Fix cutoff of instance name in sign-up form (#30598 by @oneiros)
- Fix invalid date searches returning 503 errors (#31526 by @notchairmk)
- Fix invalid `visibility` values in `POST /api/v1/statuses` returning 500 errors (#31571 by @c960657)
- Fix some components re-rendering spuriously in web UI (#31879 and #31881 by @ClearlyClaire and @Gargron)
- Fix sort order of moderation notes on Reports and Accounts (#31528 by @ThisIsMissEm)
- Fix email language when recipient has no selected locale (#31747 by @ClearlyClaire)
- Fix frequently-used languages not correctly updating in the web UI (#31386 by @c960657)
- Fix `POST /api/v1/statuses` silently ignoring invalid `media_ids` parameter (#31681 by @c960657)
- Fix handling of the `BIND` environment variable in the streaming server (#31624 by @ThisIsMissEm)
- Fix empty `aria-hidden` attribute value in logo resources area (#30570 by @mjankowski)
- Fix “Redirect URI” field not being marked as required in “New application” form (#30311 by @ThisIsMissEm)
- Fix right-to-left text in preview cards (#30930 by @ClearlyClaire)
- Fix rack attack `match_type` value typo in logging config (#30514 by @mjankowski)
- Fix various cases of duplicate, missing, or inconsistent borders or scrollbar styles (#31068, #31286, #31268, #31275, #31284, #31305, #31346, #31372, #31373, #31389, #31432, #31391, #31445, #32091, #32147 and #32137 by @ClearlyClaire, @mjankowski, @valtlai and @vmstan)
- Fix editing description of media uploads with custom thumbnails (#32221 by @ClearlyClaire)
- Fix race condition in `POST /api/v1/push/subscription` (#30166 by @ClearlyClaire)
- Fix post deletion not being delayed when those are part of an account warning (#30163 by @ClearlyClaire)
- Fix rendering error on `/start` when not logged in (#30023 by @timothyjrogers)
- Fix unneeded requests to blocked domains when receiving relayed signed activities from them (#31161 by @ClearlyClaire)
- Fix logo pushing header buttons out of view on certain conditions in mobile layout (#29787 by @ClearlyClaire)
- Fix notification-related records not being reattributed when merging accounts (#29694 by @ClearlyClaire)
- Fix results/query in `api/v1/featured_tags/suggestions` (#29597 by @mjankowski)
- Fix distracting and confusing always-showing scrollbar track in boost confirmation modal (#31524 by @ClearlyClaire)
- Fix being able to upload more than 4 media attachments in some cases (#29183 by @mashirozx)
- Fix preview card player getting embedded when clicking on the external link button (#29457 by @ClearlyClaire)
- Fix full date display not respecting the locale 12/24h format (#29448 by @renchap)
- Fix filters title and keywords overflow (#29396 by @GeopJr)
- Fix incorrect date format in “Follows and followers” (#29390 by @JasonPunyon)
- Fix navigation item active highlight for some paths (#32159 by @mjankowski)
- Fix “Edit media” modal sizing and layout when space-constrained (#27095 by @ronilaukkarinen)
- Fix modal container bounds (#29185 by @nico3333fr)
- Fix inefficient HTTP signature parsing using regexps and `StringScanner` (#29133 by @ClearlyClaire)
- Fix moderation report updates through `PUT /api/v1/admin/reports/:id` not being logged in the audit log (#29044, #30342, and #31033 by @mjankowski, @tribela, and @vmstan)
- Fix moderation interface allowing to select rule violation when there are no server rules (#31458 by @ThisIsMissEm)
- Fix redirection from paths with url-encoded `@` to their decoded form (#31184 by @timothyjrogers)
- Fix Trending Tags pending review having an unstable sort order (#31473 by @ThisIsMissEm)
- Fix the emoji dropdown button always opening the dropdown instead of behaving like a toggle (#29012 by @jh97uk)
- Fix processing of incoming posts with bearcaps (#26527 by @kmycode)
- Fix support for IPv6 redis connections in streaming (#31229 by @ThisIsMissEm)
- Fix search form re-rendering spuriously in web UI (#28876 by @Gargron)
- Fix `RedownloadMediaWorker` not being called on transient S3 failure (#28714 by @ClearlyClaire)
- Fix ISO code for Canadian French from incorrect `fr-QC` to `fr-CA` (#26015 by @gunchleoc)
- Fix `.opus` file uploads being misidentified by Paperclip (#28580 by @vmstan)
- Fix loading local accounts with extraneous domain part in WebUI (#28559 by @ClearlyClaire)
- Fix destructive actions in dropdowns not using error color in light theme (#28484 by @logicalmoody)
- Fix call to inefficient `delete_matched` cache method in domain blocks (#28374 by @ClearlyClaire)
- Fix status edits not always being streamed to mentioned users (#28324 by @ClearlyClaire)
- Fix onboarding step descriptions being truncated on narrow screens (#28021 by @ClearlyClaire)
- Fix duplicate IDs in relationships and familiar_followers APIs (#27982 by @KevinBongart)
- Fix modal content not being selectable (#27813 by @pajowu)
- Fix Web UI not displaying appropriate explanation when a user hides their follows/followers (#27791 by @ClearlyClaire)
- Fix format-dependent redirects being cached regardless of requested format (#27632 by @ClearlyClaire)
- Fix confusing screen when visiting a confirmation link for an already-confirmed email (#27368 by @ClearlyClaire)
- Fix explore page reloading when you navigate back to it in web UI (#27489 by @Gargron)
- Fix missing redirection from `/home` to `/deck/home` in the advanced interface (#27378 by @Signez)
- Fix empty environment variables not using default nil value (#27400 by @renchap)
- Fix language sorting in settings (#27158 by @gunchleoc)

## Upgrade notes

To get the code for v4.3.0, use `git fetch && git checkout v4.3.0`.

> [!NOTE]
> As always, **make sure you have backups of the database before performing any upgrades**. If you are using docker-compose, this is how a backup command might look: `docker exec mastodon_db_1 pg_dump -Fc -U postgres postgres > name_of_the_backup.dump`

### Dependencies

External dependencies have changed since v4.2.12, with the Ruby, PostgreSQL and Node.js minimum version being higher. In addition, an optional dependency on `libvips` has been introduced to replace ImageMagick.

- Ruby: 3.1 or newer
- PostgreSQL: 12 or newer
- Elasticsearch (recommended, for full-text search): 7.x (OpenSearch should also work)
- LibreTranslate (optional, for translations): 1.3.3 or newer
- Redis: 4 or newer
- Node: 18 or newer
- ImageMagick (optional if using libvips): 6.9.7-7 or newer
- libvips (optional, instead of ImageMagick): 8.13 or newer

### Active Record encryption secrets configuration

Mastodon now requires new environment variables for secret keys to be set.
Generate new secrets and set `ACTIVE_RECORD_ENCRYPTION_DETERMINISTIC_KEY`, `ACTIVE_RECORD_ENCRYPTION_KEY_DERIVATION_SALT`, and `ACTIVE_RECORD_ENCRYPTION_PRIMARY_KEY` accordingly before restarting Mastodon.

All Mastodon processes need to have access to them, so if you use multiple `puma` (`mastodon-web`) and `sidekiq` (`mastodon-sidekiq`) nodes, make sure to copy the secrets to all of them.

Such secrets can be generated by running `bin/rails db:encryption:init`.

### Docker image split

The official Docker image has now been split in two smaller images:
- `ghcr.io/mastodon/mastodon`, which does not contain the streaming server anymore
- `ghcr.io/mastodon/mastodon-streaming`, which contains only the streaming server

The `docker-compose.yml` file shipped with Mastodon has been updated accordingly. If you use something else, you will need to update your configuration.

### Cookies and rolling updates

Cookies issued by Mastodon are now using SHA256 digests. To ensure you are not losing user sessions, do not perform a rolling update from versions of Mastodon earlier than v4.2.0.

That is, either completely stop Mastodon before updating it, or update to the latest v4.2 *then* update to v4.3.

### Yarn 4 and corepack

We have switched from Yarn 1 to the more modern and more efficient Yarn 4.

The recommended way is to use `corepack`, which is normally distributed with NodeJS. To do so, do `corepack enable`, then, in Mastodon's directory, once you have checked out v4.3.0, `corepack prepare`.

You can also install yarn 4 directly if you don't want to or can't use corepack.

### ImageMagick deprecation and libvips replacement

ImageMagick support in Mastodon is being deprecated in favor of libvips, a more efficient library to process image attachments.

To use libvips instead of ImageMagick, install libvips 8.13 or newer, and set the `MASTODON_USE_LIBVIPS` environment variable to `true`.

The official Mastodon docker images use libvips instead of ImageMagick, and we recommend you do the same, but ImageMagick is still supported in this version for older distributions that do not include a recent enough version of libvips.

### StatsD removal and OpenTelemetry integration

StatsD support has been removed, after being deprecated in 4.2.0.

If you want to have metrics for your Sidekiq queues (queue size, latency…), you can use https://github.com/Strech/sidekiq-prometheus-exporter

Mastodon now also supports exporting tracing data using OpenTelemetry. This can be used to get detailed performance data, as well as monitoring for backend errors. More informations on how to configure it in our docs (https://docs.joinmastodon.org/admin/config/#otel)

### Update steps

The following instructions are for updating from 4.2.12.

If you are upgrading directly from an earlier release, please carefully read the upgrade notes for the skipped releases as well, as they often require extra steps such as database migrations. If you are upgrading from a pre-4.2 version, please check the “Cookies and rolling updates” section above.

If you are updating from 4.3.0-beta.1, 4.3.0-beta.2 or 4.3.0-rc.1, only a few of these steps are relevant, see the next section.

### Non-docker

> [!TIP]
> The `charlock_holmes` gem may fail to build on some systems with recent versions of `gcc`.
> If you run into such an issue, try `BUNDLE_BUILD__CHARLOCK_HOLMES="--with-cxxflags=-std=c++17" bundle install`.

1. If you are using `rbenv`, [update the list of available versions](https://github.com/rbenv/ruby-build/wiki#updating-ruby-build) and install the proper Ruby version by doing `RUBY_CONFIGURE_OPTS=--with-jemalloc rbenv install` in the Mastodon install directory (e.g. `/home/mastodon/live`)
2. Install yarn 4 (if you use `corepack`, just do `corepack prepare`). See the “Yarn 4 and corepack” section for more information.
3. Install dependencies with `bundle install` and `yarn install --immutable`
4. Generate secrets by running `RAILS_ENV=production bin/rails db:encryption:init`, then copy them to your `.env.production` (copy it across all your nodes if you use multiple ones)
5. Precompile the assets: `RAILS_ENV=production bundle exec rails assets:precompile`
6. Run the *pre-deployment* database migrations by specifying the `SKIP_POST_DEPLOYMENT_MIGRATIONS=true` environment variable: `SKIP_POST_DEPLOYMENT_MIGRATIONS=true RAILS_ENV=production bundle exec rails db:migrate`
7. Restart all Mastodon processes. If you are updating directly from a Mastodon version earlier than 4.2.0, see the “Cookies and rolling updates” section.
8. Run the *post-deployment* database migrations: `RAILS_ENV=production bundle exec rails db:migrate`
9. If you use Elasticsearch or OpenSearch, rebuild the account search index with `RAILS_ENV=production bin/tootctl search deploy --only=accounts`

### When using docker

1. Generate secrets by running `docker-compose run --rm web bin/rails db:encryption:init`, then copy them to your `.env.production` (make sure to copy them across all your Mastodon nodes as they will all need access to these secrets)
2. Run the *pre-deployment* database migrations by specifying the `SKIP_POST_DEPLOYMENT_MIGRATIONS=true` environment variable: `docker-compose run --rm -e SKIP_POST_DEPLOYMENT_MIGRATIONS=true web bundle exec rails db:migrate`
3. Make sure your Docker configuration has been updated to take the Docker image split into account (See the “Docker image split” section above)
4. Restart all Mastodon processes. If you are updating directly from a Mastodon version earlier than 4.2.0, see the “Cookies and rolling updates” section.
5. Run the *post-deployment* database migrations: `docker-compose run --rm web bundle exec rails db:migrate`
6. If you use Elasticsearch or OpenSearch, rebuild the account search index with `docker-compose run --rm web bin/tootctl search deploy --only=accounts`

### Update steps from 4.3.0-beta.1, 4.3.0-beta.2 or 4.3.0-rc.1

The following instructions are for updating from 4.3.0-beta.1, 4.3.0-beta.2 or 4.3.0-rc.1, see the section above if you are updating from an older version.

### Non-docker

> [!TIP]
> The `charlock_holmes` gem may fail to build on some systems with recent versions of `gcc`.
> If you run into such an issue, try `BUNDLE_BUILD__CHARLOCK_HOLMES="--with-cxxflags=-std=c++17" bundle install`.

1. If you are using `rbenv`, [update the list of available versions](https://github.com/rbenv/ruby-build/wiki#updating-ruby-build) and install the proper Ruby version by doing `RUBY_CONFIGURE_OPTS=--with-jemalloc rbenv install` in the Mastodon install directory (e.g. `/home/mastodon/live`)
2. Install dependencies with `bundle install` and `yarn install --immutable`
3. Precompile the assets: `RAILS_ENV=production bundle exec rails assets:precompile`
4. Run the *pre-deployment* database migrations by specifying the `SKIP_POST_DEPLOYMENT_MIGRATIONS=true` environment variable: `SKIP_POST_DEPLOYMENT_MIGRATIONS=true RAILS_ENV=production bundle exec rails db:migrate`
5. Restart all Mastodon processes. If you are updating directly from a Mastodon version earlier than 4.2.0, see the “Cookies and rolling updates” section.
6. Run the *post-deployment* database migrations: `RAILS_ENV=production bundle exec rails db:migrate`

### When using docker

1. Run the *pre-deployment* database migrations by specifying the `SKIP_POST_DEPLOYMENT_MIGRATIONS=true` environment variable: `docker-compose run --rm -e SKIP_POST_DEPLOYMENT_MIGRATIONS=true web bundle exec rails db:migrate`
2. Restart all Mastodon processes. If you are updating directly from a Mastodon version earlier than 4.2.0, see the “Cookies and rolling updates” section.
3. Run the *post-deployment* database migrations: `docker-compose run --rm web bundle exec rails db:migrate`