---
name: accessibility-audit
description: Professional web accessibility testing directly into AI assistant. Scan websites and generate comprehensive reports showing accessibility issues based on WCAG 2.2 standards. Use this skill when users need to audit websites for accessibility compliance, check WCAG conformance, identify barriers for users with disabilities, or generate accessibility reports.
license: Apache 2.0
---

# Accessibility Audit Agent

A semi-automated accessibility audit tool that performs comprehensive WCAG 2.2 compliance testing on websites using axe-core, the industry-standard accessibility testing engine.

## When to Use This Skill

Use this skill when the user needs to:
- Audit a website for accessibility issues
- Check WCAG 2.2 conformance (Level A, AA, or AAA)
- Generate accessibility compliance reports
- Identify barriers for users with disabilities
- Test web pages before deployment
- Create documentation for accessibility improvements
- Compare accessibility across multiple pages or sites

## Overview

This skill provides automated accessibility testing using axe-core via Selenium WebDriver. It scans web pages, identifies accessibility violations based on WCAG 2.2 guidelines, and generates comprehensive reports in multiple formats (HTML, Markdown, JSON).

The skill operates in a semi-automated way:
1. Run automated scans using axe-core
2. Generate detailed reports with violation details
3. Provide context and recommendations for fixes
4. Support batch auditing of multiple URLs

## Prerequisites

Before running accessibility audits, ensure the required dependencies are installed:

```bash
# Install Selenium
pip install selenium --break-system-packages

# Install Chrome/Chromium (if not already installed)
# On Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver

# On other systems, ensure Chrome is installed and chromedriver is in PATH
```

## Core Workflow

### 1. Single URL Audit

To audit a single URL:

```bash
cd /mnt/skills/user/accessibility-audit
python scripts/audit.py "https://example.com" --conformance AA --output /mnt/user-data/outputs/audit.json
```

Parameters:
- `url`: The URL to audit (required)
- `--conformance` or `-c`: WCAG level (A, AA, or AAA). Default: AA
- `--output` or `-o`: Path to save JSON results
- `--visible`: Run browser in visible mode (for debugging)

### 2. Multiple URL Audit

To audit multiple URLs:

```bash
python scripts/audit.py "https://example.com" "https://example.com/about" "https://example.com/contact" \
  --conformance AA \
  --output /mnt/user-data/outputs/audits/
```

When auditing multiple URLs, `--output` should be a directory where individual JSON files will be saved.

### 3. Generate Reports

After running an audit, generate human-readable reports:

```bash
# Generate all formats (HTML + Markdown)
python scripts/report_generator.py /mnt/user-data/outputs/audit.json --format all --output /mnt/user-data/outputs/reports/

# Generate only HTML
python scripts/report_generator.py audit.json --format html --output report.html

# Generate only Markdown
python scripts/report_generator.py audit.json --format markdown --output report.md
```

The HTML report includes:
- Visual summary with accessibility score
- Violations grouped by severity (critical, serious, moderate, minor)
- Interactive details showing affected elements
- Links to remediation resources
- Professional styling for presentations

The Markdown report includes:
- Text-based summary suitable for documentation
- Detailed violation descriptions
- Code snippets of affected elements
- WCAG criterion references

## Interpreting Results

### Audit Output Structure

The audit produces JSON with the following structure:

```json
{
  "url": "https://example.com",
  "timestamp": "2025-10-17T10:30:00",
  "conformance_level": "WCAG 2.2 Level AA",
  "summary": {
    "violations": 12,
    "passes": 45,
    "incomplete": 3,
    "inapplicable": 8
  },
  "violations": [...],
  "passes": [...],
  "incomplete": [...],
  "inapplicable": [...]
}
```

Key fields:
- **violations**: Accessibility issues that failed automated testing
- **passes**: Rules that passed successfully
- **incomplete**: Items requiring manual review (e.g., contrast on images)
- **inapplicable**: Rules that don't apply to this page

### Violation Severity Levels

axe-core categorizes violations by impact:

1. **Critical**: Serious impact on users, must fix immediately
   - Missing form labels
   - Missing alt text on informative images
   - Keyboard traps

2. **Serious**: Significant barriers for some users
   - Insufficient color contrast
   - Missing landmark regions
   - Improper heading hierarchy

3. **Moderate**: Noticeable issues that should be fixed
   - Missing page language
   - Empty links
   - Redundant links

4. **Minor**: Minor annoyances, fix when possible
   - Suboptimal ARIA usage
   - Missing skip links

### Understanding Violations

Each violation includes:
- **description**: What the issue is
- **help**: How to understand the problem
- **helpUrl**: Link to detailed remediation guide
- **impact**: Severity level
- **tags**: WCAG criteria (e.g., wcag2a, wcag21aa, wcag22aa)
- **nodes**: Affected HTML elements with selectors

## Common Usage Patterns

### Pattern 1: Quick Single-Page Audit

```bash
# Audit and generate reports in one workflow
python scripts/audit.py "https://example.com" -o audit.json
python scripts/report_generator.py audit.json --format all -o reports/
```

Then provide the user with links to the generated reports in `/mnt/user-data/outputs/reports/`.

### Pattern 2: Multi-Page Site Audit

```bash
# Audit homepage and key pages
python scripts/audit.py \
  "https://example.com" \
  "https://example.com/about" \
  "https://example.com/products" \
  "https://example.com/contact" \
  --output audits/

# Generate individual reports for each page
for json_file in audits/*.json; do
  python scripts/report_generator.py "$json_file" --format all -o "reports/$(basename $json_file .json)/"
done
```

### Pattern 3: Progressive Enhancement Tracking

```bash
# Initial audit
python scripts/audit.py "https://staging.example.com" -o baseline.json

# After fixes, audit again
python scripts/audit.py "https://staging.example.com" -o after-fixes.json

# Compare violation counts to show improvement
```

### Pattern 4: Conformance Level Testing

```bash
# Test at different conformance levels
python scripts/audit.py "https://example.com" -c A -o level-a.json
python scripts/audit.py "https://example.com" -c AA -o level-aa.json
python scripts/audit.py "https://example.com" -c AAA -o level-aaa.json
```

## Providing Guidance to Users

When presenting audit results to users, follow this structure:

### 1. Executive Summary
Provide a high-level overview:
- Total violations by severity
- Accessibility score (passes / total checks)
- Conformance level tested
- Priority issues to address first

### 2. Critical Issues First
Focus on critical and serious violations that create significant barriers:
- Explain the impact on users
- Show specific examples from their site
- Provide clear remediation steps

### 3. Reference WCAG Guidelines
For each violation category, reference the relevant WCAG success criterion from `references/wcag_guidelines.md`:
- Explain what the criterion requires
- Why it matters for accessibility
- How to implement the fix

### 4. Actionable Recommendations
Provide concrete next steps:
- Prioritized fix list (critical → serious → moderate → minor)
- Code examples showing before/after
- Suggest tools for ongoing testing (browser extensions, CI/CD integration)

## Advanced Usage

### Custom axe-core Configuration

To run audits with custom axe rules or options, modify the audit script:

```python
# In audit.py, modify the axe.run() call:
results = self.driver.execute_script("""
    return axe.run({
        runOnly: {
            type: 'tag',
            values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice']
        },
        rules: {
            'color-contrast': { enabled: true },
            'duplicate-id': { enabled: false }
        }
    });
""")
```

### Integrating with CI/CD

To use this skill in continuous integration:

```bash
# Run audit and check for violations
python scripts/audit.py "$URL" -o audit.json
violations=$(python -c "import json; print(json.load(open('audit.json'))['summary']['violations'])")
if [ "$violations" -gt 0 ]; then
  echo "Accessibility violations found: $violations"
  exit 1
fi
```

### Testing Authenticated Pages

For pages requiring authentication, modify the audit script to handle login:

```python
# Before running the audit:
self.driver.get("https://example.com/login")
# Add login automation here
self.driver.find_element(By.ID, "username").send_keys("user")
self.driver.find_element(By.ID, "password").send_keys("pass")
self.driver.find_element(By.ID, "submit").click()
```

## Limitations and Manual Testing

Automated testing with axe-core covers approximately 57% of WCAG issues. The following require manual testing:

1. **Keyboard Navigation**: Manually verify all interactive elements are keyboard accessible
2. **Screen Reader Testing**: Test with NVDA, JAWS, or VoiceOver
3. **Color Contrast on Images**: Verify text overlaid on images meets contrast requirements
4. **Cognitive Load**: Assess clarity and simplicity of content
5. **Multimedia**: Verify captions, transcripts, and audio descriptions
6. **Focus Management**: Check focus order and visual focus indicators

Inform users that automated audits should be complemented with:
- Manual keyboard-only testing
- Screen reader testing
- User testing with people with disabilities

## Reference Materials

The skill includes comprehensive WCAG 2.2 documentation:
- `references/wcag_guidelines.md`: Complete WCAG 2.2 reference with success criteria, common violations, and fixes

When explaining accessibility issues to users, consult this reference to provide:
- Specific WCAG criterion numbers
- Conformance level requirements
- Detailed remediation guidance

## Example Interactions

### Example 1: Basic Audit Request
**User**: "Can you audit my website for accessibility?"

**Response**:
1. Ask for the URL
2. Ask for conformance level (suggest AA as standard)
3. Run audit.py with appropriate parameters
4. Generate HTML and Markdown reports
5. Provide summary of findings with links to detailed reports
6. Highlight critical issues requiring immediate attention

### Example 2: Multi-Page Audit
**User**: "I need to audit my entire website's main pages"

**Response**:
1. Ask for list of URLs or offer to audit common pages (home, about, contact, etc.)
2. Run batch audit
3. Generate individual reports for each page
4. Create summary showing which pages have the most issues
5. Provide prioritized recommendations

### Example 3: Explaining Violations
**User**: "What does 'color contrast' violation mean?"

**Response**:
1. Consult `references/wcag_guidelines.md` for WCAG 1.4.3
2. Explain the requirement (4.5:1 ratio for normal text)
3. Show why it matters (users with low vision)
4. Provide examples from their audit results
5. Suggest tools to check contrast ratios
6. Give before/after code examples

## Best Practices

1. **Start with Level AA**: This is the industry standard and legally required in many jurisdictions
2. **Prioritize by Impact**: Focus on critical and serious violations first
3. **Provide Context**: Explain why each violation matters for real users
4. **Show Examples**: Use actual elements from the user's site in explanations
5. **Offer Solutions**: Don't just identify problems, provide clear remediation steps
6. **Encourage Iteration**: Accessibility is ongoing; suggest regular testing
7. **Recommend Manual Testing**: Remind users that automated testing is just the first step

## Troubleshooting

### Chrome/Chromium Not Found
If the audit script fails to launch Chrome:
```bash
# Install Chromium
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### Selenium Import Error
```bash
pip install selenium --break-system-packages
```

### Page Timeout
For slow-loading pages, increase the timeout in audit.py:
```python
WebDriverWait(self.driver, 30).until(...)  # Increase from 10 to 30 seconds
```

### axe-core Loading Failed
If axe-core fails to load from CDN, the script will report this error. Check internet connectivity.

## Summary

This skill provides professional-grade accessibility auditing capabilities, enabling users to:
- Quickly identify WCAG 2.2 compliance issues
- Generate comprehensive, shareable reports
- Understand accessibility barriers and how to fix them
- Track improvements over time
- Build more inclusive web experiences

Always supplement automated testing with manual testing and user feedback for comprehensive accessibility assurance.
