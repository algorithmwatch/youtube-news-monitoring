"""
Retrieve some videos info from given channel.

"""

import json
from pathlib import Path

import pandas as pd
import pyyoutube
from tqdm import tqdm

NUM_VIDEOS = 2000
API_KEY = Path("secrets.txt").read_text()

api = pyyoutube.Api(api_key=API_KEY)


def get_videos(channel_id):
    channel_res = api.get_channel_info(channel_id=channel_id)

    playlist_id = channel_res.items[0].contentDetails.relatedPlaylists.uploads

    # count=None => restrict total number of videos
    # limit=50 => 50 videos per page
    playlist_item_res = api.get_playlist_items(
        playlist_id=playlist_id, count=NUM_VIDEOS, limit=50
    )

    return playlist_item_res.items


def processor(channel_name):
    r = api.search_by_keywords(
        q=channel_name, search_type=["channel"], count=1, limit=1
    )
    channel_id = r.items[0].id.channelId
    file_path = Path("channeldata") / (channel_id + ".json")

    if not file_path.is_file():
        videos = [v.to_json() for v in get_videos(channel_id)]
        file_path.write_text(json.dumps(videos))

    return channel_id


if __name__ == "__main__":
    df = pd.read_pickle("df.pkl")
    Path("channeldata").mkdir(exist_ok=True)
    chan_path = Path("chan2id.json")

    chan2id = []
    for channel in tqdm(df["channel"].unique()):
        if chan_path.is_file():
            chan2id = json.loads(chan_path.read_text())

        # prevent unnessary searches for the channel id
        if len([x for x in chan2id if x["name"] == channel]) == 0:
            chan2id.append({"name": channel, "id": processor(channel)})
            Path("chan2id.json").write_text(json.dumps(chan2id))
