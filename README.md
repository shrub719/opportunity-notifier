# Uptree Checker

Python script to report new jobs, placements and events on [Uptree](https://uptree.co/).

## Configuration

`.env` should contain three keys:
- `TO_EMAIL`: the email address to send the updates to
- `FROM_EMAIL`: the email address from which the updates are sent
- `FROM_PASS`: an application password for `FROM_EMAIL`

## Usage

Run periodically, allowing it to check for new updates.

The program stores a log of past events in `events.json`.
