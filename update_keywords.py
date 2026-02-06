#!/usr/bin/env python3
"""
SEO Keywords Update Script
Updates meta keywords tags in HTML files with page-specific keywords
"""

import os
import re
from pathlib import Path

# Define keyword mappings for different page types
KEYWORD_MAPPINGS = {
    # Homepage
    "index.html": "Kutch travel guide,White Rann of Kutch,Rann Utsav 2025,Bhuj tourism,Mandvi beaches,Gujarat travel,Rann Festival,Kutch destinations,Great Rann of Kutch,Kutch culture,India travel guide,Kutch handicrafts,Kutch photography,Gujarat tourism,Kutch hidden gems,Kutch tour packages,Things to do in Kutch",
    
    # Destinations
    "destinations/bhuj": "Bhuj tourism,Bhuj city guide,Aina Mahal Bhuj,Prag Mahal,Bhuj museums,Bhuj palaces,Bhuj shopping,Bhujodi village,Bhuj hotels,how to reach Bhuj,Bhuj sightseeing,Bhuj heritage,Kutch capital,Bhuj attractions",
    "destinations/dhordo-white-rann": "White Rann of Kutch,Dhordo,Rann Utsav,Great Rann of Kutch,White Desert India,Rann Utsav 2025,Tent City Dhordo,White Rann full moon,Rann permit,Kalo Dungar,Road to Heaven,White Rann photography,Dhordo camping",
    "destinations/mandvi": "Mandvi beach,Vijay Vilas Palace,Mandvi tourism,Mandvi shipbuilding,Mandvi hotels,Mandvi beach resort,Kutch beaches,Mandvi sightseeing,Mandvi wind farm,Mandvi port,Mandvi palace,Mandvi Gujarat",
    "destinations/kalo-dungar": "Kalo Dungar,Black Hill Kutch,highest point Kutch,Kalo Dungar viewpoint,Dattatreya temple,magnetic hill Kutch,Kalo Dungar sunset,Kutch viewpoints,Black Hill Gujarat",
    "destinations/lakhpat": "Lakhpat fort,Lakhpat ghost town,Lakhpat Gujarat,Lakhpat beach,Lakhpat tourism,Kutch heritage sites,Lakhpat history,Gurudwara Lakhpat,abandoned city Kutch",
    "destinations/dholavira": "Dholavira,Harappan site,Indus Valley Civilization,Dholavira excavation,ancient Kutch,Dholavira UNESCO,archaeological site Gujarat,Dholavira tourism,Harappan city",
    "destinations/narayan-sarovar-koteshwar": "Narayan Sarovar,Koteshwar temple,sacred lake Kutch,Narayan Sarovar pilgrimage,Koteshwar Mahadev,religious sites Kutch,Narayan Sarovar Gujarat,holy places Kutch",
    "destinations/mata-na-madh": "Mata na Madh,Ashapura Mata temple,Kutch temples,Mata na Madh pilgrimage,Ashapura temple Gujarat,religious tourism Kutch,Mata na Madh Gujarat",
    "destinations/anjar": "Anjar Gujarat,Anjar town,Anjar Kutch,Anjar tourism,Anjar sightseeing,Kutch towns,Anjar attractions",
    "destinations/gandhidham": "Gandhidham,Gandhidham city,Gandhidham tourism,Gandhidham Gujarat,Kutch cities,Gandhidham attractions,Gandhidham shopping",
    "destinations/mundra": "Mundra port,Mundra Gujarat,Mundra tourism,Mundra beach,Adani port Mundra,Mundra Kutch,Mundra attractions",
    "destinations/road-to-heaven": "Road to Heaven Kutch,scenic drives Kutch,Road to Heaven Gujarat,Kutch photography spots,best roads Kutch,Kutch landscapes",
    
    # Crafts
    "crafts/ajrakh": "Ajrakh block printing,Ajrakh fabric,Ajrakhpur,Kutch handicrafts,Ajrakh art,traditional block printing,Ajrakh sarees,Ajrakh patterns,Kutch textiles,Ajrakh workshop,Ajrakh printing technique",
    "crafts/bandhani": "Bandhani tie dye,Kutch bandhani,Bandhani sarees,tie and dye Kutch,Bandhani patterns,traditional bandhani,Bandhani fabric,Kutch textiles,Bandhani art,Bandhani technique",
    "crafts/rogan-art": "Rogan art,Rogan painting,Kutch Rogan art,traditional Rogan,Rogan fabric painting,Kutch handicrafts,Rogan technique,Rogan artists Kutch",
    "crafts/weaving": "Kutch weaving,handloom Kutch,traditional weaving,Kutch textiles,handwoven fabrics,Kutch weavers,weaving villages Kutch,Kutch handloom",
    "crafts/pottery": "Kutch pottery,traditional pottery,Kutch ceramics,pottery villages Kutch,handmade pottery,Kutch artisans,pottery craft Kutch",
    "crafts/mirror-work": "mirror work Kutch,Kutch embroidery,mirror embroidery,traditional mirror work,Kutch handicrafts,mirror work textiles,Kutch mirror craft",
    "crafts/leather-craft": "Kutch leather craft,leather work Kutch,traditional leather,Kutch artisans,leather products Kutch,handmade leather Kutch",
    "crafts/sudi-chappu": "Sudi Chappu,Kutch footwear,traditional footwear,handmade shoes Kutch,Kutch leather footwear,traditional Kutch shoes",
    
    # Blog posts
    "blog/rann-utsav-2025-guide": "Rann Utsav 2025,Rann Utsav guide,Rann Festival,Tent City booking,Rann Utsav dates,Rann Utsav packages,Rann Utsav activities,White Rann festival,Kutch festival,Rann Utsav travel guide",
    "blog/white-rann-full-moon-guide": "White Rann full moon,full moon Kutch,White Rann night,moonlight Rann,White Rann photography,full moon festival,Rann full moon guide,White Desert full moon",
    "blog/kutchi-cuisine-food-guide": "Kutchi cuisine,Kutch food,traditional Kutchi food,Kutch recipes,Gujarati food Kutch,Kutch dishes,Kutchi thali,food guide Kutch,Kutch culinary,traditional cuisine Gujarat",
    "blog/photography-guide-kutch": "Kutch photography,photography guide Kutch,White Rann photography,Kutch landscapes,photography tips Kutch,best photo spots Kutch,Kutch photo tour",
    "blog/hidden-gems-kutch": "hidden gems Kutch,offbeat Kutch,unexplored Kutch,secret places Kutch,hidden destinations Kutch,offbeat travel Gujarat,lesser known Kutch",
    "blog/ancient-crafts-kutch-heritage": "Kutch crafts,traditional crafts Kutch,Kutch heritage,handicrafts Kutch,artisan villages Kutch,Kutch craft heritage,traditional arts Kutch",
    
    # Utility pages
    "about": "about Kutch travel,Kutch travel guide,travel information Kutch,Kutch tourism info,about us,Kutch travel planning",
    "bookings": "Kutch bookings,book Kutch tour,Rann Utsav booking,Kutch hotels booking,tour packages Kutch,Kutch travel booking,reserve Kutch tour",
    "plan": "plan Kutch trip,Kutch itinerary,Kutch travel planning,trip planner Kutch,Kutch tour planning,plan your visit Kutch,Kutch travel tips",
    "culture": "Kutch culture,Kutchi traditions,Kutch heritage,cultural tourism Kutch,Kutch festivals,traditional culture Gujarat,Kutch customs",
    "festivals": "Kutch festivals,Rann Utsav,festivals Gujarat,cultural festivals Kutch,Kutch celebrations,traditional festivals,Kutch events",
    "food": "Kutch food,Kutchi cuisine,food Kutch,traditional food Gujarat,Kutch restaurants,Kutchi dishes,food guide Kutch",
    "history": "Kutch history,historical Kutch,Kutch heritage,history Gujarat,ancient Kutch,Kutch civilization,historical sites Kutch",
    "geography": "Kutch geography,Kutch landscape,geography Gujarat,Kutch terrain,Kutch region,physical geography Kutch",
}

def get_keywords_for_path(file_path):
    """
    Determine appropriate keywords based on file path
    """
    path_str = str(file_path).replace('\\', '/')
    
    # Check for exact matches first
    for pattern, keywords in KEYWORD_MAPPINGS.items():
        if pattern in path_str:
            return keywords
    
    # Default keywords for unmatched pages
    return "Kutch travel guide,Gujarat tourism,Kutch destinations,Kutch attractions,travel Gujarat,Kutch tourism,visit Kutch,Kutch India"

def update_meta_keywords(html_content, new_keywords):
    """
    Update or add meta keywords tag in HTML content
    """
    # Pattern to match existing meta keywords tag (with DOTALL for minified HTML)
    pattern = r'<meta\s+name="keywords"\s+content="[^"]*"\s*/?>'
    
    # New meta keywords tag
    new_tag = f'<meta name="keywords" content="{new_keywords}"/>'
    
    # Check if meta keywords exists (use re.DOTALL to handle minified HTML)
    if re.search(pattern, html_content, re.DOTALL):
        # Replace existing tag
        updated_content = re.sub(pattern, new_tag, html_content, flags=re.DOTALL)
        return updated_content, "updated"
    else:
        # Try to add after description meta tag
        desc_pattern = r'(<meta\s+name="description"\s+content="[^"]*"\s*/>)'
        if re.search(desc_pattern, html_content, re.DOTALL):
            updated_content = re.sub(desc_pattern, r'\1' + new_tag, html_content, flags=re.DOTALL)
            return updated_content, "added"
    
    return html_content, "skipped"

def process_html_files(root_dir, dry_run=True):
    """
    Process all HTML files in the directory
    """
    root_path = Path(root_dir)
    html_files = list(root_path.rglob("*.html"))
    
    stats = {
        "total": 0,
        "updated": 0,
        "added": 0,
        "skipped": 0,
        "errors": 0
    }
    
    print(f"{'DRY RUN - ' if dry_run else ''}Processing {len(html_files)} HTML files...\n")
    
    for html_file in html_files:
        stats["total"] += 1
        
        try:
            # Read file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get appropriate keywords
            keywords = get_keywords_for_path(html_file.relative_to(root_path))
            
            # Update content
            updated_content, action = update_meta_keywords(content, keywords)
            
            # Track stats
            stats[action] += 1
            
            # Write back if not dry run
            if not dry_run and action in ["updated", "added"]:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            # Print progress
            relative_path = html_file.relative_to(root_path)
            print(f"[{action.upper()}] {relative_path}")
            if dry_run:
                print(f"  Keywords: {keywords[:100]}...")
            
        except Exception as e:
            stats["errors"] += 1
            print(f"[ERROR] {html_file}: {str(e)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary {'(DRY RUN)' if dry_run else ''}")
    print(f"{'='*60}")
    print(f"Total files processed: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Added: {stats['added']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Errors: {stats['errors']}")
    
    return stats

if __name__ == "__main__":
    import sys
    
    # Get directory from command line or use current directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Check if --execute flag is provided
    dry_run = "--execute" not in sys.argv
    
    if dry_run:
        print("="*60)
        print("DRY RUN MODE - No files will be modified")
        print("Run with --execute flag to apply changes")
        print("="*60)
        print()
    
    # Process files
    process_html_files(target_dir, dry_run=dry_run)
    
    if dry_run:
        print("\nTo apply these changes, run:")
        print(f"  python update_keywords.py {target_dir} --execute")
