from importlib.resources import files


def path_branding(name: str) -> str:
    return str(files("portent.assets.branding").joinpath(name))
