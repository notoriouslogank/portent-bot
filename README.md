# Portent

Portent is a Discord bot built **slash-first** with `discord.py` 2.x - the successor to Harbinger.

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -U -e .[dev]
cp .env.example .env # fill TOKEN, DEV_GUILD_ID, LOG_LEVEL, SYNC_MODE
make dev             # run with guild sync; try /ping in your dev server
```

## Structure
src/portent/
    bot.py              # entrypoint
    config.py           # env loader
    logging_setup.py    # Rich console + rotating file
    command_sync.py     # guild/global sync helper
    cogs/               # modular commands
tests/

## Dev Notes
- Lint/format: `make fmt` / `make lint`
- Tests: `make test`
- Publish slash commands globally: `make sync-global` (after tagging a release)

## Versioning
This repo uses setuptools-scm -> version = latest Git tag.
- Tag a release: `git tag v0.1.0 && git push origin v0.1.0`
- See version at runtime:
    `import importlib.metadata as im; print(im.version("portent"))`

## License
MIT - see `LICENSE`
