import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    Handles standard, shortened, and embed URLs.
    """
    video_id = None
    if "youtube.com/watch?v=" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0]
    elif "youtube.com/embed/" in url:
        video_id = url.split("embed/")[1].split("?")[0]
    return video_id

def get_transcript(video_id, preferred_language='en'):
    """
    Fetches and formats the transcript for a given video ID.
    Prioritizes the preferred language.
    """
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id=video_id)

        # Search for the preferred language transcript.
        target_transcript = None
        # The list needs to be iterated over to find the right language
        for transcript in transcript_list:
            if transcript.language_code.lower() == preferred_language:
                target_transcript = transcript
                break
        
        # If the preferred language is not found, fall back to the first available transcript.
        if not target_transcript:
            # Create a new iterator
            transcript_iterator = iter(transcript_list)
            target_transcript = next(transcript_iterator)

        # Fetch and format the transcript.
        transcript_text = " ".join([item.text for item in target_transcript.fetch()])
        return transcript_text
    except Exception as e:
        return f"Error: Could not retrieve transcript. Please check the following:\n- The video URL is correct.\n- The video has a transcript available.\n- You have an active internet connection.\nDetails: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcript.py <youtube_video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    video_id = get_video_id(video_url)

    if not video_id:
        print("Error: Invalid YouTube URL provided.")
        sys.exit(1)

    # The get_transcript function now handles language preference.
    transcript_text = get_transcript(video_id)
    print(transcript_text)
