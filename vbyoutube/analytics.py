import click
from tabulate import tabulate
from datetime import datetime
from googleapiclient.discovery import build


@click.command()
def stats():
    """Show channel statistics (subscribers, total views, video count)."""
    try:
        youtube = build_youtube()

        # Get channel statistics
        request = youtube.channels().list(
            part="statistics",
            mine=True
        )
        response = request.execute()

        if not response['items']:
            click.echo("No channel found!")
            return

        stats = response['items'][0]['statistics']

        # Format the data
        data = [
            ["Subscribers", f"{int(stats['subscriberCount']):,}"],
            ["Total Views", f"{int(stats['viewCount']):,}"],
            ["Total Videos", stats['videoCount']]
        ]

        click.echo("\n=== Channel Statistics ===")
        click.echo(tabulate(data, tablefmt="simple"))

    except Exception as e:
        click.echo(f"Error fetching stats: {e}")


@click.command()
@click.option('--sort-by',
              type=click.Choice(['views', 'likes', 'comments', 'date']),
              default='date',
              help='Sort videos by metric')
@click.option('--limit',
              type=int,
              default=10,
              help='Number of videos to show')
@click.option('--top',
              is_flag=True,
              help='Show top videos instead of recent ones')
def videos(sort_by='date', limit=10, top=False):
    """List videos with their metrics."""
    try:
        youtube = build_youtube()

        # First get channel ID
        channels_response = youtube.channels().list(
            part="id",
            mine=True
        ).execute()

        if not channels_response['items']:
            click.echo("No channel found!")
            return

        channel_id = channels_response['items'][0]['id']

        # Get all videos
        videos = []
        next_page_token = None

        while True:
            request = youtube.search().list(
                part="id",
                channelId=channel_id,
                maxResults=50,
                type="video",
                pageToken=next_page_token,
                order="relevance" if top else "date"
            )
            response = request.execute()

            if not response.get('items'):
                break

            video_ids = [item['id']['videoId'] for item in response['items']]

            # Get detailed stats for these videos
            stats_request = youtube.videos().list(
                part="snippet,statistics",
                id=','.join(video_ids)
            )
            stats_response = stats_request.execute()

            for item in stats_response['items']:
                videos.append({
                    'title': item['snippet']['title'],
                    'views': int(item['statistics'].get('viewCount', 0)),
                    'likes': int(item['statistics'].get('likeCount', 0)),
                    'comments': int(item['statistics'].get('commentCount', 0)),
                    'date': datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token or (not top and len(videos) >= limit):
                break

        if not videos:
            click.echo("No videos found!")
            return

        # Sort videos
        if top:
            sort_key = {
                'views': lambda x: x['views'],
                'likes': lambda x: x['likes'],
                'comments': lambda x: x['comments'],
                'date': lambda x: x['date']
            }[sort_by]
            videos.sort(key=sort_key, reverse=True)
        else:
            videos.sort(key=lambda x: x['date'], reverse=True)

        # Format for display
        table_data = []
        for video in videos[:limit]:
            table_data.append([
                video['title'][:50] +
                ('...' if len(video['title']) > 50 else ''),
                f"{video['views']:,}",
                f"{video['likes']:,}",
                f"{video['comments']:,}",
                video['date'].strftime('%Y-%m-%d')
            ])

        headers = ['Title', 'Views', 'Likes', 'Comments', 'Published']

        if top:
            click.echo(f"\n=== Top {limit} Videos (sorted by {sort_by}) ===")
        else:
            click.echo(f"\n=== Latest {limit} Videos ===")
        click.echo(tabulate(table_data, headers=headers, tablefmt="simple"))

    except Exception as e:
        click.echo(f"Error fetching videos: {e}")


def build_youtube():
    """Build YouTube service from credentials."""
    from .upload import get_credentials
    credentials = get_credentials()
    return build("youtube", "v3", credentials=credentials)
