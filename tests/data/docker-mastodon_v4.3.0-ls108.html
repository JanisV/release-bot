————————

*LinuxServer Changes:*

Rebase to Alpine 3\.20, enable [Active Record Encryption](https://github.com/mastodon/mastodon/pull/29831/files)\. Existing users should update their nginx confs to avoid http2 deprecation warnings\.

*mastodon Changes:*

✏ __*Upgrade overview*__

This release contains upgrade notes that deviate from the norm:

‼️ Requires new encryption secrets environment variables
⚠️ The minimal supported version for PostgreSQL has been bumped to 12
⚠️ The minimal supported version for Ruby has been bumped to 3\.1
⚠️ The minimal supported version for Node\.js has been bumped to 18
⚠️ Requires rebuilding Elasticsearch accounts index
⚠️ We switched from yarn 1 to yarn 4, and recommend using corepack
⚠️ The Docker image has been split in two separate images
⚠️ Rolling updates from versions earlier than Mastodon 4\.2 are not supported
⚠️ StatsD integration has been removed, replaced by OpenTelemetry integration
⚠️ ImageMagick is being deprecated and may be removed in a future version
ℹ️ Requires streaming API restart
ℹ️ Requires database migrations
ℹ️ The logging format of the streaming server has changed

For more information, scroll down to the upgrade instructions section\.

✏ __*Changelog*__

The following changelog entries focus on changes visible to users, administrators, client developers or federated software developers, but there has also been a lot of code modernization, refactoring, and tooling work, in particular by @mjankowski\.

📚 *Security*

⦁ *Add confirmation interstitial instead of silently redirecting logged\-out visitors to remote resources* \(\#27792, \#28902, and \#30651 by @ClearlyClaire and @Gargron\)
This fixes a longstanding open redirect in Mastodon, at the cost of added friction when local links to remote resources are shared\.
⦁ Fix ReDoS vulnerability on some Ruby versions \([GHSA\-jpxp\-r43f\-rhvx](https://github.com/mastodon/mastodon/security/advisories/GHSA-jpxp-r43f-rhvx)\)
⦁ Change `form-action` Content\-Security\-Policy directive to be more restrictive \(\#26897 and \#32241 by @ClearlyClaire\)
⦁ Update dependencies
📚 *Added*

⦁ *Add server\-side notification grouping* \(\#29889, \#30576, \#30685, \#30688, \#30707, \#30776, \#30779, \#30781, \#30440, \#31062, \#31098, \#31076, \#31111, \#31123, \#31223, \#31214, \#31224, \#31299, \#31325, \#31347, \#31304, \#31326, \#31384, \#31403, \#31433, \#31509, \#31486, \#31513, \#31592, \#31594, \#31638, \#31746, \#31652, \#31709, \#31725, \#31745, \#31613, \#31657, \#31840, \#31610, \#31929, \#32089, \#32085, \#32243, \#32179 and \#32254 by @ClearlyClaire, @Gargron, @mgmn, and @renchap\)
Group notifications of the same type for the same target, so that your notifications no longer get cluttered by boost and favorite notifications as soon as a couple of your posts get traction\.
This is done server\-side so that clients can efficiently get relevant groups without having to go through numerous pages of individual notifications\.
As part of this, the visual design of the entire notifications feature has been revamped\.
This feature is intended to eventually replace the existing notifications column, but for this first beta, users will have to enable it in the “Experimental features” section of the notifications column settings\.
The API is not final yet, but it consists of:
  ⦁ a new `group_key` attribute to `Notification` entities
  ⦁ `GET /api/v2/notifications`: https://docs\.joinmastodon\.org/methods/grouped\_notifications/\#get\-grouped
  ⦁ `GET /api/v2/notifications/:group_key`: https://docs\.joinmastodon\.org/methods/grouped\_notifications/\#get\-notification\-group
  ⦁ `GET /api/v2/notifications/:group_key/accounts`: https://docs\.joinmastodon\.org/methods/grouped\_notifications/\#get\-group\-accounts
  ⦁ `POST /api/v2/notifications/:group_key/dimsiss`: https://docs\.joinmastodon\.org/meth
\-\=SKIPPED\=\-
