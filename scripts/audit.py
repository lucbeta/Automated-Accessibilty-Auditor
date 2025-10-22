#!/usr/bin/env python3
"""
Accessibility Audit Script
Performs comprehensive WCAG 2.2 accessibility audits using axe-core via Selenium
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException, WebDriverException
except ImportError:
    print("ERROR: Selenium not installed. Run: pip install selenium --break-system-packages")
    sys.exit(1)


class AccessibilityAuditor:
    """Performs accessibility audits on web pages using axe-core"""
    
    # axe-core CDN URL
    AXE_CORE_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.2/axe.min.js"
    
    # WCAG 2.2 conformance levels
    CONFORMANCE_LEVELS = {
        "A": ["wcag2a", "wcag21a", "wcag22a"],
        "AA": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"],
        "AAA": ["wcag2a", "wcag2aa", "wcag2aaa", "wcag21a", "wcag21aa", "wcag21aaa", "wcag22a", "wcag22aa", "wcag22aaa"]
    }
    
    def __init__(self, headless: bool = True):
        """Initialize the auditor with Chrome WebDriver"""
        self.driver = None
        self.headless = headless
        self._setup_driver()
        
    def _setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException as e:
            print(f"ERROR: Failed to initialize Chrome WebDriver: {e}")
            print("Make sure Chrome/Chromium is installed and chromedriver is available.")
            sys.exit(1)
    
    def _inject_axe(self):
        """Inject axe-core library into the page"""
        try:
            # Try to load axe from CDN
            self.driver.execute_script(f"""
                var script = document.createElement('script');
                script.src = '{self.AXE_CORE_URL}';
                document.head.appendChild(script);
            """)
            
            # Wait for axe to load
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return typeof axe !== 'undefined'")
            )
        except TimeoutException:
            print("ERROR: Failed to load axe-core library")
            raise
    
    def audit_url(self, url: str, conformance: str = "AA", output_file: Optional[str] = None) -> Dict:
        """
        Audit a URL for accessibility issues
        
        Args:
            url: The URL to audit
            conformance: WCAG conformance level (A, AA, or AAA)
            output_file: Optional path to save JSON results
            
        Returns:
            Dictionary containing audit results
        """
        print(f"Auditing: {url}")
        print(f"Conformance level: WCAG 2.2 Level {conformance}")
        
        try:
            # Load the page
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Inject axe-core
            self._inject_axe()
            
            # Configure axe to run with specified WCAG level
            tags = self.CONFORMANCE_LEVELS.get(conformance.upper(), self.CONFORMANCE_LEVELS["AA"])
            
            # Run axe analysis
            print("Running accessibility scan...")
            results = self.driver.execute_script(f"""
                return axe.run({{
                    runOnly: {{
                        type: 'tag',
                        values: {json.dumps(tags)}
                    }}
                }});
            """)
            
            # Add metadata
            audit_data = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "conformance_level": f"WCAG 2.2 Level {conformance.upper()}",
                "summary": {
                    "violations": len(results.get("violations", [])),
                    "passes": len(results.get("passes", [])),
                    "incomplete": len(results.get("incomplete", [])),
                    "inapplicable": len(results.get("inapplicable", []))
                },
                "violations": results.get("violations", []),
                "passes": results.get("passes", []),
                "incomplete": results.get("incomplete", []),
                "inapplicable": results.get("inapplicable", [])
            }
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w') as f:
                    json.dump(audit_data, f, indent=2)
                print(f"Results saved to: {output_path}")
            
            return audit_data
            
        except Exception as e:
            print(f"ERROR during audit: {e}")
            raise
    
    def audit_multiple_urls(self, urls: List[str], conformance: str = "AA", 
                           output_dir: Optional[str] = None) -> List[Dict]:
        """
        Audit multiple URLs
        
        Args:
            urls: List of URLs to audit
            conformance: WCAG conformance level (A, AA, or AAA)
            output_dir: Optional directory to save individual JSON results
            
        Returns:
            List of audit results for each URL
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*60}")
            print(f"Auditing {i}/{len(urls)}")
            print(f"{'='*60}\n")
            
            output_file = None
            if output_dir:
                # Create safe filename from URL
                filename = url.replace("https://", "").replace("http://", "")
                filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
                output_file = Path(output_dir) / f"{filename}.json"
            
            try:
                result = self.audit_url(url, conformance, output_file)
                results.append(result)
            except Exception as e:
                print(f"Failed to audit {url}: {e}")
                results.append({
                    "url": url,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        return results
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    parser = argparse.ArgumentParser(
        description="Perform WCAG 2.2 accessibility audits on websites using axe-core"
    )
    parser.add_argument("url", nargs="+", help="URL(s) to audit")
    parser.add_argument(
        "--conformance", "-c",
        choices=["A", "AA", "AAA"],
        default="AA",
        help="WCAG conformance level (default: AA)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (for single URL) or directory (for multiple URLs)"
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Run browser in visible mode (not headless)"
    )
    
    args = parser.parse_args()
    
    with AccessibilityAuditor(headless=not args.visible) as auditor:
        if len(args.url) == 1:
            # Single URL audit
            result = auditor.audit_url(args.url[0], args.conformance, args.output)
            
            print(f"\n{'='*60}")
            print("AUDIT SUMMARY")
            print(f"{'='*60}")
            print(f"Violations: {result['summary']['violations']}")
            print(f"Passes: {result['summary']['passes']}")
            print(f"Incomplete: {result['summary']['incomplete']}")
            print(f"Inapplicable: {result['summary']['inapplicable']}")
            
        else:
            # Multiple URL audit
            results = auditor.audit_multiple_urls(
                args.url,
                args.conformance,
                args.output
            )
            
            print(f"\n{'='*60}")
            print("OVERALL SUMMARY")
            print(f"{'='*60}")
            for result in results:
                if "error" in result:
                    print(f"{result['url']}: ERROR - {result['error']}")
                else:
                    print(f"{result['url']}: {result['summary']['violations']} violations")


if __name__ == "__main__":
    main()
