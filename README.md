# Time Saver

Utility that alerts each extra hour spent on distracting activities via the notification center.

Requires a Rescue Time API Key.

## How to use

1. Clone this repo
2. `pipenv install`
3. Create a `.env` file in the repo root with your Rescue Time API Key. As follows:

```
RESCUETIME_API_KEY=B63iAa__hHN4YWWfqhZaJe7ifqBz1mxxxx
```

4. Create a cron job to run the `time-saver.sh` script every hour. `crontab -e` to open the crontab.
The rule should look like this:

```
0 * * * * <absolute path to this repo>/time-saver.sh
```
