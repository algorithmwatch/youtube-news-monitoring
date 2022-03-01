# Examining YouTube Auto-generated News Playlists

## Data gathering

Check: <https://github.com/algorithmwatch/harke-puppeteer#monitoring>

Crontab:

```bash
*/7 * * * * /root/run_yt_monitor.sh
```

## Download data

```bash
rsync -vr awlab1:/root/yt-playlists-data/ data/
```
