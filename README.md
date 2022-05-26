# Example of alerting system promise type

## Files

* `alerting_system/test.cf` - the policy which uses the alerting system promise type.
* `alerting_system/alerting_system.py` the module, written in python, uses the `cfengine.py` python library
* `alerting_system/enable.cf` policy snippet needed to enable the promise type.
  This is where you can point it to a different python binary.
* `alerting_system/server.py` a small python server to test that the module sent HTTP requests.
* `cfbs.json` CFEngine Build project file, used by `cfbs` CLI, defines how we build a policy set from multiple modules.
  Might be interesting to read through even if you are not using it.

The library for creating promise types in Python, `cfengine.py`, can be found here:

https://build.cfengine.com/modules/library-for-promise-types-in-python/

## Build and deploy with tooling

If you are using `cfbs` and `cf-remote`, do:

```
$ cfbs build && cf-remote deploy
```

(Requires `cfbs 2.2.0` or newer).

## Adding to a policy set manually

Assuming you are using the Masterfiles Policy Framework(MPF) in `/var/cfengine/masterfiles`:

```
$ mkdir -p /var/cfengine/masterfiles/modules/promises/
$ curl https://raw.githubusercontent.com/cfengine/modules/master/libraries/python/cfengine.py > /var/cfengine/masterfiles/modules/promises/cfengine.py
$ cp alerting_system/alerting_system.py /var/cfengine/masterfiles/modules/promises/
$ cat alerting_system/enable.cf >> /var/cfengine/masterfiles/services/init.cf
$ cp test.cf /var/cfengine/masterfiles/services/autorun/
```

If you are not using `autorun`, you need to add `test.cf` to inputs and the bundle `test_alerting_system` to your bundle sequnce, or enable `autorun` in `/var/cfengine/masterfiles/def.json`:

```json
{
  "classes": {
    "services_autorun": ["any"]
  }
}
```

## Links

* [Custom promise type specification / documentation](https://docs.cfengine.com/docs/master/reference-promise-types-custom.html) - Includes details on how the protocol works and how you could implement it in another language
* [CFEngine Build](https://build.cfengine.com/) - The website where we have all kinds of modules, including promise types, inventory data and reports, security hardening, etc.
* [Custom promise types available on CFEngine Build](https://build.cfengine.com/modules/?page=1&tag=promise-type)
* [New getting started tutorial series](https://docs.cfengine.com/docs/master/guide-getting-started-with-cfengine-build.html) - Part 5 is about developing modules
