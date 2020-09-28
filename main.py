from pathlib import Path
import requests
import re
import shutil


NAT = [
    "AUT",
    "BEL",
    "BGR",
    "CYP",
    "CZE",
    "DEU",
    "DNK",
    "ESP",
    "EST",
    "FIN",
    "FRA",
    "GRC",
    "HRV",
    "HUN",
    "IRL",
    "ITA",
    "LTU",
    "LUX",
    "LVA",
    "MLT",
    "NLD",
    "POL",
    "PRT",
    "ROU",
    "SVK",
    "SVN",
    "SWE",
    "CHE",
    "GBR",
    "ISL",
    "NOR",
]

for nat in NAT:
    types_1 = ["A", "B", "J", "I", "C", "H", "F", "G", "W", "X"]
    types_2 = ["O", "D", "S", "P", "M", "T", "Y", "B"]
    docs = []
    for type_1 in types_1:
        for type_2 in types_2:
            docs.append(f"{type_1}/{type_2}")
    for doc in docs:
        url = f"https://www.consilium.europa.eu/prado/en/prado-documents/{nat}/{doc}/docs-per-type.html"
        response = requests.get(url)
        text = response.text
        images = re.findall(r"images.................", text)
        img_urls = ["https://www.consilium.europa.eu/prado/" + img for img in images]
        for img_url in img_urls:
            filename = Path(img_url).name
            out = f"dump/{nat}/{doc[0]}_{doc[2]}_{filename}"
            out = str(Path(out).with_suffix(".jpg"))
            Path(out).parent.mkdir(parents=True, exist_ok=True)
            if Path(out).exists():
                print(f"File {out} exists, skipping ....")
            img_download_response = requests.get(img_url, stream=True)
            if img_download_response.status_code == 200:
                print(f"Processing {img_url}")
                with open(out, "wb") as out_file:
                    shutil.copyfileobj(img_download_response.raw, out_file)
                    print(f"Downloaded to {out}")
