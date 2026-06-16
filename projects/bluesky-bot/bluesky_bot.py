import os
import time
from atproto import Client


def get_client():
    username = os.getenv('BLUESKY_USERNAME')
    password = os.getenv('BLUESKY_PASSWORD')

    if not username or not password:
        raise RuntimeError(
            'Set BLUESKY_USERNAME and BLUESKY_PASSWORD as environment variables before running this script.'
        )

    client = Client()
    profile = client.login(username, password)
    print(f'Logged in as {profile.handle}')
    return client, profile


def print_timeline(client, limit=30):
    timeline = client.get_timeline(limit=limit)
    for item in timeline.feed:
        text = getattr(item.post.record, 'text', '')
        print(text)
    return timeline.feed


def like_matching_posts(client, feed, search_string, max_likes=2):
    likes = 0
    for item in feed:
        text = getattr(item.post.record, 'text', '')
        if search_string.lower() in text.lower():
            client.like(item.post.uri, item.post.cid)
            likes += 1
            print(f'Liked post containing: {search_string}')
            if likes >= max_likes:
                break
    return likes


def follow_matching_display_name(client, profile, display_name):
    followers = client.get_followers(profile.did)
    followed = 0

    while followers.followers:
        follower = followers.followers.pop()
        if follower.display_name == display_name:
            client.follow(follower.did)
            followed += 1
            print(f'Followed {display_name}')
        time.sleep(0.2)

    return followed


if __name__ == '__main__':
    client, profile = get_client()
    feed = print_timeline(client)
    like_matching_posts(client, feed, search_string='Final Fantasy', max_likes=2)
