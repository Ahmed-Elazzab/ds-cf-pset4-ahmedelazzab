"""Sample module within helloworld package."""

from requests import get


def hello_world(remote: bool):
    """Say hello world, possibly with a quote from the Internet.

    Args:
        remote: if true - gets QOTD from Internet, otherwise uses fixed offline quote

    Returns:
        The QOTD (also printed on screen)
    """
    if remote:
        qotd = get("https://quotes.rest/qod").json()["contents"]["quotes"][0]["quote"]
    else:
        qotd = "Père Noël ne sois pas triste si tu tombes si tu glisses"
    print(f"Quote of the Day from the Web:\n\n{qotd}")  # noqa
    return qotd
