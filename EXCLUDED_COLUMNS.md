# Excluded Columns Documentation

This document lists columns present in the original PowerShell RdsDiscovery.csv that are **intentionally excluded** from the Python CLI/MCP implementation.

## Classification Legend

- ✅ **NEEDED**: Column provides value and should be retained if doing business assessment
- ❌ **SAFELY DELETE**: Column can be removed without losing technical or business value

## Business/Survey Columns (Not Technical Data)

The following columns are business assessment questions that must be filled manually by stakeholders. They are not derived from SQL Server technical analysis and are therefore excluded:

### 1. ✅ NEEDED: "Where is the current SQL Server workload running on, OnPrem[1], EC2[2], or another Cloud[3]?"
   - **Type**: Business question
   - **Reason**: Manual input required, not automated technical assessment
   - **Value**: Helps categorize source environment for migration planning
   - **Note**: Python tool auto-detects "RDS" vs "EC2/OnPrem" in the "Sql server Source" column

### 2. ✅ NEEDED: "Do you currently own any SQL Server licenses that you could bring to the Cloud? Y\N"
   - **Type**: Licensing question
   - **Reason**: Business decision, not technical data
   - **Value**: Critical for BYOL (Bring Your Own License) vs License Included pricing decisions

### 3. ✅ NEEDED: "Are you using perpetual license and paying software assurance? Y\N"
   - **Type**: Licensing question
   - **Reason**: Business decision, not technical data
   - **Value**: Determines eligibility for License Mobility through Software Assurance

### 4. ✅ NEEDED: "Are you using subscription license and paying subscription cost? Y\N"
   - **Type**: Licensing question
   - **Reason**: Business decision, not technical data
   - **Value**: Impacts cost comparison and migration ROI calculations

### 5. ✅ NEEDED: "will you be open to consider using a managed service with License Included, assuming we could make the economics work? Y\N"
   - **Type**: Business preference question
   - **Reason**: Stakeholder decision, not technical data
   - **Value**: Guides recommendation between RDS (managed) vs EC2 (self-managed)

### 6. ❌ SAFELY DELETE: "Do you see value of having AWS manage your SQL databases? Y\N"
   - **Type**: Business preference question
   - **Reason**: Stakeholder decision, not technical data
   - **Redundant**: Duplicate of question #5 above
   - **Recommendation**: Remove to avoid redundancy

### 7. ✅ NEEDED: "Then what are the primary motivations (e.g. cost saving, staff productivity, operational resilience, business agility)?"
   - **Type**: Business motivation question
   - **Reason**: Stakeholder input, not technical data
   - **Value**: Helps prioritize migration approach and success metrics

### 8. ✅ NEEDED: "What is the timeline for SQL Server migration to the Cloud? (Please input an estimated target date in No of Months)"
   - **Type**: Project planning question
   - **Reason**: Business timeline, not technical data
   - **Value**: Critical for project planning and resource allocation

## Non-Functional Technical Columns

### 9. ❌ SAFELY DELETE: "Free Check"
   - **Type**: Technical field
   - **Reason**: PowerShell implementation hardcodes this to 'N' for all servers
   - **Non-Functional**: The column provides no actual value - always returns 'N'
   - **PowerShell Code**: `'N' # Free Check - hardcoded`
   - **Recommendation**: Remove to avoid confusion with placeholder data

### 10. ❌ SAFELY DELETE: "Online Indexes"
   - **Type**: Technical field
   - **Reason**: Not present in RDSDiscoveryGuidev5.ps1 (the reference implementation)
   - **Status**: Appears in newer PowerShell versions but not part of core 18-feature compatibility check
   - **Impact**: Not used in RDS compatibility determination
   - **Recommendation**: Remove for consistency with v5 specification, or implement if using newer PowerShell version

## Rationale

The Python CLI/MCP implementation focuses exclusively on **automated technical assessment** of SQL Server instances. Business questions and non-functional fields are excluded to:

- Maintain clear separation between technical analysis and business assessment
- Avoid confusion with hardcoded/placeholder values
- Ensure consistency with PowerShell v5 specification
- Streamline automated batch processing

## Alternative Approach

If business assessment data is needed, it should be:
1. Collected separately through a business questionnaire
2. Merged with technical assessment results in a post-processing step
3. Managed in a separate workflow from automated technical discovery

## Added Columns (Improvements)

The Python implementation adds the following columns not in PowerShell:

- **isSSIS**: Detects SQL Server Integration Services
- **isSSRS**: Detects SQL Server Reporting Services  
- **Note**: Provides assessment status and error messages

These additions enhance the technical assessment without adding business questions.

---

## Summary Table

| # | Column Name | Type | Status | Rationale |
|---|-------------|------|--------|-----------|
| 1 | Where is workload running | Business | ✅ NEEDED | Categorizes source environment (but auto-detected in "Sql server Source") |
| 2 | Own SQL licenses (BYOL) | Business | ✅ NEEDED | Critical for licensing/pricing decisions |
| 3 | Perpetual license + SA | Business | ✅ NEEDED | Determines License Mobility eligibility |
| 4 | Subscription license | Business | ✅ NEEDED | Impacts cost comparison and ROI |
| 5 | Open to managed service | Business | ✅ NEEDED | Guides RDS vs EC2 recommendation |
| 6 | Value of AWS managing DBs | Business | ❌ DELETE | Redundant with #5 |
| 7 | Primary motivations | Business | ✅ NEEDED | Prioritizes migration approach |
| 8 | Migration timeline | Business | ✅ NEEDED | Critical for project planning |
| 9 | Free Check | Technical | ❌ DELETE | Hardcoded to 'N', non-functional |
| 10 | Online Indexes | Technical | ❌ DELETE | Not in v5, not used in compatibility check |

**Summary**: 7 columns NEEDED for business assessment, 3 columns can be SAFELY DELETED (1 redundant, 2 non-functional)
