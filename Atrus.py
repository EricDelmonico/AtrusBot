import praw

reddit = praw.Reddit('atrusbot')
sub = reddit.subreddit('NintendoSwitchDeals')

# returns all post titles with links to
# them as long as the corresponding applies:
# 1. must be an eshop, amazon, or gamestop deal
# 2. must be in the US / USA
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

# get deals for the day, week, or both
def get_deals(day_or_week):
    both = day_or_week == 'both'
    if (both == True):
        day_or_week = 'week'

    # get top 50 submissions from /r/NintendoSwitchDeals
    submissions = sub.top(time_filter=day_or_week, limit=50)

    # start out the message with a heading
    body = '#Top deals of the ' + day_or_week + '\n\n\n\n'
    body += get_deal_titles(submissions) # add appropriate post titles to message

    # if both was inputted, we also 
    # need to get top deals of the day
    if (both == True):
        return body + get_deals('day')

    # if both was not inputted,
    # simply return the message
    else:
        return body

# if AtrusBot has gotten any messages, 
# reply back with a list of on sale games
inbox = reddit.inbox.unread()
for item in inbox:
    # do not reply to comments
    if (item.was_comment == True):
        continue

    # get weekly deals or daily?
    day_or_week = ''
    if (item.body.lower().find('daily') != -1 or
        item.body.lower().find('day') != -1):
        day_or_week += 'day'
    if (item.body.lower().find('weekly') != -1 or
        item.body.lower().find('week') != -1):
        day_or_week += 'week'
    # if both day and week or neither, do both
    if (len(day_or_week) > 4 or
        len(day_or_week) == 0):
        day_or_week = 'both'    

    # reply with the deals string
    item.reply(get_deals(day_or_week))
    item.mark_read()
    