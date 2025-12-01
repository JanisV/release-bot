## 🚀 urllib3 is fundraising for HTTP/2 support

[urllib3 is raising ~$40,000 USD](https://sethmlarson.dev/urllib3-is-fundraising-for-http2-support) to release HTTP/2 support and ensure long-term sustainable maintenance of the project after a sharp decline in financial support. If your company or organization uses Python and would benefit from HTTP/2 support in Requests, pip, cloud SDKs, and thousands of other projects [please consider contributing financially](https://opencollective.com/urllib3) to ensure HTTP/2 support is developed sustainably and maintained for the long-haul.

Thank you for your support.

# Security issues

urllib3 2.5.0 fixes two moderate security issues:
- Pool managers now properly control redirects when `retries` is passed — CVE-2025-50181 reported by @sandumjacob (5.3 Medium, GHSA-pq67-6m6q-mj2v)
- Redirects are now controlled by urllib3 in the Node.js runtime — CVE-2025-50182 (5.3 Medium, GHSA-48p4-8xcf-vxj5)


# Features

- Added support for the `compression.zstd` module that is new in Python 3.14. See [PEP 784](https://peps.python.org/pep-0784/) for more information. (#3610)
- Added support for version 0.5 of `hatch-vcs` (#3612)


# Bugfixes

- Raised exception for `HTTPResponse.shutdown` on a connection already released to the pool. (#3581)
- Fixed incorrect `CONNECT` statement when using an IPv6 proxy with `connection_from_host`. Previously would not be wrapped in `[]`. (#3615)