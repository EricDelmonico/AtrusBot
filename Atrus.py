import praw

reddit = praw.Reddit('atrusbot')

def get_deal_titles(submissions):
    body = ''
    for submission in submissions:
        # grab the title for processing
        title = submission.title

        # make sure the deal is in the USA. This should  
        # (in theory) chop out any [META] posts as well.
        if (title.lower().find('usa') == -1 and title.lower().find('us') == -1):
            continue

        # really only looking for eshop/amazon/gamestop deals
        if (title.lower().find('eshop') == -1 and 
            title.lower().find('amazon') == -1 and
            title.lower().find('gamestop') == -1):
            continue
        
        # giving the post title and a link to the post
        body += '[' + submission.title + ']' + '(' + submission.permalink + ')' + '\n\n'
    return body

def get_weekly_deals():
    # get the top 50 submisions for the 
    # week from /r/nintendoswitchdeals
    sub = reddit.subreddit('NintendoSwitchDeals')
        
    # put together a message
    # -----------------------
    # weekly deals
    submissions = sub.top(time_filter='week', limit=50)
    body = '#Top deals of the week\n\n\n\n'
    body += get_deal_titles(submissions)
    
    #daily deals
    submissions = sub.top(time_filter='day', limit=30)
    body += '\n\n\n\n#Top Deals of the day\n\n\n\n'
    body += get_deal_titles(submissions)
    # -----------------------

    return body

# if AtrusBot has gotten any messages, 
# reply back with a list of on sale games
inbox = reddit.inbox.unread()
for item in inbox:
    # do not reply to comments
    if (item.was_comment == True):
        continue
    item.reply(get_weekly_deals())
    item.mark_read()
    