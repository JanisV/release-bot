**CI Report:**

https://ci-tests.linuxserver.io/linuxserver/cops/3.8.2-ls279/index.html

**LinuxServer Changes:**

**Full Changelog**: https://github.com/linuxserver/docker-cops/compare/3.8.2-ls278...3.8.2-ls279

**Remote Changes:**

See [release 3.1.1](https://github.com/mikespub-org/seblucas-cops/releases/tag/3.1.1) for breaking changes for COPS 3.x

## Change log
### 3.8.2 - 20251127 Use form authentication + update packages & readers
  * Changes in config/default.php file:
    - add $config['cops_form_authentication'] option to use form authentication
  * Update php/npm packages and ebook readers
  * Drop loading user-specific config before auth in config/config.php
  * Use new AuthMiddleware to handle authentication + update Config
  * Support form authentication with login.html again - see PR #161 from @dcoffin88

### 3.8.0 - 20251011 Add custom readers, database config files + prepare symfony upgrade 
  * Changes in config/default.php file:
    - add $config['cops_epub_reader'] option to use custom reader template
    - add $config['cops_comic_reader'] option to use codedread-kthoom template
  * Prepare upgrade of symfony/* packages to new 7.4 LTS version
  * Support custom reader template for epub files too
  * Add option to use different comic reader based on kthoom from @codedread
  * Move admin templates to subdirectory and use Twig template engine
  * Support user-specific or common database config files - see issue #160 from @tgiraud
  * Add minimal mozilla/pdfjs-dist to release package cops-3.x.x-php82.zip
  * Upgrade mozilla/pdfjs-dist to v5.4.296 and refresh pdfjs-viewer template
  * Hide dropzone in comic-reader if url is specified

**Full Changelog**: https://github.com/mikespub-org/seblucas-cops/compare/3.7.8...3.8.2