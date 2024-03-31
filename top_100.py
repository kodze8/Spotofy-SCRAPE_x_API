import requests
from bs4 import BeautifulSoup


def song_author_pair(date):
    response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
    # response.text gives us html format, otherwise response is 200,300, or smth else
    parse = BeautifulSoup(response.text, "html.parser")

    class_song_name99 = (
        "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 "
        "u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
        "u-max-width-230@tablet-only")
    class_song_name1 = (
        "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 "
        "u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 "
        "u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
    class_author99 = (
        "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max "
        "u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 "
        "u-max-width-230@tablet-only")
    class_author1 = (
        "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max "
        "u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 "
        "u-max-width-230@tablet-only u-font-size-20@tablet")

    song_99 = [a.text.strip() for a in parse.findAll(class_=class_song_name99)]
    song_1 = [a.text.strip() for a in parse.findAll(class_=class_song_name1)]

    author_1 = [a.text.strip() for a in parse.findAll(class_=class_author1)]
    author_99 = [a.text.strip() for a in parse.findAll(class_=class_author99)]

    return list(zip(song_1 + song_99, author_1 + author_99))
