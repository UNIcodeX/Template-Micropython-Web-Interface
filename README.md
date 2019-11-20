# Template-Micropython-Web-Interface

This is a template for running an asynchronous web interface on a microcontroller running Micropython. May also work on CircuitPython (untested).

There are examples for:
  - scheduling / running an asynchronous coroutine. The example periodically frees RAM.
  - Serving a main page at `/` which
    - uses Javascript to update current amount of free RAM,
    - and provides a button to toggle the state of a pin.
  - Serving static as well as on-the-fly JSON data at `/json/`, `/toggle_2/`, and `/free_mem/`.
  