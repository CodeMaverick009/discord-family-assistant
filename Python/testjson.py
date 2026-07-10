from scraper import scrape_page
from ai import analyze_page

page = scrape_page("https://www.efteling.com")

response = analyze_page(page)

print(response)