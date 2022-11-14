from random import choice
from typing import List, Tuple, Type
import urllib.parse
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

# Setup config file
class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("reddit_base")

class RedditPlugin(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.passive("((^| )r\/)([^\s^,^.]+)", multiple=True)
    async def handler(self, evt: MessageEvent, subs: List[Tuple[str, str]]) -> None:
        await evt.mark_read()
        subreddits = []  # List of all subreddits given by user
        for _, r_slash, __, sub_str in subs:
            base_url = self.config["reddit_base"]
            link = "https://{}/r/{}".format(base_url, urllib.parse.quote(sub_str.lower()))

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
            all_subs = f"\n".join(subreddits)
            condescending = [
                f"Don't you mean {all_subs} ?",
                f"Shouldn't this be {all_subs} ?",
                f"Are you sure it isn't {all_subs} ?",
                f"Isn't it {all_subs} ?",
                f"uh, {all_subs} right?",
                f"{all_subs} is probably what you're looking for",
            ]
            response = f"{choice(condescending)}"
            await evt.reply(response, allow_html=True)  # Reply to user
