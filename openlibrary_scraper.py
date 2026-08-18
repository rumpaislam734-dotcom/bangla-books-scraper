import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0"
}

base_url = "http://books.com.bd"
all_books = []

# First 5 pages দিয়ে test
for page in range(1, 6):

    if page == 1:
        url = f"{base_url}/list/"
    else:
        url = f"{base_url}/list/?page={page}"

    print(f"\nScraping Page {page}...")
    print("URL:", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Page failed:", response.status_code)
            continue

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find View Book links
        for link in soup.find_all("a", href=True):

            text = link.get_text(
                " ",
                strip=True
            )

            href = link.get(
                "href",
                ""
            ).strip()

            # Only View Book links
            if text.lower() != "view book":
                continue

            # Create actual book URL
            book_url = urljoin(
                base_url,
                href
            )

            print("\nBOOK URL FOUND:")
            print(book_url)

            try:

                book_response = requests.get(
                    book_url,
                    headers=headers,
                    timeout=20
                )

                if book_response.status_code != 200:
                    print(
                        "Book page failed:",
                        book_response.status_code
                    )
                    continue

                book_soup = BeautifulSoup(
                    book_response.text,
                    "html.parser"
                )

                # Get title
                title = ""

                if book_soup.title:
                    title = book_soup.title.get_text(
                        strip=True
                    )

                # Save data
                book = {
                    "Title": title,
                    "URL": book_url,
                    "Page": page
                }

                all_books.append(book)

                print(
                    "Collected:",
                    title[:80]
                )

            except Exception as e:

                print(
                    "Book error:",
                    e
                )

    except Exception as e:

        print(
            "Page error:",
            e
        )


# ==========================================
# REMOVE DUPLICATE BOOKS
# ==========================================

df = pd.DataFrame(all_books)

if not df.empty:

    df = df.drop_duplicates(
        subset=["URL"]
    )


# ==========================================
# RESULT
# ==========================================

print("\n")
print("=" * 50)
print(
    "TOTAL BOOKS:",
    len(df)
)
print("=" * 50)

print(
    df.head(10)
)


# ==========================================
# SAVE CSV
# ==========================================

df.to_csv(
    "bangla_books_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nCSV file saved successfully!"
)

print(
    "File: bangla_books_dataset.csv"
)