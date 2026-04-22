from src.crawler import WebCrawler
import mysql.connector
import time
from urllib.parse import urlparse

URL = "https://www.astranautas.com/"  # 🔥 CAMBIA ESTO

crawler = WebCrawler()
crawler.start_crawl(URL)

while crawler.is_running:
    time.sleep(2)

results = crawler.get_status().get("urls", [])

dominio = urlparse(URL).netloc

conn = mysql.connector.connect(
    host="TU_HOST_CPANEL",
    user="crawler_user",
    password="TU_PASSWORD_REAL",
    database="crawler_db"
)

cursor = conn.cursor()

for r in results:
    cursor.execute("""
    INSERT INTO resultados (url, title, status_code, seo_score, dominio)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        r.get("url"),
        r.get("title"),
        r.get("status_code"),
        len(r.get("title", "") or ""),
        dominio
    ))

conn.commit()
conn.close()

print("DONE")
