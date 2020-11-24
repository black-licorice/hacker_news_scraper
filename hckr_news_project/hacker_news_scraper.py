import requests
from time import sleep
from bs4 import BeautifulSoup

# min score is minimum score value for posts to be chosen
min_score = input("Posts should have a minimum score of... \n  >")
try:
    min_score = int(min_score)
except ValueError:
    print("Please enter an integer...")
    exit(1)
# count is page count
count = 1


# get values for each page called
def init(p_count):
    # get hackernews
    site = 'https://news.ycombinator.com/news?p='
    res = requests.get(site + str(p_count))
    # set soup object
    soup = BeautifulSoup(res.text, 'html.parser')
    # sub_text contains the score, we can check if a score exists by checking the length of the score class in subtext
    sub_text = soup.select('.subtext')
    # anchors are anchor tags
    anchors = soup.select('.storylink')
    vals = {'soup': soup, 'sub_text': sub_text, 'anchors': anchors, 'res': res}
    return vals


def check_if_last_page():
    # if status_code is 400, then the previous page was the last
    if init(count)['res'].status_code == 400:
        return True
    return False


def get_posts(links, subtext):
    post_list = []
    for i, item in enumerate(links):
        # vote is the score class in subtext
        vote = subtext[i].select('.score')
        # if vote
        if len(vote):
            # score is the number of votes as an integer
            score = (int(vote[0].getText().strip(' points')))
            if score > min_score:
                href = item.get('href', None)
                # if href is to another page on the site, we must add the root route to the 'link'
                if href.startswith('item?'):
                    href = 'https://news.ycombinator.com/' + href
                # define only the variables we need for if statements until last var to save on runtime
                title = item.getText()
                # append post dictionary to post_list
                post_list.append({'title': title, 'link': href, 'score': score})
    return post_list


def print_posts():
    posts = get_posts(init(count)['anchors'], init(count)['sub_text'])
    for post in posts:
        print(f"Title: {post['title']}\nScore: {post['score']}\n  {post['link']}\n")


# check site every 10 mins
if __name__ == '__main__':
    min_time = 10
    while True:
        print_posts()
        if check_if_last_page():
            print('Last page scrapped, waiting ten minutes...')
            sleep(min_time * 60)
            count = 1
            continue
        else:
            count += 1
            print(f"Page {count}:")
