————————

📌 __*v1\.118\.0*__

Welcome to release `v1.118.0` of Immich\. This version comes with several breaking changes, and also improvements to the mobile app UI and UX, a new documentation home page, as well as bug fixes and enhancements across the app\. We hope you enjoy this release\!

>*⚠️ Warning*
>✏ __*Breaking changes*__
>This release includes the following breaking changes:
>1\. Port alignment
>2\. Remove deprecated API endpoints
>3\. Remove deprecated `start.sh` arguments

📚 *1\. Port alignment*
We aligned the internal port of the `immich-server` to be similar to the binding port\. Please make the following change to your `docker-compose.yml` file under the `immich-server` section\. Reverse proxies using port 3001 also need to be updated to use port 2283\.

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

📚 *2\. Remove deprecated API endpoints*
The following endpoints were previously deprecated and have been removed, if you are a community project maintainer and using one of the endpoints below, please make sure to make changes to your project:
⦁ `/api/server-info/*` has been removed\. Use `/api/server/*` instead\.
⦁ `/api/people/:id/assets` has been removed\. Use `/api/search/metadata` instead\.
>*ⓘ Note*
>This includes `/api/server-info/ping`, `/api/server-info/version`, `/api/server-features`, `/api/server-info/config`, `/api/server-info/statistics`, and others\.

📚 *3\. Remove deprecated `start.sh` arguments*
The following docker commands have been removed:
⦁ `start.sh immich`
⦁ `start.sh microservices`
Follow the steps below to align `docker-compose.yml` with the default setup\.

**>*ⓘ Note*
>These steps are only required if you still have the `immich-microservices` section in your `docker-compose.yml` or didn't follow the previous instructions to remove the command section\. If you don't have the mentioned content below, you can ignore this

🔖 *1\. Update `docker-compose.yml`*

Remove the `command` line from `immich-server` and the entire `immich-microservices` service section as shown below\.

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

🔖 *2\. Remove the running `immich-microservices` container*
Run `docker compose down --remove-orphans` after updating `docker-compose.yml` to remove the old `immich-microservices` container\.

✏ __*Highlights*__

Some of the highlights for this release include the following:

⦁ Mobile UI/UX improvement
⦁ Option to refresh face detection
⦁ Color filters for editing photos
⦁ Timezone improvements
⦁ Deprecated release notes section
⦁ Better JPEG compression
⦁ Multi\-GPU support for ML
📚 *Mobile UI/UX improvement*

Thank you all for the great feedback from the [dicussion](https://github.com/immich-app/immich/discussions/12597) we made a month ago about the proposed changes to the mobile app layout\. We hope the following changes will provide more fluid experience when browing and managing your photos and videos\.

🔖 *Navigation bar*

Photos and albums are the two most used pages\. To make them more accessible, we replaced the `Sharing` page with a new `Albums` page where you can find all of the album related features and functions\.

🖼️https://github\.com/user\-attachments/assets/8020ae55\-8e79\-4cf0\-ba2c\-54ac56a9acb8

🔖 *Albums page*

This new page allows users to quickly view, sort, search, filter, create, and manage albums\.

🖼️https://github\.com/user\-attachments/assets/d5782994\-f0f8\-481f\-b89e\-c12b498b90b3

🔖 *Library page*

The library page now incl
\-\=SKIPPED\=\-