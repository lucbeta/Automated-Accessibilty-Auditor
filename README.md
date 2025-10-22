# Accessibility Audit Agent Skill

Professional web accessibility testing integrated into Claude. Scan websites and generate comprehensive WCAG 2.2 compliance reports.

## What This Skill Does

This skill enables Claude to:
- 🔍 Scan websites for accessibility issues using axe-core (industry-standard testing engine)
- 📊 Generate comprehensive reports in HTML, Markdown, and JSON formats
- ✅ Check compliance with WCAG 2.2 standards (Levels A, AA, AAA)
- 🎯 Identify specific elements that need fixing
- 📈 Track accessibility improvements over time
- 🔄 Audit multiple pages in batch

## Installation

### 1. Install the Skill

Upload the `accessibility-audit.zip` file to Claude via the Skills menu.

### 2. Install Dependencies

The skill requires Selenium and Chrome/Chromium. Claude will guide you through installation, but you can also run:

```bash
pip install selenium --break-system-packages
sudo apt-get install -y chromium-browser chromium-chromedriver
```

## Usage Examples

### Basic Audit

Simply ask Claude:
```
"Audit https://example.com for accessibility issues"
```

Claude will:
1. Run an automated WCAG 2.2 Level AA scan
2. Generate HTML and Markdown reports
3. Summarize critical issues
4. Provide actionable recommendations

### Multi-Page Audit

```
"Audit these pages for accessibility: 
- https://example.com
- https://example.com/about
- https://example.com/contact"
```

### Custom Conformance Level

```
"Audit my website for WCAG 2.2 Level AAA compliance"
```

### Explain Violations

```
"What accessibility issues did you find? Explain how to fix them."
```

## What You'll Get

### HTML Report
- Visual dashboard with accessibility score
- Violations grouped by severity (critical, serious, moderate, minor)
- Interactive details showing affected elements
- Direct links to fix documentation
- Professional styling for sharing with teams

### Markdown Report
- Text-based report for documentation
- Detailed violation descriptions
- Code snippets of problematic elements
- WCAG criterion references

### JSON Data
- Raw audit data for programmatic processing
- Complete violation details
- Integration with CI/CD pipelines

## Key Features

### Automated Testing
Uses axe-core, the same engine powering browser accessibility DevTools, to automatically test against 50+ WCAG rules.

### WCAG 2.2 Compliance
Tests against the latest WCAG 2.2 standards including new success criteria:
- Focus Not Obscured
- Dragging Movements  
- Target Size (Minimum)
- Consistent Help
- Redundant Entry
- Accessible Authentication

### Actionable Reports
Every violation includes:
- Description of the problem
- Impact on users
- Specific affected elements
- Step-by-step remediation guide
- Links to detailed documentation

### Batch Processing
Audit multiple pages simultaneously to assess site-wide accessibility.

## Understanding Results

### Violation Severity

- **Critical**: Serious barriers that prevent access (e.g., missing form labels, keyboard traps)
- **Serious**: Significant issues affecting usability (e.g., insufficient contrast, missing landmarks)
- **Moderate**: Noticeable problems that should be fixed (e.g., missing page language, empty links)
- **Minor**: Small improvements to enhance experience (e.g., suboptimal ARIA usage)

### Accessibility Score

The skill calculates a percentage score based on:
```
Score = (Passed Rules / Total Applicable Rules) × 100
```

A score of 100% means all automated checks passed. However, remember that automated testing covers only ~57% of WCAG requirements.

## Limitations

Automated testing catches many issues but cannot test everything. You should also:
- Manually test keyboard navigation
- Use screen readers (NVDA, JAWS, VoiceOver)
- Verify color contrast on images
- Check video captions and transcripts
- Test with real users who have disabilities

## Common Use Cases

### Pre-Launch Checks
Scan staging sites before going live to catch accessibility issues early.

### Compliance Documentation
Generate reports for legal/compliance requirements (ADA, Section 508, etc.).

### Progressive Enhancement
Track improvements over time by comparing audit results.

### Developer Training
Use reports to educate teams on accessibility best practices.

### Client Deliverables
Include professional accessibility reports in project deliverables.

## WCAG 2.2 Standards

The skill tests compliance with Web Content Accessibility Guidelines (WCAG) 2.2, organized around four principles:

1. **Perceivable**: Information must be presentable in ways users can perceive
2. **Operable**: UI components and navigation must be operable
3. **Understandable**: Information and UI operation must be understandable
4. **Robust**: Content must work with current and future technologies

## Support & Resources

- **WCAG 2.2 Quick Reference**: https://www.w3.org/WAI/WCAG22/quickref/
- **axe-core Rules**: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- **WebAIM**: https://webaim.org/
- **A11y Project**: https://www.a11yproject.com/

## Troubleshooting

If you encounter issues:
1. Ensure Chrome/Chromium is installed
2. Verify Selenium is installed: `pip list | grep selenium`
3. Check that the target website is accessible (not behind login)
4. Ask Claude for help - the skill includes detailed troubleshooting guidance

## License

Apache 2.0

## About

This skill integrates axe-core, developed by Deque Systems, the gold standard in automated accessibility testing. axe-core powers accessibility tools across the industry including browser extensions, CI/CD integrations, and testing frameworks.

By combining automated testing with Claude's ability to explain and contextualize issues, this skill makes accessibility testing more approachable and actionable for everyone.
