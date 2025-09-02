# Opportunity Notifier

Python script to report new jobs, placements and events on various websites.

## Features

Currently checks:
- [x] [Uptree](https://uptree.co/)
- [ ] [the-trackr.com](https://the-trackr.com/trackers/)

## Configuration

`.env` should contain three keys:
- `TO_EMAIL`: the email address to send the updates to
- `FROM_EMAIL`: the email address from which the updates are sent
- `FROM_PASS`: an application password for `FROM_EMAIL`

## Usage

Run periodically (e.g. cron, systemd timer), allowing it to check for new updates.
