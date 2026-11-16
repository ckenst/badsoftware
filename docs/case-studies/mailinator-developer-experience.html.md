# The Bad Software Company Case Study - Restoring Mailinator's Developer Experience

Source: https://badsoftware.com/case-studies/mailinator-developer-experience.html

Summary: Creating an API source of truth, modernizing four SDKs, and measuring adoption of the resulting releases.

# Restoring Mailinator's Developer Experience

Creating an API source of truth, modernizing four SDKs, and measuring adoption of the resulting releases.

## Project snapshot

| Project | Details |
|---|---|
| Organization | Mailinator |
| Project type | API documentation and SDK modernization |
| Period | 2025–2026 |
| Scope | OpenAPI specification, developer documentation, examples, tests, and the Ruby, JavaScript, Python, and C# SDKs |
| Initial condition | No current source of truth for the API; broken endpoints; outdated SDKs; inconsistent or missing examples |
| Initial measured result | Ruby downloads increased 64.5%; JavaScript downloads increased 24.4%; recent downloads shifted toward the updated releases |
| Follow-up evidence | JavaScript growth continued; Python package downloads increased after 1.0.9; updated Ruby and C# releases continued to receive downloads |

## Executive summary

Mailinator's developer documentation was old, omitted product features, and could no longer describe the complete API. There was no current specification to use as a source of truth, so the work began by testing the running product and reconciling its behavior with the available documentation.

That investigation found endpoints that were completely broken, behavior that had changed, and operations that no longer belonged in the public interface. It also showed that every official SDK was out of date. The clients exposed different subsets of the product, implemented some requests incorrectly, and offered examples that varied widely by language or were missing altogether.

The work produced an OpenAPI specification for the Mailinator API, updated documentation, and modernization work across the Ruby, JavaScript, Python, and C# clients. In the initial post-release measurement, Ruby and JavaScript showed the clearest evidence of adoption: their download rates increased, and most recent downloads moved to versions containing the new work. A follow-up through November 12, 2026 found continued JavaScript growth, increased Python package activity, and continued downloads of the updated Ruby and C# releases.

## The challenge

The original task appeared to be a documentation update. Three conditions made it a larger engineering problem:

1. **The documentation was not authoritative.** It was old and missing features, but there was no current API contract against which to correct it.
2. **The running product was inconsistent.** Testing the existing API exposed endpoints that were broken, changed, replaced, or obsolete.
3. **The client libraries had drifted independently.** Every official SDK was out of date. Features, request behavior, deprecation status, examples, and tests varied between languages.

Rewriting the documentation alone would have made one part of the developer experience clearer while leaving the underlying disagreements intact.

## The approach

### 1. Establish the current behavior

The running product became the starting point. Existing endpoints were exercised to determine what worked, what had changed, and what was broken. Available documentation and implementation behavior were compared rather than assuming either one was correct.

### 2. Create the API specification

An [OpenAPI specification](https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml) was created to describe the available endpoints, parameters, request bodies, response models, and deprecated behavior in one place.

The specification gave the API documentation a defined contract. It also made discrepancies testable: an SDK operation either aligned with the contract or it did not.

### 3. Update the documentation

The developer documentation was reorganized and updated against the specification. Missing API operations were documented, incorrect material was corrected, and newer examples were added. The specification also supported generated endpoint documentation, reducing the amount of API reference material that had to be maintained independently.

### 4. Compare the SDKs with the contract

The assessment found that all of Mailinator's official SDKs were out of date. Remediation focused first on the Ruby, JavaScript, Python, and C# clients.

The comparison uncovered missing message retrieval and streaming operations, incorrect paths and parameters, incomplete response models, and unsupported or obsolete operations that were still presented as current.

### 5. Repair the clients and their surrounding systems

The SDK work included:

- Adding missing API operations and query parameters.
- Correcting request paths, payloads, and response models.
- Marking obsolete operations as deprecated.
- Adding regression coverage for corrected behavior.
- Separating offline tests from integration tests that required credentials.
- Adding or standardizing installation instructions, examples, reference material, and changelogs.
- Updating dependencies and addressing known security vulnerabilities.
- Documenting how to compare each client with the OpenAPI specification as the API evolves.

The objective was not to make the language repositories identical. It was to make them describe and access the same product while respecting the conventions of each ecosystem.

## Results

### A shared source of truth

Mailinator gained a machine-readable API contract that could inform its endpoint documentation and SDK maintenance. Changes no longer had to be reconstructed independently from old documentation and client implementations.

### New SDK releases

The first published releases containing this work were:

| SDK | First updated release | Publication date | Previous release gap |
|---|---:|---:|---:|
| JavaScript | 1.0.8 | February 11, 2026 | 9 months |
| Ruby | 1.0.7 | March 9, 2026 | 12 months |
| Python | 1.0.8 | April 12, 2026 | 13 months |
| C# | 1.0.7 | August 15, 2026 | 17 months |

Additional releases expanded API coverage, improved tests and examples, and updated dependencies.

### Release status as of November 12, 2026

| SDK | Latest release | Publication date | Releases containing this work |
|---|---:|---:|---:|
| JavaScript | 1.1.2 | August 15, 2026 | 6 |
| Ruby | 1.1.1 | August 15, 2026 | 3 |
| Python | 1.0.9 | August 15, 2026 | 2 |
| C# | 2.0.0 | September 29, 2026 | 2 |

These releases continued the alignment work. They added message retrieval, streaming, domain listing, and webhook operations; expanded offline and integration coverage; updated examples and maintenance guidance; and addressed dependency vulnerabilities. C# 2.0.0 also upgraded RestSharp across a public API boundary, requiring the major version change and migration guidance.

### Initial post-release measurement

Public package-registry data was compared across equal 90-day periods immediately before and after the first updated Ruby and JavaScript releases.

| SDK | Before | After | Change | Updated-version adoption |
|---|---:|---:|---:|---:|
| Ruby | 10.7 downloads/day | 17.6 downloads/day | **+64.5%** | 91% of recent downloads |
| JavaScript | 4,406 downloads/day | 5,483 downloads/day | **+24.4%** | 71% of recent weekly downloads |

Ruby provided the clearest result. Its download rate increased almost 65%, and recent downloads shifted overwhelmingly toward versions containing the new work.

JavaScript downloads increased approximately 24%. The package had already been growing, but its year-over-year growth also accelerated after the updated releases.

At that point, the other clients did not provide the same evidence. Updated Python versions received downloads, but the package's overall download rate had not increased during the initial observation window. The first C# release had not been available long enough for an equally strong comparison.

### Follow-up measurement

Registry data was checked again on November 12, 2026. Each ecosystem exposes different statistics, so the follow-up separates comparable rate measurements from cumulative evidence of adoption.

| SDK | Follow-up evidence | Result | What it supports |
|---|---|---:|---|
| JavaScript | August 14–November 11, 2026 compared with the same 90 days in 2025 | 6,667 vs. 3,221 downloads/day; **+107%** | Package growth continued year over year |
| Python | Equal 88-day periods before and after 1.0.9, excluding release day | 188.2 vs. 312.2 downloads/day; **+65.9%** | Overall package activity increased after the release |
| Ruby | Cumulative downloads of versions containing the work | 4,580 downloads; 1.1.1 received 1,933 | Updated releases continued to be adopted |
| C# | Cumulative downloads of versions containing the work | 5,576 downloads across 1.0.7 and 2.0.0 | Updated releases were adopted |

npm recorded 600,006 JavaScript package downloads in the 2026 follow-up window, compared with 289,911 over the same dates in 2025. This is evidence that the earlier growth did not disappear after the first updated releases, but it does not isolate the effect of any individual version.

Python's result changes the initial picture. PyPIStats data excluding known mirrors increased from 16,562 downloads before 1.0.9 to 27,471 afterward. Because the counts are package-wide rather than version-specific, the comparison shows increased package activity after the release, not adoption of 1.0.9 itself.

RubyGems and NuGet expose cumulative counts by version but not the historical daily version data needed to reconstruct equivalent before-and-after windows. Their totals show that developers downloaded the updated releases; they do not establish that the releases increased each package's overall rate.

## Measurement limits

Package downloads are not unique users or API requests. Registry counts include automated builds, dependency scanners, repeated installations, and other activity that cannot be separated into individual developers. PyPIStats excludes known mirrors but still includes CI/CD activity. npm reports package-wide downloads, while the RubyGems and NuGet figures used in the follow-up are cumulative version totals. Timing alone also cannot prove that the SDK releases caused the download increases.

The data supports a narrower conclusion: developers adopted the repaired releases; JavaScript growth continued; and Python package activity increased in the later comparison. That is evidence of distribution, package activity, and version adoption—not proof that the releases caused the changes or that package downloads became downstream Mailinator usage.

## End state

The project changed more than the documentation. Mailinator had a defined API contract, updated developer material, newer client releases, more consistent examples, and stronger tests around the behavior that had been repaired.

The documentation problem was where the maintenance gap became visible. Establishing a source of truth made it possible to find the connected problems and repair them systematically.

## Evidence sources

- [Mailinator API specification](https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml)
- [Ruby SDK](https://github.com/manybrain/mailinator-ruby-client), [changelog](https://github.com/manybrain/mailinator-ruby-client/blob/main/CHANGELOG.md), [RubyGems package](https://rubygems.org/gems/mailinator_client), and [version data](https://rubygems.org/api/v1/versions/mailinator_client.json)
- [JavaScript SDK](https://github.com/manybrain/mailinator-javascript-client), [changelog](https://github.com/manybrain/mailinator-javascript-client/blob/master/CHANGELOG.md), [npm package](https://www.npmjs.com/package/mailinator-client), and npm download data for the [2026](https://api.npmjs.org/downloads/point/2026-08-14:2026-11-11/mailinator-client) and [2025](https://api.npmjs.org/downloads/point/2025-08-14:2025-11-11/mailinator-client) comparison periods
- [Python SDK](https://github.com/manybrain/mailinator-python-client), [changelog](https://github.com/manybrain/mailinator-python-client/blob/master/CHANGELOG.md), [PyPI package](https://pypi.org/project/mailinator-python-client-2/), [PyPIStats data](https://pypistats.org/api/packages/mailinator-python-client-2/overall?mirrors=false), and [methodology](https://pypistats.org/faqs)
- [C# SDK](https://github.com/manybrain/mailinator-csharp-client), [changelog](https://github.com/manybrain/mailinator-csharp-client/blob/master/CHANGELOG.md), [NuGet package](https://www.nuget.org/packages/MailinatorApiClient), and [version data](https://azuresearch-usnc.nuget.org/query?q=packageid%3AMailinatorApiClient&prerelease=false)
