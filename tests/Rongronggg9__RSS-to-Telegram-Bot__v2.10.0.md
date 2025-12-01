### Highlights

- **Container health check**: The official Docker image includes an automatic health check to determine if the container is running properly. The health check status can be checked in `docker ps`. This feature, combined with [`autoheal`](https://github.com/willfarrell/docker-autoheal) or some other monitoring tool, can restart the container automatically when it is unhealthy.
- **Support for chat-specific #hashtags**: Telegram recently added a feature called "chat-specific hashtags," formatting as `#hashtag@username`. However, escaping '@' broke these hashtags. Properly supports such hashtags by allowing '@' in hashtags.

### Enhancements

- **No longer proxies images from `*.wp.com` when generating Telegraph posts**: `*.wp.com` is in the blocklist of `wsrv.nl` (environment variable `IMAGES_WESERV_NL`). Thus, these images are no longer proxied when generating Telegraph posts. All images from `*.wp.com` can be accessed with any referer header, so they are now kept as is.
- **Link to repo in UA**: The default User-Agent now contains a link to the repository, which can help webmasters identify the source of traffic and add RSStT into their allowlists.
- **Minor enhancements**: Some internal functions have been refined to enhance compatibility with various feeds.
- **Minor refactor**: Some internal functions have been refactored to improve performance, readability and maintainability.

### Bug fixes

- **Canonical `DATABASE_URL` not recognized**: Since v2.9.0, `DATABASE_URL` is canonicalized before connecting to the corresponding database. However, a canonical URL pointing to a local path cannot be recognized when checking the validity of the scheme (database type). Both canonical (`scheme:/path/to/file.db`) and traditional (`scheme:///path/to/file.db`) forms of such URLs are recognized correctly now.
- **Monitoring not deferred as per server-side cache when subscribing**: Since v2.7.0, monitoring tasks will be deferred when aggressive server-side caches (e.g., Cloudflare and RSSHub, which make it futile to check for updates before cache expiration) are detected. However, the first monitoring task for a newly subscribed feed was not being deferred. This has been fixed and the first monitoring task now waits for the server-side cache to expire.
- **Minor bug fixes**

<hr>

## v2.10.0: 容器健康检查、特定于聊天的 #hashtag 和更多

### 亮点

- **容器健康检查**: 官方 Docker 镜像现在包含自动健康检查，用于确定容器是否正常运行。健康检查状态可以在 `docker ps` 中查看。结合 [`autoheal`](https://github.com/willfarrell/docker-autoheal) 或其他监控工具，当容器不健康时可以自动重启容器。
- **支持特定于聊天的 #hashtag**: Telegram 最近添加了一个名为“特定于聊天的 hashtag”的功能，格式为 `#hashtag@username`。然而，转义 `@` 会破坏这些 hashtag。通过在 hashtag 中允许 `@` 来正确地支持这类 hashtag。

### 增强

- **生成 Telegraph 文章时，不再代理来自 `*.wp.com` 的图像**: `*.wp.com` 位于 `wsrv.nl` (环境变量 `IMAGES_WESERV_NL`) 的阻断列表中。因此，在生成 Telegraph 文章时，这些图像不再被代理。来自 `*.wp.com` 的所有图片都可以用任何 refer 头访问，因此它们现在保持原样。
- **UA 中的仓库链接**: 默认的 User-Agent 现在包含一个指向仓库的链接，这可以帮助网站管理员识别流量来源并将 RSStT 添加到白名单中。
- **次要的增强**: 改进了一些内部函数以增强与各种 feed 的兼容性。
- **次要的重构**: 重构了一些内部函数以提高性能、可读性和可维护性。

### Bug 修复

- **无法识别规范的 `DATABASE_URL`**: 自 v2.9.0 起, 在连接到相应的数据库之前，`DATABASE_URL` 被规范化。然而，在检查 scheme (数据库类型) 的合法性时，无法识别指向本地路径的规范 URL。现在，此类 URL 的规范 (`scheme:/path/to/file.db`) 和传统 (`scheme:///path/to/file.db`) 形式都被正确识别。
- **订阅时不会根据服务端缓存延迟监控**：自 v2.7.0 起，当检测到激进的服务器端缓存时，监控任务将被延迟（例如 Cloudflare 和 RSSHub，它们使得在缓存过期之前检查更新变得徒劳无功）。但是，当新订阅 feed 时，第一个监视任务不会被推迟。该问题已修复，第一个监控任务会等待服务端缓存过期。
- **次要的 bug 修复**