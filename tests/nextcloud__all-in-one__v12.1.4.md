Nextcloud 32.0.2 is included

<!-- Release notes generated using configuration in .github/release.yml at main -->

## What's Changed
### Potentially breaking with v12
- The docker API version that is used by the mastercontainer was upgraded to v1.44 to fix an incompatibility with docker v29. Make sure that your underlying docker installation supports this api version by upgrading the docker installation. If you are not able to upgrade your docker installation, you can adjust the internally used docker api version by so: https://github.com/nextcloud/all-in-one?tab=readme-ov-file#how-to-adjust-the-internally-used-docker-api-version
- The included Nextcloud archive was upgraded from v31 to v32
- The libreoffice binary which was included in the Nextcloud container by default is now removed to reduce the image size by half. You can still add it by so: https://github.com/nextcloud/all-in-one?tab=readme-ov-file#how-to-add-os-packages-permanently-to-the-nextcloud-container
- The caddy community container was upgraded to v3. There is one breaking change if you are using that: 
    - The Talk port that was usually exposed on port 3478 is now set to port 443 udp and tcp and reachable via `your-nc-domain.com`. For the changes to become activated, you need to go to `https://your-nc-domain.com/settings/admin/talk` and delete all turn and stun servers. Then restart the containers and the new config should become active.

### 🏕 New features and other improvements
* collabora: adjust some additional things by @szaimen in https://github.com/nextcloud/all-in-one/pull/7178
* re-enable whiteboard by default by @szaimen in https://github.com/nextcloud/all-in-one/pull/7180
### 🐞 Fixed bugs
* fix whiteboard recording chrome #3 by @hweihwang in https://github.com/nextcloud/all-in-one/pull/7128
* Revert "build(deps): bump collabora/code from 25.04.7.1.1 to 25.04.7.2.1 in /Containers/collabora" by @szaimen in https://github.com/nextcloud/all-in-one/pull/7175
### 👒 Updated dependencies
* build(deps): bump peter-evans/create-pull-request from 7.0.8 to 7.0.9 in /.github/workflows by @dependabot[bot] in https://github.com/nextcloud/all-in-one/pull/7176
* build(deps): bump actions/checkout from 5.0.1 to 6.0.0 in /.github/workflows by @dependabot[bot] in https://github.com/nextcloud/all-in-one/pull/7177


**Full Changelog**: https://github.com/nextcloud/all-in-one/compare/v12.1.3...v12.1.4