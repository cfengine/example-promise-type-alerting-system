import sys
import os
import requests
from cfengine import PromiseModule, ValidationError, Result


def sh(cmd):
    # TODO: Using something like subprocess is more flexible than os.system
    output = os.system(cmd)
    return (0, output)


class AlertingSystemPromiseTypeModule(PromiseModule):
    def log(self, component, message):
        """Log a message to cf-agent / file / HTTP only

        Only log if not already present in log file.
        Returns true if we did log something, false otherwise.
        """
        log_file = "/var/cfengine/alerting_log"

        # Create file if it doesn't exist: (TODO: don't use shell for this)
        if not os.path.exists(log_file):
            sh("touch " + log_file)

        # The full message we want to log:
        message = f"{component} : {message}"

        # Check if it's already logged in the log file:
        with open(log_file, "r") as f:
            if message in f.read():
                # Log message already there, do nothing:
                return False

        # Not logged, let's do it:
        with open(log_file, "a") as f:
            # Log to file:
            f.write(message + "\n")
            # And to HTTP API:
            data = str({"message": message, "component": component})
            requests.post(
                "http://127.0.0.1:5000/",
                data=data,
            )
            # And to the agent / terminal:
            self.log_info(message)

            # For an alternative to requests which is not another dependency,
            # see urllib: https://docs.python.org/3/library/urllib.request.html

            # We could also use curl:
            # sh(f"curl -X POST --data '{data}' 'http://127.0.0.1:5000/'")
        return True

    def validate_promise(self, promiser, attributes):
        if not promiser:
            raise ValidationError(f"Promiser must be non-empty")
        if not "message" in attributes:
            raise ValidationError(f"Missing message attribute")

    def evaluate_promise(self, promiser, attributes):
        component = promiser
        message = attributes["message"]

        # Important: the module should check whether changes are necessary
        #            and return KEPT if everything was already as desired
        if self.log(component, message):
            # The log method did log something
            return Result.REPAIRED
        # Already logged, no changes made this time
        return Result.KEPT


if __name__ == "__main__":
    AlertingSystemPromiseTypeModule().start()
