import logging

import boto3
import pandas as pd
import json

import awswrangler as wr


logging.getLogger("awswrangler").setLevel(logging.DEBUG)

# TODO: create test_infra for opensearch
OPENSEARCH_DOMAIN = 'search-es71-public-z63iyqxccc4ungar5vx45xwgfi.us-east-1.es.amazonaws.com'  # change to your domain
OPENSEARCH_DOMAIN_FGAC = 'search-os1-public-urixc6vui2il7oawwiox2e57n4.us-east-1.es.amazonaws.com'
BUCKET = 'mentzera'

inspections_documents = [
{"business_address":"315 California St","business_city":"San Francisco","business_id":"24936","business_latitude":"37.793199","business_location":{"lon": -122.400152,"lat": 37.793199},"business_longitude":"-122.400152","business_name":"San Francisco Soup Company","business_postal_code":"94104","business_state":"CA","inspection_date":"2016-06-09T00:00:00.000","inspection_id":"24936_20160609","inspection_score":77,"inspection_type":"Routine - Unscheduled","risk_category":"Low Risk","violation_description":"Improper food labeling or menu misrepresentation","violation_id":"24936_20160609_103141"},
{"business_address":"10 Mason St","business_city":"San Francisco","business_id":"60354","business_latitude":"37.783527","business_location":{"lon": -122.409061,"lat": 37.783527},"business_longitude":"-122.409061","business_name":"Soup Unlimited","business_postal_code":"94102","business_state":"CA","inspection_date":"2016-11-23T00:00:00.000","inspection_id":"60354_20161123","inspection_type":"Routine", "inspection_score": 95},
{"business_address":"2872 24th St","business_city":"San Francisco","business_id":"1797","business_latitude":"37.752807","business_location":{"lon": -122.409752,"lat": 37.752807},"business_longitude":"-122.409752","business_name":"TIO CHILOS GRILL","business_postal_code":"94110","business_state":"CA","inspection_date":"2016-07-05T00:00:00.000","inspection_id":"1797_20160705","inspection_score":90,"inspection_type":"Routine - Unscheduled","risk_category":"Low Risk","violation_description":"Unclean nonfood contact surfaces","violation_id":"1797_20160705_103142"},
{"business_address":"1661 Tennessee St Suite 3B","business_city":"San Francisco Whard Restaurant","business_id":"66198","business_latitude":"37.75072","business_location":{"lon": -122.388478,"lat": 37.75072},"business_longitude":"-122.388478","business_name":"San Francisco Restaurant","business_postal_code":"94107","business_state":"CA","inspection_date":"2016-05-27T00:00:00.000","inspection_id":"66198_20160527","inspection_type":"Routine","inspection_score":56 },
{"business_address":"2162 24th Ave","business_city":"San Francisco","business_id":"5794","business_latitude":"37.747228","business_location":{"lon": -122.481299,"lat": 37.747228},"business_longitude":"-122.481299","business_name":"Soup House","business_phone_number":"+14155752700","business_postal_code":"94116","business_state":"CA","inspection_date":"2016-09-07T00:00:00.000","inspection_id":"5794_20160907","inspection_score":96,"inspection_type":"Routine - Unscheduled","risk_category":"Low Risk","violation_description":"Unapproved or unmaintained equipment or utensils","violation_id":"5794_20160907_103144"},
{"business_address":"2162 24th Ave","business_city":"San Francisco","business_id":"5794","business_latitude":"37.747228","business_location":{"lon": -122.481299,"lat": 37.747228},"business_longitude":"-122.481299","business_name":"Soup-or-Salad","business_phone_number":"+14155752700","business_postal_code":"94116","business_state":"CA","inspection_date":"2016-09-07T00:00:00.000","inspection_id":"5794_20160907","inspection_score":96,"inspection_type":"Routine - Unscheduled","risk_category":"Low Risk","violation_description":"Unapproved or unmaintained equipment or utensils","violation_id":"5794_20160907_103144"}
]

def test_connection():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    print(client.info())


# def test_fgac_connection():
#     client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN_FGAC,
#                                    fgac_user='admin',
#                                    fgac_password='SECRET')
#     print(client.info())


def test_create_index():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.create_index(
        client,
        index='test-index1',
        mappings={
            'properties': {
                'name': {'type': 'text'},
                'age': {'type': 'integer'}
            }
        },
        settings={
            'index': {
                'number_of_shards': 1,
                'number_of_replicas': 1
            }
        }
    )
    print(response)


def test_delete_index():
    index = 'test_delete_index'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    wr.opensearch.create_index(
        client,
        index=index
    )
    response = wr.opensearch.delete_index(
        client,
        index=index
    )
    print(response)


def test_index_df():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_df(client,
                                      df=pd.DataFrame([{'_id': '1', 'name': 'John'},
                                                       {'_id': '2', 'name': 'George'},
                                                       {'_id': '3', 'name': 'Julia'}
                                                       ]),
                                      index='test_index_df1'
                                      )
    print(response)


def test_index_documents():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                      documents=[{'_id': '1', 'name': 'John'},
                                                 {'_id': '2', 'name': 'George'},
                                                 {'_id': '3', 'name': 'Julia'}
                                                ],
                                      index='test_index_documents1'
                                      )
    print(response)


def test_index_documents_id_keys():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                             documents=inspections_documents,
                                             index='test_index_documents_id_keys',
                                             id_keys=['inspection_id']
                                             )
    print(response)


def test_index_documents_no_id_keys():
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                             documents=inspections_documents,
                                             index='test_index_documents_no_id_keys'
                                             )
    print(response)


def test_search():
    index = 'test_search'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                             documents=inspections_documents,
                                             index=index,
                                             id_keys=['inspection_id'],
                                             refresh='wait_for'
                                             )
    df = wr.opensearch.search(
        client,
        index=index,
        search_body={
            "query": {
                "match": {
                    "business_name": "soup"
                }
            }
        },
        _source=['inspection_id', 'business_name', 'business_location']
    )

    print('')
    print(df.to_string())


def test_search_filter_path():
    index = 'test_search'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                             documents=inspections_documents,
                                             index=index,
                                             id_keys=['inspection_id'],
                                             refresh='wait_for'
                                             )
    df = wr.opensearch.search(
        client,
        index=index,
        search_body={
            "query": {
                "match": {
                    "business_name": "soup"
                }
            }
        },
        _source=['inspection_id', 'business_name', 'business_location'],
        filter_path=['hits.hits._source']
    )

    print('')
    print(df.to_string())


def test_search_scroll():
    index = 'test_search_scroll'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    response = wr.opensearch.index_documents(client,
                                             documents=inspections_documents,
                                             index=index,
                                             id_keys=['inspection_id'],
                                             refresh='wait_for'
                                             )
    df = wr.opensearch.search(
        client,
        index=index,
        is_scroll=True,
        _source=['inspection_id', 'business_name', 'business_location']
    )

    print('')
    print(df.to_string())


def test_index_json_local():
    file_path = '/tmp/inspections.json'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    with open(file_path, 'w') as filehandle:
        for doc in inspections_documents:
            filehandle.write('%s\n' % json.dumps(doc))
    response = wr.opensearch.index_json(
        client,
        index='test_index_json_local',
        path=file_path
    )
    print(response)


def test_index_json_s3():
    file_path = '/tmp/inspections.json'
    s3_key = 'tmp/inspections.json'
    client = wr.opensearch.connect(host=OPENSEARCH_DOMAIN)
    with open(file_path, 'w') as filehandle:
        for doc in inspections_documents:
            filehandle.write('%s\n' % json.dumps(doc))
    s3 = boto3.client('s3')
    s3.upload_file(file_path, BUCKET, s3_key)
    response = wr.opensearch.index_json(
        client,
        index='test_index_json_s3',
        path=f's3://{BUCKET}/{s3_key}'
    )
    print(response)


def test_index_csv_local():
    file_path = '/tmp/inspections.csv'
    index = 'test_index_csv_local'
    df=pd.DataFrame(inspections_documents)
    df.to_csv(file_path, index=False)
    client = wr.opensearch.connect(OPENSEARCH_DOMAIN)
    wr.opensearch.delete_index(client, index)
    response = wr.opensearch.index_csv(
        client,
        path=file_path,
        index=index
    )
    print(response)