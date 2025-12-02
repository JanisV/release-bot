> [!NOTE]
> A problem has been reported where the AppImage cannot be run on some previous OS versions,
> leading to the release of version v2 specifically for the AppImage binary. Further information: #3781, https://github.com/sqlitebrowser/sqlitebrowser/discussions/3775#discussioncomment-10969170

This is a new release with several improvements over the v3.13.0 release from three months ago. :rocket:

As a special mention, SQLean has a new `time` extension! Check out the following link for more information: https://github.com/nalgeon/sqlean/blob/main/docs/time.md

Thanks to everyone for being part of our Community!

Related Discussion: https://github.com/sqlitebrowser/sqlitebrowser/discussions/3775

### Changelog
#### Added
- Add links to the wiki as help for many dialogs (7af1256, b5abc86)

#### Changed
- Change the default to install a shortcut to the Start menu when installing on Windows (623bec6)
- Improve icon image for links in 'Help' menu (#3693, 027c6a8)
- Pragma names and values can now be translated (#3697, bf62f3a, ad00ad4)
- Remove trailing characters when copying a single cell (#3735, 20f481a)
- Update AppImage binary to use the latest SQLCipher library (#3744, 21ba2d0)
- When editing the DB cells, expanded queries with parameters are included in the SQL Log (ac3209f)

#### Fixed
-  ExtendedTableWidget
    - Fix an issue that prevented autocomplete from working in some race conditions (#2567, #3706)
    - Use Tab to close autocomplete popup and move to next item (3aff8c9)
    - Troubleshoot 'Copy as SQL' action on a cell results in string being copied (#1952, 1ebe7bf)

- Global
    - Fix "Argument Missing" error in Korean translation (#3635, #3692, cd518de)
    - Fix an issue that caused apps to crash on some older versions of macOS (#3691)
    - Fix an issue when freezing after stopping a pragma (#3742, 15a9620)
    - Fix an issue with outputting the wrong version on macOS
    - Troubleshooting poor HiDPI support on Windows (#3684)
    - Troubleshoot SQL queries containing VACUUM that run incorrectly (#3723, 51784aa)

- MainWindow
    - Fix an issue when selecting queries containing multi-byte strings (#3731, f89097c)

- TableBrowser
    - Fix a bug where the first row was not adjusted (#3767, ad690e7)

- etc
    - Fix misleading links to Qt license information (8361aa5)
    - Replace 'http' with 'https' in the 'AboutDialog' and 'MainWindow' (9832a52)
    - Translation
        - German (#3749, 8e38bf0)
        - Indonesian (#3756, 6100595)
        - Japanese (#3755, e0f6aea)
        - Korean (7bbfcf9)
        - Simplified Chinese (#3761, 9eb0a5a)
        - Spanish (ac33918)

### Dependent library version information for each OS
|     **-**    |                     [**Qt**](https://www.qt.io/)                     |            [**SQLCipher**](https://www.zetetic.net/sqlcipher/)            |            [**SQLite**](https://sqlite.org/)            |         [**SQLean**](https://github.com/nalgeon/sqlean)         |
|:------------:|:--------------------------------------------------------------------:|:-------------------------------------------------------------------------:|:-------------------------------------------------------:|:---------------------------------------------------------------:|
| **AppImage** |          [5.12.8](https://www.qt.io/blog/qt-5.12.8-released)         | [4.6.1](https://www.zetetic.net/blog/2024/08/20/sqlcipher-4.6.1-release/) |                      Not applicable                     |                          Not applicable                         |
|   **macOS**  | [5.15.13](https://www.qt.io/blog/commercial-lts-qt-5.15.13-released) | [4.6.1](https://www.zetetic.net/blog/2024/08/20/sqlcipher-4.6.1-release/) |                      Not applicable                     | [0.27.1](https://github.com/nalgeon/sqlean/releases/tag/0.27.1) |
|  **Windows** |          [5.15.2](https://www.qt.io/blog/qt-5.15.2-released)         | [4.6.1](https://www.zetetic.net/blog/2024/08/20/sqlcipher-4.6.1-release/) | [3.46.1](https://www.sqlite.org/releaselog/3_46_1.html) | [0.27.1](https://github.com/nalgeon/sqlean/releases/tag/0.27.1) |


### SHA256SUMS
- DB.Browser.for.SQLite-v3.13.1-win32.msi
    - e0b9f86d3da4d8d800e144295487e43de306c1bd27f14dccfe41e904736f25f7
- DB.Browser.for.SQLite-v3.13.1-win32.zip
    - 917ad2fa8d36e3bfa3fc85b11a34a8c18d189fbc2289f5a0d3bf41de8a288edc
- DB.Browser.for.SQLite-v3.13.1-win64.msi
    - d023d54b3a5db10c7e896089bb3dbe6e7f4bc4eaa9bbecb34ca414be5970f688
- DB.Browser.for.SQLite-v3.13.1-win64.zip
    - 22375e275ec42d96de1d3b8e9ea4ed86d2a3505c4d0ffcbd1af67aa4003e5e4d
- DB.Browser.for.SQLite-v3.13.1-x86.64-v2.AppImage
    - c2fd0c27c84777747527e1b28deccc824bc88eeb47f36a9575bf1ba0a5a38453
- DB.Browser.for.SQLite-v3.13.1.dmg
    - a641cfbfcc2ce609f07de44a35134dab53485ecc18e6d9afa297b514d74bd75e
- SQLiteDatabaseBrowserPortable_3.13.1.paf.exe
	- dee51170538a2e5bffdd281c96680e1856d0b7440f5042c1a127db3b5e193ccb