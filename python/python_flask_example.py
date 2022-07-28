# flask_example.py
import flask
import requests
from fibonacci import fibonacci
from logger import logger

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import sampling
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from configparser import ConfigParser
from pathlib import Path
from opentelemetry import trace as OpenTelemetry
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

resource = Resource.create({
    "service.name": "dt-python-opentel", #TODO Replace with the name of your application
    "service.version": "1.0.0" #TODO Replace with the version of your application
})

for name in ["dt_metadata_e617c525669e072eebe3d0f08212e8f2.properties", "/var/lib/dynatrace/enrichment/dt_metadata.properties"]:
    try:
        config = ConfigParser()
        with open(Path(name).read_text()) as f:
            config.read_string('[_]\n' + f.read())
        resource.update(config['_'])
        break
    except:
        pass

OpenTelemetry.set_tracer_provider(TracerProvider(resource=resource, sampler=sampling.ALWAYS_ON))

OpenTelemetry.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(
        endpoint="https://<TENANTID>.live.dynatrace.com/api/v2/otlp/v1/traces", #TODO Replace <TENANT> with your unique  tenant id:
        headers={
            "Authorization": "Api-Token <TOKEN>" #TODO Replace <TOKEN> with your API Token scoped with "Ingest OpenTelemetry traces"
        },
    ))
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@app.route("/")
def hello():
    with tracer.start_as_current_span("example-request"):
        requests.get("http://www.example.com")
    return "hello"

@app.route("/calculate-fib")
def calculateFib():
    current_span = trace.get_current_span()
    n = random.randint(1,20)
    current_span.set_attribute("fibonacci.number",n)
    fib = fibonacci(n)
    logger(hex(current_span.context.trace_id)[2:], hex(current_span.context.span_id)[2:], "The calculate-fib n: {n}, fib: {fib}".format(n=n,fib=fib), current_span.start_time)
    return "hello calculate-fib n: {n}, fib: {fib}. Trace_id:{trace_id} and Span_id:{span_id}".format(n=n,fib=fib, trace_id=hex(current_span.context.trace_id)[2:], span_id=hex(current_span.context.span_id)[2:])

app.run(port=5000)