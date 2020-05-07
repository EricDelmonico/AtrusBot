import praw

reddit = praw.Reddit('atrusbot')
sub = reddit.subreddit('NintendoSwitchDeals')

submissions = sub.top(time_filter='week', limit=50)

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

    print(title)

