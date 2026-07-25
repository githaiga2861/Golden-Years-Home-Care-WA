# Golden Years Home Care WA — Setup

## 1. Create the repo & push (paste in your terminal)
    cd ~
    mkdir Golden-Years-Home-Care-WA && cd Golden-Years-Home-Care-WA
    # unzip the site files here, then:
    git init -b main
    git add -A
    git commit -m "Golden Years Home Care WA — initial site"
    # create an EMPTY repo named Golden-Years-Home-Care-WA on github.com first, then:
    git remote add origin https://github.com/githaiga2861/Golden-Years-Home-Care-WA.git
    git push -u origin main

## 2. Copy the logo from the main site
    cp ~/Golden-Years/images/logo.png images/
    cp ~/Golden-Years/images/favicon.png images/
    git add -A && git commit -m "Add logo" && git push

## 3. Paste your Web3Forms key
Search all .html files for:  40d97e85-xxxx-xxxx-xxxx-7624f70df2b0
Replace with your real access key (same one as the main site). One command:
    sed -i 's/40d97e85-xxxx-xxxx-xxxx-7624f70df2b0/YOUR-REAL-KEY-HERE/g' *.html
    git add -A && git commit -m "Web3Forms key" && git push

## 4. GitHub Pages
Repo → Settings → Pages → Source: Deploy from a branch → main / root → Save
Custom domain: goldenyearshomecarewa.com → Save → wait for check → Enforce HTTPS.

## 5. Cloudflare DNS (after buying goldenyearshomecarewa.com)
DNS → Records → add these 5 (Proxy status: DNS only / grey cloud):
    A     @    185.199.108.153
    A     @    185.199.109.153
    A     @    185.199.110.153
    A     @    185.199.111.153
    CNAME www  githaiga2861.github.io
The CNAME file in this repo is already set to goldenyearshomecarewa.com.
