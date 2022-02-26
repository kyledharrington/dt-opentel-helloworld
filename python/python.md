##   Dynatrace python opentelemetry setup

1. Please see the [Instrument Python applications with OpenTelemetry](https://www.dynatrace.com/support/help/extend-dynatrace/opentelemetry/opentelemetry-ingest/opent-python) link for prerequisites

1. Please ber sure to install the following pip dependencies in your environment

    - please note, not all of these dependencies are needed for Dynatrace instrumentation, but are required for the [Open Telemetry Example Quick Start](https://opentelemetry-python.readthedocs.io/en/latest/getting-started.html#instrumentation-example-with-flask)

1. Run the following:
    ```
    pip install opentelemetry-api
    pip install opentelemetry-sdk
    pip install opentelemetry-instrumentation-requests
    pip install opentelemetry-instrumentation-flask
    pip install opentelemetry-instrumentation-requests
    pip install opentelemetry-exporter-otlp
    pip install opentelemetry-exporter-otlp-proto-http
    ``` 

1. Once all dependencies are installed you will need to append the python_flask_example.py


1. Then you can run the flask app by running:

    ```
    python python_flask_example.py
    ```

1. The flask application will now serve traffic on port 5000
1. Send traffic via web browser or GET request to:
    ```
    http://localhost:5000/
    ```
1. This will generate spans via opentelemetry and send this data to Dynatrace