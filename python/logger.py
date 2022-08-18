import requests, json

def logger(trace_id, span_id, content, timestamp, tenantId, token):
    try:
        log = {"content":content,"trace_id":trace_id, "span_id":span_id, "timestamp":timestamp}
        api = {'Accept': 'application/json; charset=utf-8', 'Content-Type': 'application/json; charset=utf-8', 'Authorization' : "Api-Token {token}".format(token=token)}
        post = requests.post('https://{tenantId}.live.dynatracelabs.com/api/v2/logs/ingest'.format(tenantId=tenantId), headers=api, params={}, data=json.dumps(log))
        post.raise_for_status()
        print(post.status_code)
    except requests.exceptions.Timeout as err:
        print("The request timed out. Couldn't reach - {url}".format(url = url))
        raise SystemExit(err)
    except requests.exceptions.ConnectionError as err:
        print("The URL was malformed - {url}".format(url = url))
        raise SystemExit(err)
    except requests.exceptions.TooManyRedirects as err:
        print("The URL was malformed - {url}".format(url = url))
        raise SystemExit(err)
    except Exception as e:
        print(e)
