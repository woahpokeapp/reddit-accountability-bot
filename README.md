# Reddit Accountability Bot

A Python bot that monitors productivity-focused subreddits to identify users seeking accountability and study support.

## Purpose

This bot helps facilitate timely accountability support in productivity communities by monitoring discussions where users express study intentions or request motivation/accountability partners.

## Features

- Monitors r/productivity, r/pomodoro, r/GetStudying, r/focus
- Detects keywords related to accountability and study requests
- Sends real-time alerts via Slack for manual follow-up
- Tracks seen posts to avoid duplicate notifications
- Read-only monitoring (no automated posting)

## Technical Stack

- Python 3.x
- PRAW (Python Reddit API Wrapper)
- Slack Webhooks for notifications
- Runs on DigitalOcean Droplet

## Usage

The bot operates in read-only mode. When relevant discussions are detected, alerts are sent via Slack. All community engagement happens through manual responses via personal Reddit account, ensuring authentic human interaction rather than automated bot responses.

## Installation
```bash
pip install praw requests
python bot.py
```

## Configuration

Edit `bot.py` and add your:
- Reddit API credentials
- Slack webhook URL
