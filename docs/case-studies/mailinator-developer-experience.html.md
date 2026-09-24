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
| Measured result | Ruby downloads increased 64.5%; JavaScript downloads increased 24.4%; recent downloads shifted toward the updated releases |

## Executive summary

Mailinator's developer documentation was old, omitted product features, and could no longer describe the complete API. There was no current specification to use as a source of truth, so the work began by testing the running product and reconciling its behavior with the available documentation.

That investigation found endpoints that were completely broken, behavior that had changed, and operations that no longer belonged in the public interface. It also showed that every official SDK was out of date. The clients exposed different subsets of the product, implemented some requests incorrectly, and offered examples that varied widely by language or were missing altogether.

The work produced an OpenAPI specification for the Mailinator API, updated documentation, and modernization work across the Ruby, JavaScript, Python, and C# clients. After publication, Ruby and JavaScript showed the clearest evidence of adoption: their download rates increased, and most recent downloads moved to versions containing the new work.

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

### Evidence of adoption

Public package-registry data was compared across equal 90-day periods immediately before and after the first updated Ruby and JavaScript releases.

| SDK | Before | After | Change | Updated-version adoption |
|---|---:|---:|---:|---:|
| Ruby | 10.7 downloads/day | 17.6 downloads/day | **+64.5%** | 91% of recent downloads |
| JavaScript | 4,406 downloads/day | 5,483 downloads/day | **+24.4%** | 71% of recent weekly downloads |

Ruby provided the clearest result. Its download rate increased almost 65%, and recent downloads shifted overwhelmingly toward versions containing the new work.

JavaScript downloads increased approximately 24%. The package had already been growing, but its year-over-year growth also accelerated after the updated releases.

The other clients did not provide the same evidence. Updated Python versions received downloads, but the package's overall download rate did not increase. The C# release showed an early increase but had not been available long enough for an equally strong comparison.

## Measurement limits

Package downloads are not unique users or API requests. Registry counts include automated builds, dependency scanners, repeated installations, and other activity that cannot be separated into individual developers. Timing alone also cannot prove that the SDK releases caused the download increases.

The data supports a narrower conclusion: developers adopted the repaired Ruby and JavaScript releases, and most recent downloads moved to versions containing the new work. That is evidence of distribution and version adoption, not proof of downstream Mailinator usage.

## End state

The project changed more than the documentation. Mailinator had a defined API contract, updated developer material, newer client releases, more consistent examples, and stronger tests around the behavior that had been repaired.

The documentation problem was where the maintenance gap became visible. Establishing a source of truth made it possible to find the connected problems and repair them systematically.

## Evidence sources

- [Mailinator API specification](https://github.com/manybrain/mailinatordocs/blob/main/openapi/mailinator-api.yaml)
- [Ruby SDK](https://github.com/manybrain/mailinator-ruby-client) and [RubyGems package](https://rubygems.org/gems/mailinator_client)
- [JavaScript SDK](https://github.com/manybrain/mailinator-javascript-client) and [npm package](https://www.npmjs.com/package/mailinator-client)
- [Python SDK](https://github.com/manybrain/mailinator-python-client) and [PyPI package](https://pypi.org/project/mailinator-python-client-2/)
- [C# SDK](https://github.com/manybrain/mailinator-csharp-client) and [NuGet package](https://www.nuget.org/packages/MailinatorApiClient)
