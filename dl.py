import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

LOGO_DEV_KEY = "pk_Lkgv2GbETbS0ULQwNvKv5Q"

headers = {
    "User-Agent": "Mozilla/5.0"
}

os.makedirs("icons", exist_ok=True)


# ----------------------------
# Get domain from company name
# ----------------------------
def get_domain(company):
    try:
        url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={company}"
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        data = r.json()
        if not data:
            return None

        return data[0]["domain"], data[0]["name"]

    except:
        return None


# ----------------------------
# Download logo PNG
# ----------------------------
def download_logo(domain):
    try:
        url = f"https://img.logo.dev/{domain}?token={LOGO_DEV_KEY}&format=png"
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return False

        # CLEAN DOMAIN → filename (remove .com / .net / etc)
        clean_domain = domain.replace("www.", "")
        clean_domain = clean_domain.split(".")[0]

        filename = f"icons/{clean_domain}.png"

        # SKIP IF EXISTS (NO OVERWRITE)
        if os.path.exists(filename):
            print(f"⏩ Skipped (exists): {clean_domain}")
            return True

        with open(filename, "wb") as f:
            f.write(r.content)

        print(f"✅ Saved: {clean_domain}")
        return True

    except:
        return False


# ----------------------------
# Worker
# ----------------------------
def process_company(company):
    result = get_domain(company)

    if not result:
        print(f"❌ No domain: {company}")
        return company

    domain, real_name = result

    success = download_logo(domain)

    if success:
        return None
    else:
        print(f"❌ Failed: {company}")
        return company


# ----------------------------
# Main
# ----------------------------
def main(file_path, threads=10):
    with open(file_path, "r", encoding="utf-8") as f:
        companies = [c.strip() for c in f if c.strip()]

    failed = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(process_company, c) for c in companies]

        for f in as_completed(futures):
            res = f.result()
            if res:
                failed.append(res)

    # Save failures
    if failed:
        with open("failed.txt", "w", encoding="utf-8") as f:
            for c in failed:
                f.write(c + "\n")

        print(f"\n⚠️ Failed: {len(failed)} saved to failed.txt")
    else:
        print("\n🎉 All logos downloaded successfully!")


# RUN
main("companies.txt", threads=12)