## Web Crawler for the Human Trafficking Project

This is the core web crawler that will be used for the human trafficking project

## Building

### Get the code

#### Clone or [Fork](http://doc.gitlab.com/ee/workflow/forking_workflow.html)

```bash
  # clone
  git clone git@gitlab.com:danlrobertson/palantiri.git     # ssh
  # or
  git clone https://gitlab.com/danlrobertson/palantiri.git # http
  # build
  python setup.py install
  # test
  python setup.py test
```

## Running

```bash
  python search.py -[cgb] <site> <optional arguments>"
```
  - `-[cgb]` defines the domain name. E.g. `-b` for <area>.backpage.com
  - `site` takes a comma separated list which defines the subdirectories to search. E.g. BusinessServices,ComputerServices
  - optional arguments are defined with `--<argument> value`

A more detailed list may be obtained by running `python search.py --help`. [example.py](example.py) is an example of what
we currently run. The run time for the program is around 30 minutes.

## Running with tor and privoxy

- Generate a hashed password for [tor](https://www.torproject.org/)

  ```
    tor --hash-password mypassword
  ```

- Add the password hash and what should be the default, `ControlPort 9051`, to your `/etc/tor/torrc`. E.g.

  ```
    ## The port on which Tor will listen for local connections from Tor
    ## controller applications, as documented in control-spec.txt.
    ControlPort 9051
    ## If you enable the controlport, be sure to enable one of these
    ## authentication methods, to prevent attackers from accessing it.
    HashedControlPassword 16:4CAEC75092BE933060809DCD955754143613F9C418BEEF6F569D59F7DC
  ```
  Note: If you copy-paste the above, make sure to replace the `HashedControlPassword` value with the password hash
        genterated from step 1. The value displayed is a dummy example hash. You will be prompted for the password
        you generated the hash for by the `search.py` or `example.py` script.

- [Privoxy](http://www.privoxy.org/) to route all traffic through tor, by adding the following to your `/etc/privoxy/config`

```
  forward-socks5 / localhost:9050 .
```

- Restart both tor and privoxy, and the script should do the rest for you. If you are interested in how that is accomplished,
  check out [engine.py](src/core/engine.py) and the class `TorEngine`.

## Dependencies

- [Python 3.4](https://www.python.org/)
- [Selenium 2.47.1](https://github.com/seleniumhq/selenium)
- [Tor 2.7.4](https://www.torproject.org/)
- [Stem 1.4.1](https://stem.torproject.org/)
- [Privoxy 3.0.23](http://www.privoxy.org/)

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more information about contributing to this project

## Questions

Please checkout our [slack](https://atl-data-scientists.slack.com) if you are already a part of the project or contact @danlrobertson if you have any questions.