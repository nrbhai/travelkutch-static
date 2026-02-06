import re

# Test Bhuj page
with open('destinations/bhuj/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find keywords tag
match = re.search(r'<meta name="keywords" content="([^"]+)"', content)
if match:
    keywords = match.group(1)
    print(f"Bhuj keywords found:")
    print(f"  {keywords[:200]}...")
    
    # Check if it contains Bhuj-specific keywords
    if "Bhuj tourism" in keywords:
        print("  ✓ Contains Bhuj-specific keywords!")
    else:
        print("  ✗ Still has generic keywords")
else:
    print("No keywords tag found!")
