# Shutdown Signal
## A simplified method using signal handling to ensure a clean shutdown
## for continuous processes

### Basic usage

```python
# Typical Workflow
while True:
    # do work

# Proposed Workflow
from palantiri.util import ShutdownHandler
handle = ShutdownHandler(signal_number)
while handle.isalive:
    # do work
```

### A contrived example

```python
import time
from palantiri.util import ShutdownHandler

# install the handler for signals
handle = ShutdownHandler(2)      # SIGINT
handle.add_signal(1)             # SIGHUP

while handle.isalive:
    print("Hello!")
    time.sleep(1)     # user presses Ctrl+C here
    print("World!")   # "World!" will still print
    time.sleep(1)
```
