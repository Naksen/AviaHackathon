import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse_reviews_from_page(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    reviews = soup.find_all("div", class_="la8a5ef73")
    parsed_reviews = []

    for review in reviews:

        title_tag = review.find("h3", class_="text-weight-medium")
        title = title_tag.text.strip() if title_tag else "Заголовок отсутствует"

        link_tag = title_tag.find("a") if title_tag else None
        link = f"https://www.banki.ru{link_tag['href']}" if link_tag else "Ссылка отсутствует"

        text_tag = review.find("div", class_="l22dd3882")
        text = text_tag.text.strip() if text_tag else "Текст отсутствует"

        rating_tag = review.find("div", class_="lb3db10af")
        rating = rating_tag.text.strip() if rating_tag else "Оценка отсутствует"

        date_tag = review.find("span", class_="l0caf3d5f")
        date = date_tag.text.strip() if date_tag else "Дата отсутствует"

        parsed_reviews.append({
            "title": title,
            "link": link,
            "rating": rating,
            "text": text,
            "date": date,
        })
    return parsed_reviews


base_url = "https://www.banki.ru/services/responses/bank/promsvyazbank/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

all_reviews = []

for page in range(1, 316):  # Всего 315 страниц
    print(f"Парсим страницу {page}...")
    url = f"{base_url}?page={page}&is_countable=on"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        reviews = parse_reviews_from_page(response.text)
        all_reviews.extend(reviews)
    else:
        print(f"Ошибка при загрузке страницы {page}: {response.status_code}")

print(f"Всего собрано отзывов: {len(all_reviews)}")

df = pd.DataFrame(all_reviews)
df.to_csv("reviews.csv", index=False, encoding="utf-8")
print("Отзывы сохранены в файл reviews.csv")
