# -*- coding: utf-8 -*-

about = '''
Everything is simple. You want find best advert but don`t want to live on refresh button.
I help you to make watcher on a gumtree advert board and you`ll get your best advert ASAP.
All I need, that you take URL (to desired advert category, with all filters applied) and two list of words: blacklist and whitelist.
I look for new adverts and check them, if there`s any of blacklist words in it - I drop it.
If there`s a whitelist words - I write a direct message to you, otherwise, just send link to this ad to our chat. 
You can add those watchers as much as you want. And delete them when they become unnecessary. All simple.
Let`s go, try your keyboard!
'''


def about_message(chat, *args):
    return chat.send_text(about)


__author__ = 'manitou'
