"""
Batch Scraping Tokopedia - Multiple Brands Laptop 10-15 Juta
Jalankan semua brand sekaligus secara otomatis.
"""

import requests
import json
import csv
import time
import random
import os
from datetime import datetime

# ============================================================
# KONFIGURASI
# ============================================================
BRANDS = [
    "laptop msi",
    "laptop axioo",
    "laptop advan",
    "laptop gigabyte",
    "laptop colorful",
    "laptop hp",
    "laptop dell",
]

MIN_PRICE = 10000000   # 10 juta
MAX_PRICE = 15000000   # 15 juta
ROWS_PER_PAGE = 60
MAX_PAGES = 5
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# HEADERS
# ============================================================
HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "content-type": "application/json",
    "origin": "https://www.tokopedia.com",
    "referer": "https://www.tokopedia.com/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "x-device": "desktop-0.0",
    "x-source": "tokopedia-lite",
    "x-tkpd-lite-service": "zeus",
}

GRAPHQL_QUERY = r"""query SearchProductV5Query($params: String!) {
  searchProductV5(params: $params) {
    header {
      totalData
      responseCode
      keywordProcess
      keywordIntention
      componentID
      isQuerySafe
      additionalParams
      backendFilters
      meta {
        dynamicFields
        __typename
      }
      __typename
    }
    data {
      totalDataText
      banner {
        position
        text
        applink
        url
        imageURL
        componentID
        trackingOption
        __typename
      }
      redirection {
        url
        __typename
      }
      related {
        relatedKeyword
        position
        trackingOption
        otherRelated {
          keyword
          url
          applink
          componentID
          products {
            oldID: id
            id: id_str_auto_
            name
            url
            applink
            mediaURL {
              image
              __typename
            }
            shop {
              oldID: id
              id: id_str_auto_
              name
              city
              tier
              __typename
            }
            badge {
              oldID: id
              id: id_str_auto_
              title
              url
              __typename
            }
            price {
              text
              number
              __typename
            }
            freeShipping {
              url
              __typename
            }
            labelGroups {
              position
              title
              type
              url
              styles {
                key
                value
                __typename
              }
              __typename
            }
            rating
            wishlist
            ads {
              id
              productClickURL
              productViewURL
              productWishlistURL
              tag
              __typename
            }
            meta {
              oldWarehouseID: warehouseID
              warehouseID: warehouseID_str_auto_
              componentID
              __typename
            }
            __typename
          }
          __typename
        }
        __typename
      }
      suggestion {
        currentKeyword
        suggestion
        query
        text
        componentID
        trackingOption
        __typename
      }
      ticker {
        oldID: id
        id: id_str_auto_
        text
        query
        applink
        componentID
        trackingOption
        __typename
      }
      violation {
        headerText
        descriptionText
        imageURL
        ctaURL
        ctaApplink
        buttonText
        buttonType
        __typename
      }
      products {
        oldID: id
        id: id_str_auto_
        ttsProductID
        name
        url
        applink
        mediaURL {
          image
          image300
          videoCustom
          __typename
        }
        shop {
          oldID: id
          id: id_str_auto_
          ttsSellerID
          name
          url
          city
          tier
          __typename
        }
        stock {
          ttsSKUID
          __typename
        }
        badge {
          oldID: id
          id: id_str_auto_
          title
          url
          __typename
        }
        price {
          text
          number
          range
          original
          discountPercentage
          __typename
        }
        freeShipping {
          url
          __typename
        }
        labelGroups {
          position
          title
          type
          url
          styles {
            key
            value
            __typename
          }
          __typename
        }
        labelGroupsVariant {
          title
          type
          typeVariant
          hexColor
          __typename
        }
        category {
          oldID: id
          id: id_str_auto_
          name
          breadcrumb
          gaKey
          __typename
        }
        rating
        wishlist
        ads {
          id
          productClickURL
          productViewURL
          productWishlistURL
          tag
          __typename
        }
        meta {
          oldParentID: parentID
          parentID: parentID_str_auto_
          oldWarehouseID: warehouseID
          warehouseID: warehouseID_str_auto_
          isImageBlurred
          isPortrait
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}
"""

def build_params(keyword, page):
    start = (page - 1) * ROWS_PER_PAGE
    return (
        f"device=desktop&enter_method=normal_search&l_name=sre&navsource="
        f"&ob=23&page={page}&pmin={MIN_PRICE}&pmax={MAX_PRICE}"
        f"&q={keyword}&related=true&rows={ROWS_PER_PAGE}"
        f"&safe_search=false&sc=&scheme=https&shipping="
        f"&show_adult=false&source=search&srp_component_id=02.01.00.00"
        f"&srp_page_id=&srp_page_title=&st=product&start={start}"
        f"&topads_bucket=true&unique_id=scraper_{int(time.time())}"
        f"&variants=&warehouses="
    )

def scrape_page(session, keyword, page):
    payload = [{
        "operationName": "SearchProductV5Query",
        "variables": {"params": build_params(keyword, page)},
        "query": GRAPHQL_QUERY
    }]
    
    try:
        resp = session.post(
            "https://gql.tokopedia.com/graphql/SearchProductV5Query",
            json=payload, headers=HEADERS, timeout=30
        )
        if resp.status_code != 200:
            print(f"    [ERROR] HTTP {resp.status_code}")
            return [], 0
        
        raw = resp.json()
        data = raw[0] if isinstance(raw, list) else raw
        
        if "errors" in data and data["errors"]:
            for e in data["errors"]:
                print(f"    GraphQL Error: {e.get('message')}")
            if data.get("data") is None:
                return [], 0
        
        if not data.get("data"):
            return [], 0
        
        sr = data["data"].get("searchProductV5")
        if not sr:
            return [], 0
        
        total = (sr.get("header") or {}).get("totalData", 0)
        products_data = (sr.get("data") or {}).get("products") or []
        
        products = []
        for p in products_data:
            ads = p.get("ads")
            is_ad = bool(ads and ads.get("tag"))
            
            pi = p.get("price") or {}
            si = p.get("shop") or {}
            
            badge_raw = p.get("badge")
            badge_titles = []
            if badge_raw:
                if isinstance(badge_raw, dict):
                    if badge_raw.get("title"):
                        badge_titles.append(badge_raw["title"])
                elif isinstance(badge_raw, list):
                    badge_titles = [b.get("title") for b in badge_raw if isinstance(b, dict) and b.get("title")]
            
            cat = p.get("category") or {}
            fs = p.get("freeShipping") or {}
            
            label_groups = p.get("labelGroups") or []
            sold = ""
            cb = ""
            for lg in label_groups:
                if lg and lg.get("position") == "integrity":
                    sold = lg.get("title", "")
                elif lg and lg.get("type") == "textBold" and "cashback" in (lg.get("title", "")).lower():
                    cb = lg.get("title", "")
            
            mu = p.get("mediaURL") or {}
            
            products.append({
                "nama_produk": p.get("name", ""),
                "harga": pi.get("text", ""),
                "harga_angka": pi.get("number", 0),
                "harga_asli": pi.get("original", ""),
                "diskon_persen": pi.get("discountPercentage", 0),
                "rating": p.get("rating", ""),
                "terjual": sold,
                "nama_toko": si.get("name", ""),
                "kota": si.get("city", ""),
                "tier_toko": si.get("tier", 0),
                "badge": ", ".join(badge_titles),
                "kategori": cat.get("name", ""),
                "gratis_ongkir": "Ya" if fs.get("url") else "Tidak",
                "cashback": cb,
                "is_iklan": "Ya" if is_ad else "Tidak",
                "url": p.get("url", ""),
                "image_url": mu.get("image", ""),
            })
        
        return products, total
    except Exception as e:
        print(f"    [ERROR] {e}")
        return [], 0

def scrape_brand(session, keyword):
    brand_name = keyword.replace("laptop ", "")
    date_str = datetime.now().strftime('%d-%m-%Y')
    output_file = os.path.join(OUTPUT_DIR, f"tokopedia_{brand_name}_{date_str}.csv")
    
    print(f"\n{'='*60}")
    print(f"  SCRAPING: {keyword.upper()} | Rp{MIN_PRICE:,.0f} - Rp{MAX_PRICE:,.0f}")
    print(f"{'='*60}")
    
    all_products = []
    
    for page in range(1, MAX_PAGES + 1):
        print(f"  [Page {page}/{MAX_PAGES}] ", end="")
        
        products, total = scrape_page(session, keyword, page)
        
        if page == 1:
            print(f"Total: {total} produk | ", end="")
        
        if not products:
            print("Kosong. Stop.")
            break
        
        filtered = [p for p in products if p["harga_angka"] and MIN_PRICE <= p["harga_angka"] <= MAX_PRICE]
        all_products.extend(filtered)
        print(f"{len(filtered)} produk OK | Total: {len(all_products)}")
        
        if len(products) < ROWS_PER_PAGE:
            break
        
        time.sleep(random.uniform(2, 4))
    
    # Dedup
    seen = set()
    unique = []
    for p in all_products:
        if p["url"] not in seen:
            seen.add(p["url"])
            unique.append(p)
    
    if unique:
        fieldnames = [
            "nama_produk", "harga", "harga_angka", "harga_asli", "diskon_persen",
            "rating", "terjual", "nama_toko", "kota", "tier_toko", "badge",
            "kategori", "gratis_ongkir", "cashback", "is_iklan", "url", "image_url"
        ]
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique)
        print(f"  >> Tersimpan: {len(unique)} produk -> {os.path.basename(output_file)}")
    else:
        print(f"  >> Tidak ada produk ditemukan untuk {brand_name}")
    
    return brand_name, len(unique), output_file

def main():
    print("=" * 60)
    print("  TOKOPEDIA BATCH SCRAPER - Multi Brand")
    print(f"  Harga: Rp{MIN_PRICE:,.0f} - Rp{MAX_PRICE:,.0f}")
    print(f"  Brands: {len(BRANDS)}")
    print("=" * 60)
    
    session = requests.Session()
    results = []
    
    for i, keyword in enumerate(BRANDS, 1):
        print(f"\n[{i}/{len(BRANDS)}] ", end="")
        brand, count, fpath = scrape_brand(session, keyword)
        results.append((brand, count, fpath))
        
        # Delay antar brand
        if i < len(BRANDS):
            d = random.uniform(3, 5)
            print(f"  Delay {d:.1f}s antar brand...")
            time.sleep(d)
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"  RINGKASAN SCRAPING")
    print(f"{'='*60}")
    total = 0
    for brand, count, fpath in results:
        print(f"  {brand.upper():12s} : {count:4d} produk  -> {os.path.basename(fpath)}")
        total += count
    print(f"  {'TOTAL':12s} : {total:4d} produk")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
