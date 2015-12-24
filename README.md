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
