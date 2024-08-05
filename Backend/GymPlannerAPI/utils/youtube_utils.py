from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_youtube_video_url(query, api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            maxResults=1
        )
        response = request.execute()

        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f'https://www.youtube.com/watch?v={video_id}'
        return None
    except HttpError as e:
        error_content = e.content.decode('utf-8')
        if 'quotaExceeded' in error_content:
            print("Quota exceeded. Please try again later.")
            raise Exception("Quota exceeded!")
        else:
            print(f"An HTTP error occurred: {e}")
            raise Exception("An HTTP error occurred!")
