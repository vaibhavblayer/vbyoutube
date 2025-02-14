# vbyoutube

A command-line tool for managing YouTube content, designed for educational content creators. It helps streamline video uploads, updates, and analytics while maintaining organized content across devices.

## Installation

pip install vbyoutube

## Directory Structure & Metadata

Your content should follow this structure:

youtube_content/
└── 2024/
    └── february/
        └── video_name/
            ├── video.mov
            ├── description.txt
            └── thumbnails/
                └── thumbnail.png

With metadata.json in the video directory:

{
    "title": "Video Title",
    "files": {
        "video": "/path/to/video.mov",
        "thumbnail": "/path/to/thumbnail.png",
        "description": "/path/to/description.txt"
    },
    "tags": ["tag1", "tag2"],
    "language": {
        "video": "en",
        "title_and_description": "en"
    },
    "recording": {
        "date": "2024-02-14",
        "location": "Mumbai"
    },
    "license": "Standard YouTube License",
    "embedding": true,
    "education": {
        "type": "Problem walkthrough",
        "academic_system": "India",
        "level": "Intermediate",
        "exam": "JEE Advanced"
    }
}

## Commands

### Upload

# Upload new video
vbyoutube upload -m path/to/metadata.json

### Update

# Update existing video
vbyoutube update -m path/to/metadata.json

### Sync

# Auto-detect sync direction
vbyoutube sync

# Force direction
vbyoutube sync --force-direction to-ssd
vbyoutube sync --force-direction to-local

# Custom paths
vbyoutube sync -s /path/to/ssd -d /path/to/local

### Analytics

# Channel statistics
vbyoutube stats

# Latest videos (default)
vbyoutube videos

# Latest 20 videos
vbyoutube videos --limit 20

# Top performing videos
vbyoutube videos --top --sort-by views
vbyoutube videos --top --sort-by likes
vbyoutube videos --top --sort-by comments

## Features

- **Upload & Update**
  - Metadata-driven uploads
  - Automatic thumbnail setting
  - Education metadata support
  - Returns video URL
  - Update existing videos

- **Smart Sync**
  - Timestamp-based direction
  - Excludes video files
  - Handles Mac-specific files
  - Default paths configurable

- **Analytics**
  - Channel statistics
  - Video performance metrics
  - Sort by views/likes/comments
  - Recent uploads tracking

## First Time Setup

1. Create OAuth 2.0 credentials in Google Cloud Console
2. Enable YouTube Data API
3. Run any command to trigger authentication
4. Follow browser prompts to authorize

## Dependencies
- click
- google-api-python-client
- google-auth-oauthlib
- tqdm
- tabulate

## License
MIT License

## Author
Vaibhav Blayer
