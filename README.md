## Web Crawler for the Human Trafficking Project

This is the core web crawler that will be used for the human trafficking project

## Building

### Get the code

#### Clone or [Fork](http://doc.gitlab.com/ee/workflow/forking_workflow.html)

```bash
  # clone
  git clone git@gitlab.com:atl-ads/palantiri.git     # ssh
  # or
  git clone https://gitlab.com/atl-ads/palantiri.git # http
  # build
  cd palantiri
  
  # Make sure you are using python3, then use pip to install dependencies
  # The anaconda package and version manager is easiest way to do this https://www.continuum.io/downloads
  pip install -e .

  # test
  python setup.py test
```

## Running

### Start a MongoMD or PostgreSQL Server

Install MongoDB or PostgreSQL and use the
[`PostgreSQLDump`](https://gitlab.com/atl-ads/palantiri/blob/master/src/core/datahandler.py#L78) or
[`MongoDBDump`](https://gitlab.com/atl-ads/palantiri/blob/master/src/core/datahandler.py$L152) class
to store the collected data in a database.


### Scrape
```bash
  python search.py -[cgb] <site> <optional arguments>"
```
  - `-[cgb]` defines the domain name. E.g. `-b` for <area>.backpage.com
  - `site` takes a comma separated list which defines the subdirectories to search. E.g. BusinessServices,ComputerServices
  - optional arguments are defined with `--<argument> value`

A more detailed list may be obtained by running `python search.py --help`. [example.py](example.py) is an example of what
we currently run. The run time for the program is around 30 minutes.

## More Documentation

- [Running with Tor and Privoxy](docs/RunWithTor.md)
- [Handling Signals to Shutdown Process](docs/ShutdownSignal.md)

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
