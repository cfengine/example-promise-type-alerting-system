import sys
import os
import requests
from cfengine import PromiseModule, ValidationError, Result

class AlertingSystemPromiseTypeModule(PromiseModule):
    def log(self, message, level="info"):
        log_file = "/var/cfengine/alerting_log"
        if not os.path.exists(log_file):
            os.system("touch " + log_file)
        if not os.path.exists(log_file):
            self.log_error("Failed to create log file")
            return Result.NOT_KEPT

        with open(log_file, "r") as f:
            if message in f.read():
                return Result.REPAIRED

        with open(log_file, "a") as f:
            f.write(message + "\n")
            # requests.post("http://127.0.0.1:5000/", data = str({"message": message}))
            self._log(level, message)
        return Result.KEPT

    def validate_promise(self, promiser, attributes):
        if not promiser:
            raise ValidationError(f"Promiser must be non-empty")
        if "component" not in attributes:
            raise ValidationError("Missing required attribute 'component'")

        if "severity" in attributes and attributes["severity"] not in ("info", "error"):
            raise ValidationError("Invalid severity: " + attributes["severity"])

    def evaluate_promise(self, promiser, attributes):
        message = promiser
        component = attributes["component"]
        severity = attributes.get("severity", "unknown")
        message = f"{message} - {component} - {severity}"

        return self.log(message, "info" if severity == "unknown" else severity)


if __name__ == "__main__":
    AlertingSystemPromiseTypeModule().start()
