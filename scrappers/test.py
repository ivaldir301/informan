import httpx

# Define the URL and headers for the API request
url = "https://expressodasilhas.cv/ping/hello"
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-CV,pt;q=0.9,en-GB;q=0.8,en;q=0.7,pt-PT;q=0.6,en-US;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://expressodasilhas.cv",
    "Referer": "https://expressodasilhas.cv/politica",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

# Define the payload form data
payload = {
    "user": "nobody",
    "path": "/politica",
    "section": "politica",
    "lastTime": "1737054619",
    "referrer": "https://expressodasilhas.cv/conteudo-patrocinado",
}

# Make the POST request to the API
response = httpx.post(url, headers=headers, data=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    news_data = response.json()
    print("News Data:", news_data)
else:
    print(f"Error: {response.status_code}, {response.text}")
