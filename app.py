from flask import Flask, jsonify, request
from app.config import requestURI, postURI, keymd5, payload
from app.api import getResponse, getForm, setQuestionAttr, setData
import xmltodict
import requests
import dateutil.parser
import pandas as pd
from collections import OrderedDict
app = Flask(__name__)

@app.route('/folders')
def getFolder():
    data = getResponse(requestURI + '/folders')
    data = data['folders']
    lists = []
    for dt in data:
        list = {
            'name':dt['name'],
            'link': request.host_url + 'folder/' + dt['id']
        }
        lists.append(list)
    return jsonify(lists)

@app.route('/folder/<id>')
def getSurveys(id):
    data = getResponse(requestURI + '/surveys?folder_id=' + id)
    lists = []
    for dt in data['surveys']:
        list = {
            'name':dt['name'],
            'link': request.host_url + 'survey/' + dt['id'],
            'created_at': dateutil.parser.parse(dt['createdAt']),
            'modified_at': dateutil.parser.parse(dt['modifiedAt'])
        }
        lists.append(list)
    return jsonify(lists)

@app.route('/survey/<id>')
def getSurvey(id):
    data = getResponse(requestURI + '/surveys/' + id)
    data['meta_url'] = request.host_url + 'datapoint/' + data['id']
    collections = []
    for form in data['forms']:
        collection_links = {
                'path': request.host_url + 'collections/' + data['id'] + '/' + form['id'],
                'name': form['name'],
                'questionnaire': form['questionGroups']
        }
        collections.append(collection_links)
    data['forms'] = collections
    return jsonify(data)

@app.route('/datapoint/<id>')
def getDataPoint(id):
    data = getResponse(requestURI + '/data_points?survey_id=' + id)
    return jsonify(data)

@app.route('/collections/<survey_id>/<form_id>')
def getData(survey_id, form_id):
    collections = []
    data = getResponse(requestURI + '/surveys/' + survey_id)
    data['meta_url'] = request.host_url + 'datapoint/' + data['id']
    meta = data['forms'][0]['questionGroups'][0]['questions']
    for form in data['forms']:
        par_id = form['questionGroups'][0]['id']
        answers = getResponse(requestURI + '/form_instances?survey_id=' + survey_id + '&form_id=' + form_id)
        for answer in answers['formInstances']:
            resp = []
            for mt in meta:
                values = answer['responses'][par_id][0][mt['id']]
                apps = {
                    'val' : values,
                    'type' : mt['type'],
                    'var' : mt['variableName']
                }
                resp.append(apps)
            collections.append({
                'id': answer['id'],
                'submitter':answer['submitter'],
                'identifier':answer['identifier'],
                'device':answer['deviceIdentifier'],
                'submited_at':answer['submissionDate'],
                'responses':resp,
            })
    return jsonify(collections)

@app.route('/download/<id>')
def downloadData(id):
    url = requestURI + '/surveys/' + id
    allData = []
    for path, url in OrderedDict().items():
        surveys = getResponse(url)
        return jsonify(surveys)
        if (surveys.get('forms')):
            finalData = []
            for survey in surveys['forms']:
                form = survey.get('name', 'No Name')[0:2] + '_' + survey.get('id') + '.csv'
                form = form.replace('/', '_')
                formInstances = getForm(survey)
                qMap = OrderedDict()
                finalData = OrderedDict()
                setQuestionAttr(survey, qMap, finalData)
                setData(formInstances, qMap, finalData)
                df = pd.DataFrame(finalData, columns=finalData.keys)
                allData.append(df)
            return jsonify(allData)
        else:
            'No surveys found'

@app.route('/addprice')
def login():
    url = postURI + '/login_return_ACC_ID'
    data = payload([
        {'key':'keymd5', 'value':keymd5},
        {'key':'acc_name', 'value':'trang123'},
        {'key':'acc_pass', 'value':'1234'},
    ])
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    u = requests.post(url, data = data, headers = headers)
    uid = xmltodict.parse(u.text)
    ids = uid['short']['#text']
    if ids == '0':
        response = 'error login'
    else:
        url = postURI + '/add_price_return_newid'
        values = payload([
            {'key':'keymd5', 'value':keymd5},
            {'key':'ID_Commodity', 'value':'1'},
            {'key':'ID_Agency', 'value':'1'},
            {'key':'Date_var', 'value':'06/05/2018'},
            {'key':'MIN_PRICE', 'value':'999'},
            {'key':'MAX_price', 'value':'888'},
            {'key':'ACC_ID', 'value': '9'},
        ])
        r = requests.post(url, data = values, headers = headers)
        response = r.text
    return response


if __name__=='__main__':
    app.config.update(DEBUG=True)
    app.run()
