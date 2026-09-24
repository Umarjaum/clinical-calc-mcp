# Security policy

## Supported versions

Security fixes are applied to the latest released version and the current default branch. Users should upgrade to the latest release where possible.

## Reporting a vulnerability

Please do not report exploitable vulnerabilities in a public issue. Use GitHub's private vulnerability reporting feature for this repository. If private reporting is unavailable, contact the repository maintainer privately through GitHub before disclosing details publicly. Include affected version, reproduction steps, and impact, but do not include patient data, secrets, or personal information.

This project is local-only by design: calculation tools make no network requests, read no patient files, store no patient information, and do not log inputs. MCP client behavior and deployment security are outside the package and should be assessed separately.
