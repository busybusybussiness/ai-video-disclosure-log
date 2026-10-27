# ai-video-disclosure-log

Free, offline command-line tool that writes one Markdown AI-use disclosure record per video, as a checklist for your own files.

`aidisc.py` writes one record per video: which AI tools were used, whether AI altered existing footage or audio, whether the result could be mistaken for real people, places or events, and whether the disclosure step is still pending. It refuses to overwrite an existing record and never touches the network (Python standard library only).

## Usage

```
python aidisc.py --out records --video-id ep-001 --title "Rain loop" --tool "SDXL 1.0 local" --ai-used --realistic
```

Output: `records/ep-001.md`. Re-running with the same ID is refused (exit 2). When a realistic AI video has no disclosure marked as applied, the record shows an ACTION line.

| Flag | Meaning |
|---|---|
| `--ai-used` | AI generated or meaningfully altered some content |
| `--altered` | AI altered existing footage/audio (vs generated fresh) |
| `--realistic` | the AI content could be mistaken for real people, places or events |
| `--disclosure-applied` | you set the AI-use disclosure in the upload form |

## What it does NOT do
- It does not check or certify that any video complies with any platform policy.
- It is not legal advice. Every record says so.
- It does not upload anything or read any account.

The rule in `required_disclosure()` paraphrases YouTube's public help page, [Disclosing use of GenAI content](https://support.google.com/youtube/answer/14328491) (re-checked 2026-10-26). Re-check the live page yourself; platform rules change.

## Tests

```
python -m pytest test_aidisc.py
```

## License
MIT. Written with AI assistance and reviewed by tests.
