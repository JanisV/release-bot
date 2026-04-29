# v1.118.0

Welcome to release `v1.118.0` of Immich. This version comes with several breaking changes, and also improvements to the mobile app UI and UX, a new documentation home page, as well as bug fixes and enhancements across the app. We hope you enjoy this release!

> [!WARNING] 
> ## Breaking changes
> This release includes the following breaking changes:
> 1. Port alignment
> 2. Remove deprecated API endpoints
> 3. Remove deprecated `start.sh` arguments

### 1. Port alignment
We aligned the internal port of the `immich-server` to be similar to the binding port. Please make the following change to your `docker-compose.yml` file under the `immich-server` section. Reverse proxies using port 3001 also need to be updated to use port 2283.

```diff
services:
  immich-server:
    container_name: immich_server
    ...
    ports:
-    - 2283:3001
+    - 2283:2283
    ...
```

### 2. Remove deprecated API endpoints
The following endpoints were previously deprecated and have been removed, if you are a community project maintainer and using one of the endpoints below, please make sure to make changes to your project:
- `/api/server-info/*` has been removed. Use `/api/server/*` instead.
- `/api/people/:id/assets` has been removed. Use `/api/search/metadata` instead.

> [!NOTE] 
> This includes `/api/server-info/ping`, `/api/server-info/version`, `/api/server-features`, `/api/server-info/config`, `/api/server-info/statistics`, and others.

### 3. Remove deprecated `start.sh` arguments
The following docker commands have been removed:
- `start.sh immich`
- `start.sh microservices`


Follow the steps below to align `docker-compose.yml` with the default setup.

> [!NOTE] 
> These steps are only required if you still have the `immich-microservices` section in your `docker-compose.yml` or didn't follow the previous instructions to remove the command section. If you don't have the mentioned content below, you can ignore this


#### 1. Update `docker-compose.yml`


Remove the `command` line from `immich-server` and the entire `immich-microservices` service section as shown below.

```diff
services:
  immich-server:
    container_name: immich_server
    ...
    :
-   command: [ "start.sh", "immich" ]
    ...
    
-  immich-microservices:
-    container_name: immich_microservices
-    ...
-    :
-    command: [ "start.sh", "microservices" ]
-    ...
```

#### 2. Remove the running `immich-microservices` container
Run `docker compose down --remove-orphans` after updating `docker-compose.yml` to remove the old `immich-microservices` container.

## Highlights

Some of the highlights for this release include the following:

- Mobile UI/UX improvement
- Option to refresh face detection
- Color filters for editing photos
- Timezone improvements
- Deprecated release notes section
- Better JPEG compression
- Multi-GPU support for ML

### Mobile UI/UX improvement

Thank you all for the great feedback from the [dicussion](https://github.com/immich-app/immich/discussions/12597) we made a month ago about the proposed changes to the mobile app layout. We hope the following changes will provide more fluid experience when browing and managing your photos and videos.

#### Navigation bar

Photos and albums are the two most used pages. To make them more accessible, we replaced the `Sharing` page with a new `Albums` page where you can find all of the album related features and functions.

<img width="350" alt="image" src="https://github.com/user-attachments/assets/8020ae55-8e79-4cf0-ba2c-54ac56a9acb8">

#### Albums page

This new page allows users to quickly view, sort, search, filter, create, and manage albums. 

<img width="350" alt="image" src="https://github.com/user-attachments/assets/d5782994-f0f8-481f-b89e-c12b498b90b3">

#### Library page

The library page now includes quick access buttons to various views, including

- Favorites
- Archived
- Shared links
- Trash
- People
- Places
- Device albums
- Partner sharing

<p>
<img width="350" alt="image" src="https://github.com/user-attachments/assets/4d676568-593f-493f-b11c-6cc109b693ec">

<img width="350" alt="image" src="https://github.com/user-attachments/assets/4250a994-84a0-4195-b9f9-6c21b422124b">
</p>

#### Search page

Many of the items that were previously on this page have been moved to the `Library` page, mentioned above. As a result, the search page is less cluttered and includes quick access search chips and queries. Also, clicking on the search navbar item a second time will focus on the search bar and open the keyboard for easy access.

<img width="350" alt="image" src="https://github.com/user-attachments/assets/c02b7f79-1b0f-4d36-96f4-ba5b0e998cb4">

### Color filters for editing photos

This release introduces colors filter option in the edit menu on the mobile app. You can apply a set of presets colors to your photo. Thanks @Yuvi-raj-P for your contribution.


<img width="350" alt="filter-page" src="https://github.com/user-attachments/assets/3a34489a-f5cd-49a3-b960-459e97b563d0">


### Timezone improvements
Images without timezones could previously show up incorrectly in the timeline if the server had a timezone (`TZ=...`) set. This has been fixed and can be corrected by running metadata extraction on all assets.

### Deprecated release notes section
Future releases will now include a "Deprecated" section in the release notes, including details of API endpoints and other changes that will become breaking changes in a future release. Moving forward, we plan to use this section of the release notes as our primary communication method for these types of changes.

### Refresh face detection

Assets now have a `Refresh faces` option to update the set of detected faces based on the current face detection threshold. Likewise, there is a new `Refresh` button for Face Detection in the Jobs page that does the same for all assets.

Importantly, this does not clear all recognized people like the `All` button (renamed to `Reset`). If you find that a different detection threshold works better for your library and want to apply that new value to existing assets, `Refresh` will simply add or remove faces to apply this change.

It will only ever delete faces detected through machine learning, not EXIF. Speaking of EXIF-sourced faces, they can now be used to recognize detected faces as a result of this feature. This means the facial recognition process can share the same people listed in face metadata instead of duplicating them.

### Better JPEG compression

Immich now uses [Jpegli](https://opensource.googleblog.com/2024/04/introducing-jpegli-new-jpeg-coding-library.html), a new library leveraging the advancements of JPEG XL to shrink JPEG file size at the same (or higher) quality. This change narrows the gap between JPEG and WebP compression considerably, especially at high quality.

### Multi-GPU support for ML

It is now possible for a single instance of the machine learning service to use more than one GPU. Previously, this required several services and a load balancer in front. See the [documentation](https://main.preview.immich.app/docs/features/ml-hardware-acceleration#multi-gpu) for instructions.

<!-- Release notes generated using configuration in .github/release.yml at main -->

## Support Immich

<p align="center">
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjY2eWc5Y2F0ZW56MmR4aWE0dDhzZXlidXRmYWZyajl1bWZidXZpcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/87CKDqErVfMqY/giphy.gif" width="450" title="SUPPORT THE PROJECT!"> 
</p>


If you find the project helpful, you can support Immich by purchasing a product key at [https://buy.immich.app](https://buy.immich.app).

Cheers! 🍻

- - - -

<!-- Release notes generated using configuration in .github/release.yml at main -->

## What's Changed
### 🚨 Breaking Changes
* refactor(server): worker env by @jrasm91 in https://github.com/immich-app/immich/pull/13160
* chore: remove deprecated controller by @jrasm91 in https://github.com/immich-app/immich/pull/13189
* chore: remove deprecated endpoint by @jrasm91 in https://github.com/immich-app/immich/pull/13190
* feat: align compose ports by @jrasm91 in https://github.com/immich-app/immich/pull/13185
### 🚀 Features
* feat(server): refresh face detection by @mertalev in https://github.com/immich-app/immich/pull/12335
* feat(mobile): Adding filters feature to mobile image editor by @Yuvi-raj-P in https://github.com/immich-app/immich/pull/13174
* feat(ml): round-robin device assignment by @mertalev in https://github.com/immich-app/immich/pull/13237
* feat(mobile): new mobile UI by @alextran1502 in https://github.com/immich-app/immich/pull/12582
### 🌟 Enhancements
* feat(doc): new homepage design and font by @alextran1502 in https://github.com/immich-app/immich/pull/13084
* chore(mobile): search page minor enhancements by @alextran1502 in https://github.com/immich-app/immich/pull/13403
* fix(mobile): more efficient loading local image on ios by @alextran1502 in https://github.com/immich-app/immich/pull/13426
### 🐛 Bug fixes
* fix(mobile): respect orientation on displaying asset dimensions by @Yagnap in https://github.com/immich-app/immich/pull/13129
* fix(server): UTC+13 timezones treated as invalid during exif parsing  by @C-Otto in https://github.com/immich-app/immich/pull/13176
* fix(server): external libraries queueing two transcode jobs by @zackpollard in https://github.com/immich-app/immich/pull/13251
* fix(server): Allow commas and braces in import paths by @etnoy in https://github.com/immich-app/immich/pull/13259
* fix(server): searching with both `personIds` and `withPeople` by @mertalev in https://github.com/immich-app/immich/pull/13254
* fix(web): video player on Safari by @alextran1502 in https://github.com/immich-app/immich/pull/13242
* fix(server): timezones by @jrasm91 in https://github.com/immich-app/immich/pull/13262
* fix(ml): pin onnxruntime-openvino by @mertalev in https://github.com/immich-app/immich/pull/13290
* fix(cli): allow special characters in paths by @etnoy in https://github.com/immich-app/immich/pull/13282
* fix(mobile): trash sorting order by @yashrajjain726 in https://github.com/immich-app/immich/pull/13299
* fix(web): User removal from option menu on the top in shared album by @Pranav-8bit in https://github.com/immich-app/immich/pull/12959
* fix(web): rtl text on map is hidden by @zackpollard in https://github.com/immich-app/immich/pull/13342
* fix: library deletion by @danieldietzler in https://github.com/immich-app/immich/pull/13350
* fix(server): incorrect out_color_matrix value when generating thumbnails by @lyynd in https://github.com/immich-app/immich/pull/13409
* fix(web): change the code zh-Hans to zh-CN by @fa1seut0pia in https://github.com/immich-app/immich/pull/13414
### 📚 Documentation
* feat(docs): update roadmap by @aviv926 in https://github.com/immich-app/immich/pull/13212
* docs: fix confustion about libmali in hardware-transcoding.md  by @yoni13 in https://github.com/immich-app/immich/pull/13226
* docs: update version range for pgvecto.rs by @mertalev in https://github.com/immich-app/immich/pull/13231
* docs: Add DB name to backup-and-restore by @Mraedis in https://github.com/immich-app/immich/pull/13244
* docs: update authelia link by @martabal in https://github.com/immich-app/immich/pull/13413
### 🌐 Translations
* chore(mobile): added 'ignore_icloud' translation item by @rgomulin in https://github.com/immich-app/immich/pull/12788
* chore(web): update translations by @weblate in https://github.com/immich-app/immich/pull/13126

## New Contributors
* @Yagnap made their first contribution in https://github.com/immich-app/immich/pull/13129
* @yoni13 made their first contribution in https://github.com/immich-app/immich/pull/13226
* @Itoktsnhc made their first contribution in https://github.com/immich-app/immich/pull/13297
* @Mraedis made their first contribution in https://github.com/immich-app/immich/pull/13244
* @maexled made their first contribution in https://github.com/immich-app/immich/pull/12399
* @rgomulin made their first contribution in https://github.com/immich-app/immich/pull/12788
* @yashrajjain726 made their first contribution in https://github.com/immich-app/immich/pull/13299
* @Pranav-8bit made their first contribution in https://github.com/immich-app/immich/pull/12959
* @lyynd made their first contribution in https://github.com/immich-app/immich/pull/13409
* @fa1seut0pia made their first contribution in https://github.com/immich-app/immich/pull/13414

**Full Changelog**: https://github.com/immich-app/immich/compare/v1.117.0...v1.118.0