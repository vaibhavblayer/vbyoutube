import click
from .youtubeuploader import YouTubeUploader
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# OAuth 2.0 scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube',  # Added for full access
    'https://www.googleapis.com/auth/youtubepartner'  # Added for education metadata
]
# Update to use fixed path in home directory
CLIENT_SECRETS_FILE = os.path.expanduser('~/.youtube/client_secret.json')


def read_file(file_path):
    """Reads the content of a file."""
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise click.FileError(file_path, "File not found.")
    except Exception as e:
        raise click.ClickException(f"Error reading file {file_path}: {e}")


def get_credentials():
    """Get valid user credentials from storage or create new ones."""
    # Store credentials in the .youtube directory
    token_file = os.path.expanduser('~/.youtube/token.json')

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(token_file), exist_ok=True)

    credentials = None
    # Try to load existing credentials
    if os.path.exists(token_file):
        try:
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
                token_file, SCOPES)
        except Exception:
            # If token is invalid, remove it and proceed with new authentication
            os.remove(token_file)
            credentials = None

    # If no valid credentials available, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
            credentials = flow.run_local_server(
                port=8080,
                redirect_uri_port=8080,
                open_browser=True,
                access_type='offline',
                prompt='consent'
            )
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(credentials.to_json())

    return credentials


@click.command()
@click.option(
    '-m',
    '--metadata',
    type=click.Path(exists=True),
    help='JSON file containing video metadata',
    required=True
)
@click.option(
    '-p',
    '--privacy',
    type=click.Choice(
        ['private', 'public', 'unlisted'], case_sensitive=False),
    default='private',
    help='Video privacy status (default: private)'
)
def upload(metadata, privacy):
    """Upload a video to YouTube with metadata."""
    try:
        credentials = get_credentials()
        uploader = YouTubeUploader(credentials)

        upload_response = uploader.upload(
            metadata_file=metadata,
            privacy_status=privacy.lower()
        )

    except Exception as e:
        raise click.ClickException(f"An error occurred: {str(e)}")


if __name__ == '__main__':
    upload()
