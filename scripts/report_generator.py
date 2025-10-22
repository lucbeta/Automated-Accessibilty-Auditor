#!/usr/bin/env python3
"""
Accessibility Report Generator
Converts audit JSON results into human-readable reports (HTML, Markdown, PDF)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import argparse


class ReportGenerator:
    """Generate accessibility audit reports in various formats"""
    
    # Impact severity colors
    IMPACT_COLORS = {
        "critical": "#d32f2f",
        "serious": "#f57c00",
        "moderate": "#fbc02d",
        "minor": "#7cb342"
    }
    
    # WCAG principle descriptions
    PRINCIPLES = {
        "perceivable": "Information and user interface components must be presentable to users in ways they can perceive.",
        "operable": "User interface components and navigation must be operable.",
        "understandable": "Information and the operation of user interface must be understandable.",
        "robust": "Content must be robust enough that it can be interpreted by a wide variety of user agents, including assistive technologies."
    }
    
    def __init__(self, audit_data: Dict):
        """Initialize with audit data"""
        if isinstance(audit_data, str):
            with open(audit_data, 'r') as f:
                audit_data = json.load(f)
        self.data = audit_data
    
    def _format_violation(self, violation: Dict, format_type: str = "markdown") -> str:
        """Format a single violation"""
        if format_type == "markdown":
            return self._format_violation_markdown(violation)
        elif format_type == "html":
            return self._format_violation_html(violation)
        return ""
    
    def _format_violation_markdown(self, violation: Dict) -> str:
        """Format violation as Markdown"""
        impact = violation.get("impact", "unknown").upper()
        nodes_count = len(violation.get("nodes", []))
        
        md = f"### {violation['description']}\n\n"
        md += f"**Impact:** {impact} | "
        md += f"**Instances:** {nodes_count} | "
        md += f"**WCAG:** {', '.join(violation.get('tags', []))}\n\n"
        md += f"**Help:** {violation['help']}\n\n"
        md += f"**How to fix:**\n{violation.get('helpUrl', 'No URL available')}\n\n"
        
        if nodes_count > 0:
            md += f"**Affected elements ({nodes_count}):**\n\n"
            for i, node in enumerate(violation['nodes'][:5], 1):  # Show first 5
                target = node.get('target', ['unknown'])[0]
                html = node.get('html', 'N/A')
                md += f"{i}. `{target}`\n"
                md += f"   ```html\n   {html[:200]}{'...' if len(html) > 200 else ''}\n   ```\n"
            
            if nodes_count > 5:
                md += f"\n*... and {nodes_count - 5} more instances*\n"
        
        md += "\n---\n\n"
        return md
    
    def _format_violation_html(self, violation: Dict) -> str:
        """Format violation as HTML"""
        impact = violation.get("impact", "unknown")
        impact_color = self.IMPACT_COLORS.get(impact, "#999")
        nodes_count = len(violation.get("nodes", []))
        
        html = f"""
        <div class="violation" data-impact="{impact}">
            <div class="violation-header">
                <h3>{violation['description']}</h3>
                <span class="impact-badge" style="background-color: {impact_color};">{impact.upper()}</span>
            </div>
            <div class="violation-meta">
                <span>Instances: {nodes_count}</span>
                <span>WCAG: {', '.join(violation.get('tags', []))}</span>
            </div>
            <p><strong>Help:</strong> {violation['help']}</p>
            <p><strong>Learn more:</strong> <a href="{violation.get('helpUrl', '#')}" target="_blank">Fix this issue</a></p>
        """
        
        if nodes_count > 0:
            html += f'<details><summary>Show affected elements ({nodes_count})</summary><div class="nodes">'
            for node in violation['nodes'][:5]:
                target = node.get('target', ['unknown'])[0]
                html_snippet = node.get('html', 'N/A')
                html += f"""
                <div class="node">
                    <code class="target">{target}</code>
                    <pre><code>{html_snippet[:200]}{'...' if len(html_snippet) > 200 else ''}</code></pre>
                </div>
                """
            if nodes_count > 5:
                html += f'<p><em>... and {nodes_count - 5} more instances</em></p>'
            html += '</div></details>'
        
        html += '</div>'
        return html
    
    def generate_markdown(self, output_file: str = None) -> str:
        """Generate Markdown report"""
        md = f"# Accessibility Audit Report\n\n"
        md += f"**URL:** {self.data['url']}\n"
        md += f"**Date:** {self.data['timestamp']}\n"
        md += f"**Standard:** {self.data['conformance_level']}\n\n"
        
        # Summary
        summary = self.data['summary']
        md += f"## Summary\n\n"
        md += f"- **Violations:** {summary['violations']}\n"
        md += f"- **Passes:** {summary['passes']}\n"
        md += f"- **Incomplete:** {summary['incomplete']}\n"
        md += f"- **Inapplicable:** {summary['inapplicable']}\n\n"
        
        # Score calculation
        total_checks = summary['violations'] + summary['passes']
        if total_checks > 0:
            score = (summary['passes'] / total_checks) * 100
            md += f"**Accessibility Score:** {score:.1f}%\n\n"
        
        # Violations by impact
        violations = self.data.get('violations', [])
        if violations:
            by_impact = {}
            for v in violations:
                impact = v.get('impact', 'unknown')
                by_impact.setdefault(impact, []).append(v)
            
            md += f"## Violations by Impact\n\n"
            for impact in ['critical', 'serious', 'moderate', 'minor']:
                if impact in by_impact:
                    md += f"### {impact.capitalize()}: {len(by_impact[impact])}\n\n"
            md += "\n"
            
            # Detailed violations
            md += f"## Detailed Violations ({len(violations)})\n\n"
            for violation in violations:
                md += self._format_violation_markdown(violation)
        else:
            md += "## 🎉 No Violations Found!\n\nThis page passes all WCAG 2.2 checks at the specified conformance level.\n"
        
        # Incomplete tests
        incomplete = self.data.get('incomplete', [])
        if incomplete:
            md += f"## Items Needing Review ({len(incomplete)})\n\n"
            md += "These items require manual review:\n\n"
            for item in incomplete:
                md += f"- **{item['description']}** ({len(item.get('nodes', []))} instances)\n"
        
        if output_file:
            Path(output_file).write_text(md)
            print(f"Markdown report saved to: {output_file}")
        
        return md
    
    def generate_html(self, output_file: str = None) -> str:
        """Generate HTML report"""
        violations = self.data.get('violations', [])
        summary = self.data['summary']
        
        # Calculate score
        total_checks = summary['violations'] + summary['passes']
        score = (summary['passes'] / total_checks) * 100 if total_checks > 0 else 0
        
        # Group by impact
        by_impact = {}
        for v in violations:
            impact = v.get('impact', 'unknown')
            by_impact.setdefault(impact, []).append(v)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Audit Report - {self.data['url']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #1a73e8; margin-bottom: 10px; }}
        .meta {{ color: #666; font-size: 14px; }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{ font-size: 14px; color: #666; margin-bottom: 5px; }}
        .summary-card .number {{ font-size: 32px; font-weight: bold; }}
        .violations-count {{ color: #d32f2f; }}
        .passes-count {{ color: #388e3c; }}
        .score {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .score .number {{ font-size: 48px; font-weight: bold; }}
        .violation {{
            background: white;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #999;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .violation[data-impact="critical"] {{ border-left-color: #d32f2f; }}
        .violation[data-impact="serious"] {{ border-left-color: #f57c00; }}
        .violation[data-impact="moderate"] {{ border-left-color: #fbc02d; }}
        .violation[data-impact="minor"] {{ border-left-color: #7cb342; }}
        .violation-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }}
        .violation-header h3 {{ flex: 1; margin-right: 10px; }}
        .impact-badge {{
            padding: 4px 12px;
            border-radius: 4px;
            color: white;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .violation-meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }}
        .violation-meta span {{ margin-right: 20px; }}
        details {{ margin-top: 15px; }}
        summary {{
            cursor: pointer;
            color: #1a73e8;
            font-weight: 500;
            padding: 5px 0;
        }}
        .nodes {{ margin-top: 10px; }}
        .node {{
            background: #f5f5f5;
            padding: 10px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .target {{
            display: block;
            color: #d32f2f;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        pre {{
            background: #263238;
            color: #aed581;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 12px;
        }}
        .no-violations {{
            background: white;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .no-violations h2 {{ color: #388e3c; font-size: 32px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Accessibility Audit Report</h1>
        <div class="meta">
            <p><strong>URL:</strong> {self.data['url']}</p>
            <p><strong>Date:</strong> {self.data['timestamp']}</p>
            <p><strong>Standard:</strong> {self.data['conformance_level']}</p>
        </div>
    </div>
    
    <div class="summary">
        <div class="summary-card">
            <h3>Violations</h3>
            <div class="number violations-count">{summary['violations']}</div>
        </div>
        <div class="summary-card">
            <h3>Passes</h3>
            <div class="number passes-count">{summary['passes']}</div>
        </div>
        <div class="summary-card">
            <h3>Incomplete</h3>
            <div class="number">{summary['incomplete']}</div>
        </div>
        <div class="summary-card">
            <h3>Inapplicable</h3>
            <div class="number">{summary['inapplicable']}</div>
        </div>
    </div>
    
    <div class="score">
        <div class="number">{score:.1f}%</div>
        <p>Accessibility Score</p>
    </div>
"""
        
        if violations:
            html += "<h2>Violations</h2>"
            for impact in ['critical', 'serious', 'moderate', 'minor']:
                if impact in by_impact:
                    html += f"<h3>{impact.capitalize()} ({len(by_impact[impact])})</h3>"
                    for violation in by_impact[impact]:
                        html += self._format_violation_html(violation)
        else:
            html += """
    <div class="no-violations">
        <h2>🎉 No Violations Found!</h2>
        <p>This page passes all WCAG 2.2 checks at the specified conformance level.</p>
    </div>
"""
        
        html += """
</body>
</html>
"""
        
        if output_file:
            Path(output_file).write_text(html)
            print(f"HTML report saved to: {output_file}")
        
        return html
    
    def generate_all(self, output_dir: str):
        """Generate all report formats"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate reports
        self.generate_markdown(output_path / "report.md")
        self.generate_html(output_path / "report.html")
        
        print(f"\nAll reports generated in: {output_dir}")
        print(f"  - Markdown: report.md")
        print(f"  - HTML: report.html")


def main():
    parser = argparse.ArgumentParser(
        description="Generate accessibility audit reports from JSON"
    )
    parser.add_argument("json_file", help="Input JSON file from audit")
    parser.add_argument(
        "--format", "-f",
        choices=["markdown", "html", "all"],
        default="all",
        help="Output format (default: all)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file or directory path"
    )
    
    args = parser.parse_args()
    
    generator = ReportGenerator(args.json_file)
    
    if args.format == "markdown":
        output = args.output or "report.md"
        generator.generate_markdown(output)
    elif args.format == "html":
        output = args.output or "report.html"
        generator.generate_html(output)
    else:  # all
        output = args.output or "reports"
        generator.generate_all(output)


if __name__ == "__main__":
    main()
