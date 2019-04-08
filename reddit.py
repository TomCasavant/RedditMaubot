from random import choice
from typing import List, Tuple
import urllib.parse
from maubot import Plugin, MessageEvent
from maubot.handlers import command

class RedditPlugin(Plugin):
    @command.passive("(r/)([^\s]+)", multiple=True)
    async def handler(self, evt: MessageEvent, subs: List[Tuple[str, str]]) -> None:
        await evt.mark_read()
        subreddits = []  # List of all subreddits given by user
        for _, rslash, sub_str in subs:
            link = "https://reddit.com/r/{}".format(urllib.parse.quote(sub_str))

            async with self.http.head(
                link, headers={"User-agent": "redditmaubot"}, allow_redirects=True
            ) as response:
                # Save url and status code of url
                url = str(response.url)
                status = response.status

            if "/r/" in str(url) and status != 404:
                # Check if subreddit exists
                subreddits.append(link)

        if subreddits:
            condescending = [
                "Don't you mean {} ?",
                "Shouldn't this be {} ?",
                "Are you sure it isn't {} ?",
                "Isn't it {} ?",
                "uh, {} right?",
                "{} is probably what you're looking for",
            ]
            response = choice(condescending).format("\n".join(subreddits))
            await evt.reply(url, html_in_markdown=True)  # Reply to user
