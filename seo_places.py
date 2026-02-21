#!/usr/bin/env python3
"""
seo_places.py
-------------
Injects fully place-specific SEO into every /places/<slug>/index.html page:
  - <title>
  - meta description
  - meta keywords
  - canonical href
  - og:title, og:description, og:url, og:image
  - twitter:title
  - JSON-LD TouristAttraction structured data
"""

import os, re, json

ROOT   = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'https://travelkutch.org'

# ── Per-place SEO data ─────────────────────────────────────────────────────────
PLACES = {
    '72-jinalaya': {
        'name':        '72 Jinalaya',
        'title':       '72 Jinalaya Kutch | Ancient Jain Temple Complex',
        'description': 'Visit 72 Jinalaya, a magnificent Jain temple complex in Kutch with 72 shrines, intricate white marble carvings & deep spiritual significance. Best visited Oct–Mar.',
        'keywords':    '72 Jinalaya Kutch,Jain temple Kutch,Kutch Jain pilgrimage,72 jinalaya Gujarat,Jain marble temple Kutch,Kutch religious places,Bhuj Jain temple',
        'category':    'Hindu & Jain Temple',
        'region':      'Kutch, Gujarat',
        'lat':          23.2517,
        'lon':          69.6669,
    },
    'abjibapa-chhatardi': {
        'name':        'Abjibapa Chhatardi',
        'title':       'Abjibapa Chhatardi Bhuj | Royal Cenotaphs of Kutch',
        'description': 'Explore the ornate Abjibapa Chhatardi cenotaphs in Bhuj — stunning royal tombs featuring Portuguese-Mughal architecture, intricate jali-work & rich Kutchi craftsmanship.',
        'keywords':    'Abjibapa Chhatardi,Bhuj cenotaphs,Kutch royal tombs,Bhuj historical monuments,Kutch heritage architecture,Chhatardi Bhuj,Kutch travel places',
        'category':    'Heritage Monument',
        'region':      'Bhuj, Kutch, Gujarat',
        'lat':          23.2520,
        'lon':          69.6718,
    },
    'asar-mata': {
        'name':        'Asar Mata Temple',
        'title':       'Asar Mata Temple Kutch | Sacred Goddess Shrine',
        'description': 'Discover Asar Mata — a revered goddess temple in Kutch set amid peaceful desert landscapes. A cherished pilgrimage site for local devotees, best visited during Navratri.',
        'keywords':    'Asar Mata Kutch,Asar Mata temple,Kutch goddess temple,Kutch pilgrimage,Gujarat temples,Kutch religious tourism,Navratri Kutch',
        'category':    'Hindu Temple',
        'region':      'Kutch, Gujarat',
        'lat':          23.4200,
        'lon':          69.4500,
    },
    'dhrang-mekan-dada': {
        'name':        'Dhrang Mekan Dada',
        'title':       'Dhrang Mekan Dada Kutch | Spiritual Heritage Site',
        'description': 'Visit Dhrang Mekan Dada — a sacred dargah and heritage site in Kutch with rich spiritual history. An important pilgrimage destination drawing devotees from across Gujarat.',
        'keywords':    'Dhrang Mekan Dada,Dhrang Kutch,Kutch dargah,Kutch spiritual places,Mekan Dada Gujarat,Kutch pilgrimage sites,Gujarat heritage',
        'category':    'Dargah & Heritage Site',
        'region':      'Dhrang, Kutch, Gujarat',
        'lat':          23.5000,
        'lon':          69.7000,
    },
    'gangeshwar-mahadev': {
        'name':        'Gangeshwar Mahadev Temple',
        'title':       'Gangeshwar Mahadev Temple Kutch | Coastal Shiva Shrine',
        'description': 'Explore Gangeshwar Mahadev — a dramatic coastal Shiva temple where ancient lingas emerge from the sea. A unique blend of spirituality and natural beauty near Mandvi, Kutch.',
        'keywords':    'Gangeshwar Mahadev,Gangeshwar temple Kutch,Shiva temple Kutch,coastal temple Kutch,Mandvi temple,Kutch religious places,Shivling sea Kutch',
        'category':    'Hindu Temple',
        'region':      'Kutch, Gujarat',
        'lat':          22.8200,
        'lon':          69.7200,
    },
    'hanuman-tekri': {
        'name':        'Hanuman Tekri',
        'title':       'Hanuman Tekri Bhuj | Hilltop Temple & Panoramic Views',
        'description': 'Climb Hanuman Tekri in Bhuj for sweeping panoramic views of the city and desert. This beloved hilltop Hanuman temple offers serenity, cool breeze & stunning sunrise vistas.',
        'keywords':    'Hanuman Tekri Bhuj,Hanuman temple Bhuj,Bhuj hillside temple,Bhuj viewpoint,Kutch temples,Bhuj tourism,Gujarat Hanuman temple',
        'category':    'Hindu Temple & Viewpoint',
        'region':      'Bhuj, Kutch, Gujarat',
        'lat':          23.2550,
        'lon':          69.6670,
    },
    'jadura': {
        'name':        'Jadura',
        'title':       'Jadura Kutch | Rare Art Village & Heritage Craft Hub',
        'description': 'Visit Jadura — a unique Kutchi village famous for rare traditional embroidery crafts, authentic artisan communities & peaceful rural life far from tourist trails.',
        'keywords':    'Jadura Kutch,Jadura village Kutch,Kutch embroidery village,Kutch artisan village,Kutch craft tourism,Gujarat village tourism,Kutch off-beat',
        'category':    'Heritage Craft Village',
        'region':      'Kutch, Gujarat',
        'lat':          23.3000,
        'lon':          69.5000,
    },
    'kashi-vishwanath': {
        'name':        'Kashi Vishwanath Temple Bhuj',
        'title':       'Kashi Vishwanath Temple Bhuj | Shiva Pilgrimage Kutch',
        'description': 'Seek blessings at Kashi Vishwanath Temple in Bhuj — a revered Shiva shrine rebuilt after the 2001 earthquake, symbolising Kutch resilience and spiritual devotion.',
        'keywords':    'Kashi Vishwanath Bhuj,Shiva temple Bhuj,Kutch Shiva shrine,Bhuj temple,Kutch pilgrimage,Gujarat Shiva temple,Bhuj Hindu temple',
        'category':    'Hindu Temple',
        'region':      'Bhuj, Kutch, Gujarat',
        'lat':          23.2512,
        'lon':          69.6698,
    },
    'kotay-surya-mandir': {
        'name':        'Kotay Surya Mandir',
        'title':       'Kotay Surya Mandir Kutch | Rare Sun Temple Gujarat',
        'description': 'Discover Kotay Surya Mandir — one of Gujarat\'s rare Sun temples in Kutch, featuring ancient stone carvings and serene desert surroundings. A hidden gem for history lovers.',
        'keywords':    'Kotay Surya Mandir,Sun temple Kutch,Kutch ancient temple,Gujarat sun temple,Kutch historical temple,Suryamandir Kutch,Kutch hidden gems',
        'category':    'Ancient Hindu Temple',
        'region':      'Kutch, Gujarat',
        'lat':          23.3500,
        'lon':          69.5500,
    },
    'ravalpir': {
        'name':        'Ravalpir Dargah',
        'title':       'Ravalpir Kutch | Sacred Dargah & Annual Fair',
        'description': 'Visit Ravalpir — one of Kutch\'s most celebrated dargahs, hosting a vibrant annual urs (fair) that draws thousands of devotees from Hindu and Muslim communities alike.',
        'keywords':    'Ravalpir Kutch,Ravalpir dargah,Kutch urs fair,Kutch Sufi shrine,Ravalpir mela,Kutch communal harmony,Gujarat dargah tourism',
        'category':    'Sufi Dargah',
        'region':      'Kutch, Gujarat',
        'lat':          23.5200,
        'lon':          69.8000,
    },
    'rudramata-dam': {
        'name':        'Rudramata Dam',
        'title':       'Rudramata Dam Kutch | Scenic Reservoir & Nature Spot',
        'description': 'Explore Rudramata Dam — a picturesque reservoir in Kutch surrounded by rocky hills and seasonal greenery. A perfect picnic spot and photography destination near Bhuj.',
        'keywords':    'Rudramata Dam Kutch,Kutch reservoir,Bhuj dam,Kutch nature spots,Rudramata Bhuj,Kutch picnic places,Gujarat dam tourism',
        'category':    'Nature & Scenic Attraction',
        'region':      'Kutch, Gujarat',
        'lat':          23.4000,
        'lon':          69.6000,
    },
    'shyamji-krishnavarma': {
        'name':        'Shyamji Krishna Varma Memorial',
        'title':       'Shyamji Krishna Varma Memorial Mandvi | Freedom Fighter',
        'description': 'Pay homage at the Shyamji Krishna Varma Memorial in Mandvi — honouring the great Indian revolutionary who founded India House in London. A must-visit for history enthusiasts.',
        'keywords':    'Shyamji Krishna Varma,Shyamji memorial Mandvi,Mandvi Kutch,India House London founder,Kutch freedom fighter,Gujarat independence hero,Mandvi museum',
        'category':    'Heritage Memorial',
        'region':      'Mandvi, Kutch, Gujarat',
        'lat':          22.8300,
        'lon':          69.3500,
    },
    'vande-mataram-memorial': {
        'name':        'Vande Mataram Memorial',
        'title':       'Vande Mataram Memorial Bhujodi | Freedom Struggle Tribute',
        'description': 'Visit Vande Mataram Memorial at Bhujodi — a moving tribute to India\'s freedom fighters, with exhibits on the independence movement, located near the famous weaving village.',
        'keywords':    'Vande Mataram Memorial,Vande Mataram Bhujodi,Kutch independence memorial,Bhujodi Bhuj,Kutch heritage sites,India freedom memorial Kutch,Bhuj attraction',
        'category':    'Heritage Memorial',
        'region':      'Bhujodi, Kutch, Gujarat',
        'lat':          23.2580,
        'lon':          69.6850,
    },
    'vijay-vilas-palace': {
        'name':        'Vijay Vilas Palace',
        'title':       'Vijay Vilas Palace Mandvi | Royal Kutchi Palace & Beach',
        'description': 'Explore Vijay Vilas Palace in Mandvi — a stunning 1920s royal palace with Indo-Saracenic architecture, private beach access & ornate interiors. Film location for Ashoka & Hum Dil De Chuke Sanam.',
        'keywords':    'Vijay Vilas Palace Mandvi,Mandvi palace Kutch,Kutch royal palace,Vijay Vilas Kutch,Mandvi beach palace,Gujarat palace tourism,Kutch Bollywood location',
        'category':    'Royal Palace & Heritage',
        'region':      'Mandvi, Kutch, Gujarat',
        'lat':          22.8391,
        'lon':          69.3475,
    },
}


def make_structured_data(slug, info):
    """Return JSON-LD TouristAttraction + BreadcrumbList as a compact string."""
    sd = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TouristAttraction",
                "name": info['name'],
                "description": info['description'],
                "url": f"{DOMAIN}/places/{slug}/",
                "image": f"{DOMAIN}/images/places/{slug}/main.webp",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": info['region'],
                    "addressCountry": "IN"
                },
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": info['lat'],
                    "longitude": info['lon']
                },
                "touristType": "Cultural Tourism",
                "availableLanguage": ["English", "Hindi", "Gujarati"]
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1,
                     "name": "Home", "item": f"{DOMAIN}/"},
                    {"@type": "ListItem", "position": 2,
                     "name": "Places", "item": f"{DOMAIN}/places/"},
                    {"@type": "ListItem", "position": 3,
                     "name": info['name'], "item": f"{DOMAIN}/places/{slug}/"}
                ]
            }
        ]
    }
    return json.dumps(sd, ensure_ascii=False)


def patch_seo(content, slug, info):
    """Patch all SEO tags in the HTML string and return new content."""
    url      = f"{DOMAIN}/places/{slug}/"
    img      = f"{DOMAIN}/images/places/{slug}/main.webp"
    title    = info['title']
    desc     = info['description']
    keywords = info['keywords']
    sd_json  = make_structured_data(slug, info)

    # 1) <title>
    content = re.sub(r'<title>[^<]*</title>',
                     f'<title>{title}</title>', content)

    # 2) meta description
    content = re.sub(r'<meta name="description" content="[^"]*"',
                     f'<meta name="description" content="{desc}"', content)

    # 3) meta keywords  — replace existing or add after description
    if re.search(r'<meta name="keywords"', content):
        content = re.sub(r'<meta name="keywords" content="[^"]*"',
                         f'<meta name="keywords" content="{keywords}"', content)
    else:
        content = content.replace(
            '<meta name="robots"',
            f'<meta name="keywords" content="{keywords}"/>\n  <meta name="robots"',
            1
        )

    # 4) canonical
    content = re.sub(r'<link rel="canonical" href="[^"]*"',
                     f'<link rel="canonical" href="{url}"', content)

    # 5) og:title
    content = re.sub(r'<meta property="og:title" content="[^"]*"',
                     f'<meta property="og:title" content="{title}"', content)

    # 6) og:description
    content = re.sub(r'<meta property="og:description" content="[^"]*"',
                     f'<meta property="og:description" content="{desc}"', content)

    # 7) og:image
    content = re.sub(r'<meta property="og:image" content="[^"]*"',
                     f'<meta property="og:image" content="{img}"', content)

    # 8) og:url
    content = re.sub(r'<meta property="og:url" content="[^"]*"',
                     f'<meta property="og:url" content="{url}"', content)

    # 9) twitter:title
    content = re.sub(r'<meta name="twitter:title" content="[^"]*"',
                     f'<meta name="twitter:title" content="{title}"', content)

    # 10) twitter:image
    content = re.sub(r'<meta name="twitter:image" content="[^"]*"',
                     f'<meta name="twitter:image" content="{img}"', content)

    # 11) JSON-LD structured data — replace existing or inject after <!-- Structured Data -->
    ld_block = f'<script type="application/ld+json">{sd_json}</script>'
    existing_ld = re.search(
        r'<script type="application/ld\+json">.*?</script>',
        content, re.DOTALL
    )
    if existing_ld:
        content = content[:existing_ld.start()] + ld_block + content[existing_ld.end():]
    else:
        content = content.replace(
            '<!-- Structured Data -->',
            f'<!-- Structured Data -->\n  {ld_block}',
            1
        )

    return content


def main():
    updated = []
    errors  = []

    for slug, info in PLACES.items():
        html_path = os.path.join(ROOT, 'places', slug, 'index.html')
        if not os.path.exists(html_path):
            print(f'  [MISSING] places/{slug}/index.html')
            continue

        try:
            with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            new_content = patch_seo(content, slug, info)

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f'  [OK] places/{slug}/')
            updated.append(slug)

        except Exception as e:
            print(f'  [ERR] places/{slug}: {e}')
            errors.append(slug)

    print()
    print('=' * 60)
    print(f'Updated : {len(updated)} place pages')
    print(f'Errors  : {len(errors)}')
    print('=' * 60)

if __name__ == '__main__':
    main()
