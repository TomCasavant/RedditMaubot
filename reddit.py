from mautrix.types import EventType
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Tuple
from random import choice
import requests
from http.client import responses

class RedditPlugin(Plugin):
    @command.passive("(r/)([a-zA-Z]+)", multiple=True)
    async def handler(self, evt: MessageEvent, subs: List[Tuple[str,str]]) -> None:
        await evt.mark_read()
        subreddits = [] #List of all subreddits given by user
        for _, r, sub_str in subs:
            link = 'https://reddit.com/r/{}'.format(sub_str)
            r = requests.head(link, headers={'User-agent':'redditmaubot'}, allow_redirects=True)
            if ("/r/" in r.url):
                #Check if subreddit exists
                subreddits.append(link)

        if len(subreddits) > 0:
            condescending = ["Don't you mean {} ?", "Shouldn't this be {} ?", "Are you sure it isn't {} ?", "Isn't it {} ?", "uh, {} right?", "{} is probably what you're looking for"]
            response = choice(condescending).format("\n".join(subreddits))
            await evt.reply(response, html_in_markdown=True) #Reply to user
