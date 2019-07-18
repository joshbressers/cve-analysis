# cve-analysis
Tools for conducting analysis of CVE data in Elasticsearch

## Quckstart:
Download Elasticsearch and Kibana from elastic.co
You will need verison 7 or above

Start them (basically ./bin/elasticsearch and ./bin/kibana from the
respective directories).

Run `get-cve-json.sh` to download the CVE data from NVD  
Run `update-es.sh` to import the CVE data into Elasticsearch

You rerun the above commands to update your data whenever needed.

Now navigate your web browser to http://localhost:5601

Now go to the Management area. Click "Saved Objects". In the upper right of the
screen you'll see "Import". Import the cve-kibana.ndjson file.

Now you should have some basic visualizations and a dashboard to look at.
Happy hunting.
