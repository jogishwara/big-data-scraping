"""
Scraping Tokopedia - MacBook Harga 10-15 Juta
Menggunakan Tokopedia GraphQL API (SearchProductV5Query)
Query diambil dari curl command yang sudah berhasil sebelumnya.
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
KEYWORD = "laptop lenovo"
MIN_PRICE = 10000000   # 10 juta
MAX_PRICE = 15000000   # 15 juta
ROWS_PER_PAGE = 60
MAX_PAGES = 5          # Scrape hingga 5 halaman
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"tokopedia_lenovo_{datetime.now().strftime('%d-%m-%Y')}.csv")

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

# GraphQL query - EXACT copy dari curl yang sudah berhasil
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

def build_params(page: int) -> str:
    """Membangun parameter pencarian untuk GraphQL query."""
    start = (page - 1) * ROWS_PER_PAGE
    params = (
        f"device=desktop"
        f"&enter_method=normal_search"
        f"&l_name=sre"
        f"&navsource="
        f"&ob=23"
        f"&page={page}"
        f"&pmin={MIN_PRICE}"
        f"&pmax={MAX_PRICE}"
        f"&q={KEYWORD}"
        f"&related=true"
        f"&rows={ROWS_PER_PAGE}"
        f"&safe_search=false"
        f"&sc="
        f"&scheme=https"
        f"&shipping="
        f"&show_adult=false"
        f"&source=search"
        f"&srp_component_id=02.01.00.00"
        f"&srp_page_id="
        f"&srp_page_title="
        f"&st=product"
        f"&start={start}"
        f"&topads_bucket=true"
        f"&unique_id=scraper_{int(time.time())}"
        f"&variants="
        f"&warehouses="
    )
    return params

def scrape_page(session: requests.Session, page: int) -> tuple:
    """Scrape satu halaman hasil pencarian."""
    params = build_params(page)
    
    payload = [{
        "operationName": "SearchProductV5Query",
        "variables": {
            "params": params
        },
        "query": GRAPHQL_QUERY
    }]
    
    url = "https://gql.tokopedia.com/graphql/SearchProductV5Query"
    
    try:
        response = session.post(url, json=payload, headers=HEADERS, timeout=30)
        
        print(f"  HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  [ERROR] HTTP {response.status_code}")
            print(f"  Response: {response.text[:500]}")
            return [], 0
        
        raw_data = response.json()
        
        # Debug: simpan raw response halaman pertama
        if page == 1:
            debug_file = os.path.join(OUTPUT_DIR, "debug_response.json")
            with open(debug_file, "w", encoding="utf-8") as f:
                json.dump(raw_data, f, indent=2, ensure_ascii=False)
            print(f"  Debug response disimpan ke: debug_response.json")
        
        # Response berupa array
        if isinstance(raw_data, list):
            if len(raw_data) == 0:
                print("  [ERROR] Response array kosong")
                return [], 0
            data = raw_data[0]
        else:
            data = raw_data
        
        # Cek error
        if "errors" in data and data["errors"]:
            for err in data["errors"]:
                print(f"  GraphQL Error: {err.get('message', 'Unknown')}")
            if data.get("data") is None:
                return [], 0
        
        if "data" not in data or data["data"] is None:
            print(f"  [ERROR] 'data' field tidak ada atau None")
            return [], 0
        
        search_result = data["data"].get("searchProductV5")
        if search_result is None:
            print(f"  [ERROR] 'searchProductV5' tidak ada")
            return [], 0
        
        header = search_result.get("header") or {}
        total_data = header.get("totalData", 0)
        
        products_raw = search_result.get("data") or {}
        products_data = products_raw.get("products") or []
        
        products = []
        for p in products_data:
            ads = p.get("ads")
            is_ad = bool(ads and ads.get("tag"))
            
            price_info = p.get("price") or {}
            price_text = price_info.get("text", "")
            price_number = price_info.get("number", 0)
            original_price = price_info.get("original", "")
            discount_pct = price_info.get("discountPercentage", 0)
            
            shop_info = p.get("shop") or {}
            shop_name = shop_info.get("name", "")
            shop_city = shop_info.get("city", "")
            shop_tier = shop_info.get("tier", 0)
            
            badge_raw = p.get("badge")
            badge_titles = []
            if badge_raw:
                if isinstance(badge_raw, dict):
                    if badge_raw.get("title"):
                        badge_titles.append(badge_raw["title"])
                elif isinstance(badge_raw, list):
                    badge_titles = [b.get("title") for b in badge_raw if isinstance(b, dict) and b.get("title")]
            badge_str = ", ".join(badge_titles)
            
            category = p.get("category") or {}
            category_name = category.get("name", "")
            
            free_ship = p.get("freeShipping") or {}
            has_free_shipping = bool(free_ship.get("url"))
            
            rating = p.get("rating", "")
            
            label_groups = p.get("labelGroups") or []
            sold_count = ""
            cashback = ""
            for lg in label_groups:
                if lg and lg.get("position") == "integrity":
                    sold_count = lg.get("title", "")
                elif lg and lg.get("type") == "textBold" and "cashback" in (lg.get("title", "")).lower():
                    cashback = lg.get("title", "")
            
            media_url = p.get("mediaURL") or {}
            
            product = {
                "nama_produk": p.get("name", ""),
                "harga": price_text,
                "harga_angka": price_number,
                "harga_asli": original_price,
                "diskon_persen": discount_pct,
                "rating": rating,
                "terjual": sold_count,
                "nama_toko": shop_name,
                "kota": shop_city,
                "tier_toko": shop_tier,
                "badge": badge_str,
                "kategori": category_name,
                "gratis_ongkir": "Ya" if has_free_shipping else "Tidak",
                "cashback": cashback,
                "is_iklan": "Ya" if is_ad else "Tidak",
                "url": p.get("url", ""),
                "image_url": media_url.get("image", ""),
            }
            products.append(product)
        
        return products, total_data
        
    except requests.exceptions.RequestException as e:
        print(f"  [ERROR] Request gagal: {e}")
        return [], 0
    except Exception as e:
        print(f"  [ERROR] Unexpected: {e}")
        import traceback
        traceback.print_exc()
        return [], 0

def main():
    print("=" * 70)
    print("  TOKOPEDIA SCRAPER - MacBook Harga 10-15 Juta")
    print("=" * 70)
    print(f"  Keyword    : {KEYWORD}")
    print(f"  Harga      : Rp{MIN_PRICE:,.0f} - Rp{MAX_PRICE:,.0f}")
    print(f"  Max Pages  : {MAX_PAGES}")
    print(f"  Output     : {OUTPUT_FILE}")
    print("=" * 70)
    
    session = requests.Session()
    
    all_products = []
    total_data = 0
    
    for page in range(1, MAX_PAGES + 1):
        print(f"\n[Page {page}/{MAX_PAGES}] Scraping...")
        
        products, total = scrape_page(session, page)
        
        if page == 1:
            total_data = total
            print(f"  Total produk ditemukan: {total_data}")
        
        if not products:
            print(f"  Tidak ada produk di halaman {page}. Berhenti.")
            break
        
        # Filter hanya produk dalam range harga (double check)
        filtered = []
        for p in products:
            price = p["harga_angka"]
            if price and MIN_PRICE <= price <= MAX_PRICE:
                filtered.append(p)
        
        all_products.extend(filtered)
        print(f"  Berhasil: {len(products)} produk, {len(filtered)} sesuai range harga")
        print(f"  Total terkumpul: {len(all_products)} produk")
        
        if len(products) < ROWS_PER_PAGE:
            print(f"  Halaman terakhir tercapai.")
            break
        
        # Delay random
        delay = random.uniform(2, 4)
        print(f"  Menunggu {delay:.1f} detik...")
        time.sleep(delay)
    
    # Hapus duplikat
    seen_urls = set()
    unique_products = []
    for p in all_products:
        if p["url"] not in seen_urls:
            seen_urls.add(p["url"])
            unique_products.append(p)
    
    print(f"\n{'=' * 70}")
    print(f"  HASIL SCRAPING")
    print(f"{'=' * 70}")
    print(f"  Total produk terkumpul : {len(all_products)}")
    print(f"  Setelah hapus duplikat : {len(unique_products)}")
    
    if not unique_products:
        print("\n  [!] Tidak ada produk yang ditemukan.")
        print("  [!] Cek file debug_response.json untuk detail.")
        return
    
    # Simpan ke CSV
    fieldnames = [
        "nama_produk", "harga", "harga_angka", "harga_asli", "diskon_persen",
        "rating", "terjual", "nama_toko", "kota", "tier_toko", "badge",
        "kategori", "gratis_ongkir", "cashback", "is_iklan", "url", "image_url"
    ]
    
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_products)
    
    print(f"  File tersimpan: {OUTPUT_FILE}")
    
    # Preview
    print(f"\n{'=' * 70}")
    print(f"  PREVIEW DATA (10 produk pertama)")
    print(f"{'=' * 70}")
    
    for i, p in enumerate(unique_products[:10], 1):
        nama = p["nama_produk"][:70] + "..." if len(p["nama_produk"]) > 70 else p["nama_produk"]
        print(f"\n  {i}. {nama}")
        print(f"     Harga  : {p['harga']}")
        if p['diskon_persen']:
            print(f"     Diskon : {p['diskon_persen']}% (dari {p['harga_asli']})")
        print(f"     Rating : {p['rating'] if p['rating'] else '-'}")
        print(f"     Terjual: {p['terjual'] if p['terjual'] else '-'}")
        print(f"     Toko   : {p['nama_toko']} ({p['kota']})")
        if p['badge']:
            print(f"     Badge  : {p['badge']}")
    
    print(f"\n{'=' * 70}")
    print(f"  Scraping selesai! {len(unique_products)} produk MacBook Rp10-15jt tersimpan.")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
