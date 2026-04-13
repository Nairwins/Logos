import requests
import time

LOGO_DEV_KEY = "pk_Lkgv2GbETbS0ULQwNvKv5Q"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Get domain from company name
def get_domain(name):
    url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={name}"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None
        
        data = res.json()
        if not data:
            return None
        
        return data[0].get("domain"), data[0].get("name")
    
    except:
        return None


# Download PNG logo
def download_logo(domain, name):
    url = f"https://img.logo.dev/{domain}?token={LOGO_DEV_KEY}&format=png"
    
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return False
        
        filename = name.replace(" ", "_") + ".png"
        
        with open(filename, "wb") as f:
            f.write(res.content)
        
        return True
    
    except:
        return False


# Main process
def process_file(file_path):
    failed = []

    with open(file_path, "r") as f:
        companies = [line.strip() for line in f if line.strip()]

    total = len(companies)

    for i, company in enumerate(companies, 1):
        print(f"\n[{i}/{total}] 🔍 {company}")

        result = get_domain(company)

        if not result:
            print("❌ Domain not found")
            failed.append(company)
            continue

        domain, real_name = result
        print(f"✅ Found: {real_name} ({domain})")

        success = download_logo(domain, real_name)

        if success:
            print("✅ Logo saved")
        else:
            print("❌ Logo failed")
            failed.append(company)

        time.sleep(0.3)  # avoid rate limit

    # Save failed कंपनies
    if failed:
        with open("failed.txt", "w") as f:
            for c in failed:
                f.write(c + "\n")

        print("\n⚠️ Failed companies saved to failed.txt")
    else:
        print("\n🎉 All الشركات downloaded successfully!")


# Run
process_file("companies.txt")