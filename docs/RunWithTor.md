# Running with Tor and Privoxy

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

