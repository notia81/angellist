import StringIO
import json
import socket
import urllib

import socks  # SockiPy module
import stem.process
from stem.util import term

SOCKS_PORT = 7000
TWITTER_API_URL = "https://api.angel.co/1/users/%i"

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def query(url):
  """
  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
  """

  try:
    return urllib.urlopen(url).read()
  except:
    return "Unable to reach %s" % url


def poll_twitter_feed(user_id, tweet_count):
  """
  Polls Twitter for the tweets from a given user.
  """

  api_url = TWITTER_API_URL % (user_id, tweet_count)

  try:
    api_response = urllib.urlopen(api_url).read()
  except:
    raise IOError("Unable to reach %s" % api_url)

  #return json.loads(api_response)
  return api_response

def open_tor ():
  tor_process = stem.process.launch_tor_with_config(
    config = {
      'SocksPort': str(SOCKS_PORT),
      'ExitNodes': '{us}',
    },
  )


# try:
#   for index, tweet in enumerate(poll_twitter_feed('ioerror', 3)):
#     print "%i. %s" % (index + 1, tweet["created_at"])
#     print tweet["text"]
#     print
# except IOError, exc:
#   print exc
# finally:
#   tor_process.kill()  # stops tor

for x in range (0,10):
  open_tor()
  print term.format("\nChecking our endpoint:\n", term.Attr.BOLD)
  print term.format(query("https://www.atagar.com/echo.php"), term.Color.BLUE)
  tor_process.kill()  # stops tor
