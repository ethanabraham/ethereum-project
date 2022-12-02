import requests
from bs4 import BeautifulSoup
from csv import writer
from collections import Counter

with open("ethereum_magicians.csv", "w", encoding='utf-8', newline="") as f:
    writer = writer(f)
    header = ["Title", "Website", "EIP Number", "Category", "Author", "Article Body", "Comments", "Comment Authors"]
    writer.writerow(header)

    NUMBER_OF_PAGES = 58  # there are 58 pages
    for num in range(NUMBER_OF_PAGES):
        URL = 'https://ethereum-magicians.org/?page=' + str(num)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        topics = soup.find_all('span', class_='link-top-line')
        for topic in topics:
            # Extract Title
            title = topic.text.replace("\n", '')
            # Extract URL
            topic_url = topic.find('a')['href']
            info = [title, topic_url]

            subpage = requests.get(topic_url)
            subpage_soup = BeautifulSoup(subpage.content, "html.parser")

            # Get Primary Category
            cetegory_html = subpage_soup.find("span", itemprop="name")
            category = cetegory_html.text.replace("\n", '')

            EIP_number = ""
            if category == "EIPs":
                EIP_number = title.split()[0].upper()
                if EIP_number[-1] == ":":
                    EIP_number = EIP_number[:-1]
                if not EIP_number[-1].isdigit():
                    EIP_number = ""
                if "ERC" in EIP_number:
                    EIP_number = ""

            # Extract Author Name:
            username_html = subpage_soup.find("span", itemprop="author")
            username = username_html.text.replace("\n", '')

            # Extract Article Body
            article_body_html = subpage_soup.find("div", itemprop="articleBody")
            article_body = article_body_html.text.replace("\n", '')

            # Comments
            comments_html = subpage_soup.find_all('div', class_='post')
            comments = ""
            for i in range(1, len(comments_html)):
                comments += comments_html[i].text.replace("\n", '') + "\n"

            # comment authors
            comment_authors = subpage_soup.find_all("span", itemprop="author")
            list_of_authors = []
            for author in comment_authors[1:]:
                cleaned_author = author.find('span', itemprop="name")
                list_of_authors.append(cleaned_author.text)
            comment_author_count = str(Counter(list_of_authors))
            comment_author_count_cleaned = comment_author_count[9:-2]
            info.append(EIP_number)
            info.append(category)
            info.append(username)
            info.append(article_body)
            info.append(comments)
            info.append(comment_author_count_cleaned)
            writer.writerow(info)
