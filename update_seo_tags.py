#!/usr/bin/env python3
"""
Update meta descriptions and titles for better SEO
Optimizes for:
- Titles: 50-60 characters
- Descriptions: 150-160 characters
- Compelling, keyword-rich copy
"""

import os
import re
from pathlib import Path

# Define optimized titles and descriptions
SEO_UPDATES = {
    # Homepage
    "index.html": {
        "title": "Kutch Travel Guide | White Rann, Bhuj & Hidden Gems",
        "description": "Explore Kutch's White Rann, historic Bhuj, pristine beaches & vibrant crafts. Complete travel guide with itineraries, tips & local insights."
    },
    
    # Destinations
    "destinations/bhuj": {
        "title": "Bhuj Travel Guide | Palaces, Museums & Handicrafts",
        "description": "Discover Bhuj's royal palaces, ancient museums & artisan villages. Complete 2-day itinerary, shopping tips & local food recommendations."
    },
    "destinations/dhordo-white-rann": {
        "title": "White Rann of Kutch | Rann Utsav 2025 Complete Guide",
        "description": "Experience the White Desert's magic! Rann Utsav dates, Tent City booking, full moon nights & photography tips. Your complete travel guide."
    },
    "destinations/mandvi": {
        "title": "Mandvi Beach & Vijay Vilas Palace | Kutch Coast Guide",
        "description": "Explore Mandvi's pristine beach, majestic Vijay Vilas Palace & historic shipbuilding. Best time to visit, hotels & local attractions."
    },
    "destinations/kalo-dungar": {
        "title": "Kalo Dungar | Black Hill Kutch Viewpoint & Temple",
        "description": "Visit Kutch's highest point! Panoramic White Rann views, Dattatreya temple & magnetic hill phenomenon. Sunset timings & travel tips."
    },
    "destinations/lakhpat": {
        "title": "Lakhpat Fort | Ghost Town & Heritage Site in Kutch",
        "description": "Explore the abandoned port city of Lakhpat. Historic fort, Gurudwara, beach & fascinating history. Off-the-beaten-path Kutch destination."
    },
    "destinations/dholavira": {
        "title": "Dholavira | UNESCO Harappan Site & Ancient Kutch",
        "description": "Discover India's largest Harappan excavation! 5000-year-old civilization, water management marvels & archaeological wonders in Kutch."
    },
    "destinations/narayan-sarovar-koteshwar": {
        "title": "Narayan Sarovar & Koteshwar Temple | Sacred Kutch",
        "description": "Visit one of Hinduism's 5 sacred lakes. Koteshwar Mahadev temple, pilgrimage significance & serene desert landscapes near Pakistan border."
    },
    "destinations/mata-na-madh": {
        "title": "Mata na Madh | Ashapura Mata Temple Kutch Pilgrimage",
        "description": "Experience Kutch's most revered temple. Ashapura Mata darshan, festival dates, accommodation & spiritual significance for devotees."
    },
    
    # Crafts
    "crafts/ajrakh": {
        "title": "Ajrakh Block Printing | Traditional Kutch Textile Art",
        "description": "Discover Ajrakh's 4000-year heritage! Block printing process, Ajrakhpur village visit, authentic sarees & where to buy genuine pieces."
    },
    "crafts/bandhani": {
        "title": "Bandhani Tie-Dye | Kutch Traditional Textile Craft",
        "description": "Explore Kutch's vibrant Bandhani art! Tie-dye techniques, patterns, best shopping locations & how to identify authentic handmade pieces."
    },
    "crafts/rogan-art": {
        "title": "Rogan Art | Rare Kutch Fabric Painting Technique",
        "description": "Witness the dying art of Rogan painting! Only 2 families preserve this craft. Technique, history & where to meet master artisans."
    },
    "crafts/weaving": {
        "title": "Kutch Weaving | Handloom Textiles & Artisan Villages",
        "description": "Explore Bhujodi's master weavers! Handloom shawls, traditional patterns, Hiralaxmi Craft Park & buying directly from national awardees."
    },
    "crafts/pottery": {
        "title": "Kutch Pottery | Traditional Ceramics & Clay Craft",
        "description": "Discover Kutch's pottery villages! Traditional techniques, unique designs, artisan workshops & authentic handmade ceramic souvenirs."
    },
    "crafts/mirror-work": {
        "title": "Kutch Mirror Work | Traditional Embroidery & Textiles",
        "description": "Explore intricate mirror embroidery! Kutchi technique, patterns, best villages to visit & authentic mirror work textiles to buy."
    },
    
    # Blog posts
    "blog/rann-utsav-2025-guide": {
        "title": "Rann Utsav 2025 Complete Guide | Dates, Booking & Tips",
        "description": "Everything about Rann Utsav 2025! Festival dates, Tent City booking, cultural programs, adventure activities & complete travel planning guide."
    },
    "blog/white-rann-full-moon-guide": {
        "title": "White Rann Full Moon Guide | Best Nights & Photography",
        "description": "Experience White Rann under full moon! Best dates, photography tips, moonlight festival, permits & magical night desert experience."
    },
    "blog/kutchi-cuisine-food-guide": {
        "title": "Kutchi Cuisine Guide | Traditional Food & Must-Try Dishes",
        "description": "Savor authentic Kutchi flavors! Dabeli, Pakwan, Puri Sak & traditional thalis. Best restaurants, street food spots & local specialties."
    },
    "blog/photography-guide-kutch": {
        "title": "Kutch Photography Guide | Best Spots, Times & Tips",
        "description": "Capture Kutch's magic! White Rann photography, golden hour spots, cultural portraits & essential camera gear. Pro tips for stunning shots."
    },
    "blog/hidden-gems-kutch": {
        "title": "Hidden Gems of Kutch | Offbeat Destinations & Secrets",
        "description": "Discover unexplored Kutch! Secret beaches, forgotten temples, artisan villages & off-the-beaten-path adventures beyond tourist trails."
    },
    
    # Utility pages
    "about": {
        "title": "About Kutch Travel | Your Local Guide to Authentic Kutch",
        "description": "Learn about our mission to showcase authentic Kutch. Local insights, cultural preservation & sustainable tourism for meaningful travel experiences."
    },
    "bookings": {
        "title": "Book Kutch Tours | Rann Utsav, Hotels & Tour Packages",
        "description": "Book your Kutch adventure! Rann Utsav packages, hotel reservations, guided tours & customized itineraries. Best prices & local expertise."
    },
    "plan": {
        "title": "Plan Your Kutch Trip | Itineraries, Budget & Travel Tips",
        "description": "Plan the perfect Kutch journey! Sample itineraries, budget guides, best time to visit, packing tips & essential travel information."
    },
    "culture": {
        "title": "Kutch Culture | Traditions, Festivals & Heritage Guide",
        "description": "Immerse in Kutch's rich culture! Traditional customs, vibrant festivals, folk music, dance forms & living heritage of Gujarat's pride."
    },
    "food": {
        "title": "Kutch Food Guide | Traditional Cuisine & Best Restaurants",
        "description": "Taste authentic Kutch! Traditional dishes, best restaurants, street food, Gujarati thalis & culinary experiences you can't miss."
    },
    "history": {
        "title": "Kutch History | Ancient Civilization to Modern Times",
        "description": "Journey through Kutch's fascinating past! Harappan roots, royal dynasties, 2001 earthquake resilience & cultural evolution over millennia."
    },
    "geography": {
        "title": "Kutch Geography | Landscape, Climate & Natural Wonders",
        "description": "Understand Kutch's unique geography! Salt desert formation, seasonal wetlands, climate patterns & ecological significance of the region."
    },
}

def update_seo_tags(html_content, new_title, new_description):
    """
    Update title and description tags in HTML content
    """
    # Update title
    title_pattern = r'<title>[^<]*</title>'
    new_title_tag = f'<title>{new_title}</title>'
    updated_content = re.sub(title_pattern, new_title_tag, html_content, flags=re.DOTALL)
    
    # Update description
    desc_pattern = r'<meta name="description" content="[^"]*"'
    new_desc_tag = f'<meta name="description" content="{new_description}"'
    updated_content = re.sub(desc_pattern, new_desc_tag, updated_content, flags=re.DOTALL)
    
    return updated_content

def get_seo_for_path(file_path):
    """
    Determine appropriate SEO tags based on file path
    """
    path_str = str(file_path).replace('\\', '/')
    
    # Check for exact matches
    for pattern, seo_data in SEO_UPDATES.items():
        if pattern in path_str:
            return seo_data
    
    return None

def process_html_files(root_dir, dry_run=True):
    """
    Process all HTML files and update SEO tags
    """
    root_path = Path(root_dir)
    html_files = list(root_path.rglob("*.html"))
    
    stats = {
        "total": 0,
        "updated": 0,
        "skipped": 0,
        "errors": 0
    }
    
    print(f"{'DRY RUN - ' if dry_run else ''}Processing {len(html_files)} HTML files...\n")
    
    for html_file in html_files:
        stats["total"] += 1
        
        try:
            # Get SEO data for this file
            seo_data = get_seo_for_path(html_file.relative_to(root_path))
            
            if not seo_data:
                stats["skipped"] += 1
                continue
            
            # Read file
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update content
            updated_content = update_seo_tags(
                content,
                seo_data["title"],
                seo_data["description"]
            )
            
            # Write back if not dry run
            if not dry_run:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            
            stats["updated"] += 1
            
            # Print progress
            relative_path = html_file.relative_to(root_path)
            print(f"[UPDATED] {relative_path}")
            if dry_run:
                print(f"  Title: {seo_data['title']}")
                print(f"  Desc:  {seo_data['description'][:80]}...")
            
        except Exception as e:
            stats["errors"] += 1
            print(f"[ERROR] {html_file}: {str(e)}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Summary {'(DRY RUN)' if dry_run else ''}")
    print(f"{'='*60}")
    print(f"Total files processed: {stats['total']}")
    print(f"Updated: {stats['updated']}")
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
        print(f"  python update_seo_tags.py {target_dir} --execute")
