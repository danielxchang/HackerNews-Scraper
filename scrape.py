import requests
from bs4 import BeautifulSoup
import pprint

def retrieve_hn_webpage(page):
    payload = {'p': page}
    res = requests.get('https://news.ycombinator.com/news', params=payload if page > 1 else "")
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.titlelink')
    subtext = soup.select('.subtext')
    return links, subtext

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)

def sort_stories_by_votes(hn_list):
    return sorted(hn_list, key=lambda x: x['votes'], reverse=True)

def print_all(list):
    pprint.pprint(hn)

def top_5(hn_list):
    for place in range(5):
        print(f"#{place + 1}:")
        pprint.pprint(hn_list[place])
        print("\n")

def get_inputs():
    while True:
        try:
            pages = int(input("Enter number of pages to scrape: "))
            break
        except:
            print("Please enter an integer!")

    while True:
        try:
            setting = str(input('Top 5 or All? (Enter "T5" or "A"): '))
            if setting in ["T5", "A"]:
                break

            print('Please enter "T5" or "A"')
        except:
            print('Please enter a string!')

    return pages, setting


def main():
    pages, setting = get_inputs()
    links = []
    subtext = []
    for page in range(1, pages + 1):
        pg_links, pg_subtext = retrieve_hn_webpage(page)
        links.extend(pg_links)
        subtext.extend(pg_subtext)

    hn = create_custom_hn(links, subtext)

    print("\n")
    print(f'Total Articles (>=100 votes): {len(hn)}')
    print("\n")

    if setting == "T5":
        top_5(hn)
    else:
        print_all(hn)

if __name__ == "__main__":
    main()
