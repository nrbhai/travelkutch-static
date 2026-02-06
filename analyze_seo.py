#!/usr/bin/env python3
"""
Analyze current meta descriptions and titles
"""

import re
from pathlib import Path

def analyze_seo_tags(html_file):
    """Extract title and description from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1) if title_match else "NO TITLE"
        
        # Extract description
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
        description = desc_match.group(1) if desc_match else "NO DESCRIPTION"
        
        return title, description
    except Exception as e:
        return f"ERROR: {e}", ""

# Sample key pages
sample_pages = [
    "index.html",
    "destinations/bhuj/index.html",
    "destinations/dhordo-white-rann/index.html",
    "destinations/mandvi/index.html",
    "crafts/ajrakh/index.html",
    "crafts/bandhani/index.html",
    "blog/rann-utsav-2025-guide/index.html",
    "about/index.html",
    "bookings/index.html"
]

print("="*80)
print("CURRENT SEO TAGS ANALYSIS")
print("="*80)

for page in sample_pages:
    if Path(page).exists():
        title, desc = analyze_seo_tags(page)
        print(f"\n📄 {page}")
        print(f"   Title: {title}")
        print(f"   Desc:  {desc[:100]}{'...' if len(desc) > 100 else ''}")
        print(f"   Title Length: {len(title)} chars")
        print(f"   Desc Length:  {len(desc)} chars")
        
        # Check for issues
        issues = []
        if len(title) > 60:
            issues.append("⚠️  Title too long (>60 chars)")
        if len(title) < 30:
            issues.append("⚠️  Title too short (<30 chars)")
        if len(desc) > 160:
            issues.append("⚠️  Description too long (>160 chars)")
        if len(desc) < 120:
            issues.append("⚠️  Description too short (<120 chars)")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")

print("\n" + "="*80)
print("RECOMMENDATIONS:")
print("="*80)
print("• Titles: 50-60 characters (optimal for Google)")
print("• Descriptions: 150-160 characters (optimal for snippets)")
print("• Include primary keywords in both")
print("• Make descriptions compelling to improve click-through rate")
