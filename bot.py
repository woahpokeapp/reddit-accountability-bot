"""
Reddit Accountability Bot
Monitors productivity subreddits for users seeking accountability and study support.
"""

import praw
import requests
import time
import json
from datetime import datetime

# Configuration
REDDIT_CLIENT_ID = "your_client_id_here"
REDDIT_CLIENT_SECRET = "your_client_secret_here"
REDDIT_USER_AGENT = "AccountabilityBot/1.0"

SLACK_WEBHOOK_URL = "your_slack_webhook_url_here"

# Subreddits to monitor
SUBREDDITS = ["productivity", "pomodoro", "GetStudying", "focus"]

# Keywords to detect accountability requests
KEYWORDS = [
    "need accountability",
    "study session",
    "focus timer",
    "pomodoro",
    "need motivation",
    "starting to study",
    "accountability partner",
    "help me focus",
    "need to study",
    "study with me"
]

# File to track seen posts
SEEN_POSTS_FILE = "seen_posts.json"


def load_seen_posts():
    """Load previously seen post IDs from file."""
    try:
        with open(SEEN_POSTS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_seen_posts(seen_posts):
    """Save seen post IDs to file."""
    with open(SEEN_POSTS_FILE, 'w') as f:
        json.dump(seen_posts, f)


def send_slack_notification(post_data):
    """Send notification to Slack about a relevant post."""
    message = {
        "text": f"🎯 Accountability Opportunity Detected!",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Accountability Request"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Subreddit:*\nr/{post_data['subreddit']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Author:*\nu/{post_data['author']}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Title:*\n{post_data['title']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Content Preview:*\n{post_data['preview']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Matched Keywords:* {', '.join(post_data['matched_keywords'])}"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View on Reddit"
                        },
                        "url": post_data['url']
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print(f"✓ Notification sent for post: {post_data['title'][:50]}...")
        else:
            print(f"✗ Failed to send notification: {response.status_code}")
    except Exception as e:
        print(f"✗ Error sending notification: {e}")


def check_for_keywords(text):
    """Check if text contains any of the monitored keywords."""
    text_lower = text.lower()
    matched = [kw for kw in KEYWORDS if kw.lower() in text_lower]
    return matched


def monitor_subreddits():
    """Main monitoring function."""
    print("🤖 Starting Reddit Accountability Bot...")
    print(f"📋 Monitoring subreddits: {', '.join(SUBREDDITS)}")
    print(f"🔍 Watching for {len(KEYWORDS)} keywords")
    print("-" * 60)
    
    # Initialize Reddit API
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    # Load seen posts
    seen_posts = load_seen_posts()
    
    for subreddit_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"\n🔎 Checking r/{subreddit_name}...")
            
            # Check new posts
            for post in subreddit.new(limit=25):
                if post.id in seen_posts:
                    continue
                
                # Check title and selftext for keywords
                combined_text = f"{post.title} {post.selftext}"
                matched_keywords = check_for_keywords(combined_text)
                
                if matched_keywords:
                    # Prepare notification data
                    post_data = {
                        "subreddit": subreddit_name,
                        "author": str(post.author),
                        "title": post.title,
                        "preview": post.selftext[:200] + "..." if len(post.selftext) > 200 else post.selftext,
                        "url": f"https://reddit.com{post.permalink}",
                        "matched_keywords": matched_keywords,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Send notification
                    send_slack_notification(post_data)
                    
                    # Mark as seen
                    seen_posts.append(post.id)
                
        except Exception as e:
            print(f"✗ Error checking r/{subreddit_name}: {e}")
    
    # Save updated seen posts
    save_seen_posts(seen_posts)
    print(f"\n✓ Monitoring cycle complete. Checked {len(SUBREDDITS)} subreddits.")
    print(f"📊 Total posts tracked: {len(seen_posts)}")


def run_bot():
    """Run the bot continuously."""
    CHECK_INTERVAL = 1800  # 30 minutes in seconds
    
    print("=" * 60)
    print("Reddit Accountability Bot - Starting")
    print("=" * 60)
    
    while True:
        try:
            monitor_subreddits()
            print(f"\n⏳ Sleeping for 30 minutes... (next check at {datetime.fromtimestamp(time.time() + CHECK_INTERVAL).strftime('%H:%M:%S')})")
            print("=" * 60)
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user.")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            print("⏳ Waiting 5 minutes before retry...")
            time.sleep(300)


if __name__ == "__main__":
    # Validate configuration
    if REDDIT_CLIENT_ID == "your_client_id_here":
        print("⚠️  Please configure your Reddit API credentials in the script!")
        print("   Get them from: https://www.reddit.com/prefs/apps")
    elif SLACK_WEBHOOK_URL == "your_slack_webhook_url_here":
        print("⚠️  Please configure your Slack webhook URL!")
        print("   Get it from: https://api.slack.com/apps")
    else:
        run_bot()
      Add main bot script
