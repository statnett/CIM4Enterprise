import argparse
import json
import os
from datetime import datetime
from http import HTTPMethod
from io import StringIO
from time import sleep

import requests
from rdflib import Graph, URIRef, Literal

K_CLASS = 'Classes'
K_PROPS = 'Properties'
K_PROPURI = 'PropertyUri'
K_AVAL = 'AllowedValues'
K_CPROP = 'ClassProperties'

parser = argparse.ArgumentParser(
  description='A CLI app to create bSDD dictionary from CIM'
              'ontology in GraphDB repository.')

parser.add_argument('-gdb', '--gdb_uri', help='GraphDB URI', required=True)
parser.add_argument('-u', '--gdb_user', help='GraphDB username', required=True)
parser.add_argument('-p', '--gdb_pass', help='GraphDB password', required=True)
parser.add_argument('-r', '--gdb_repo', help='GraphDB repository',
                    required=True)
args = parser.parse_args()

HEADER_GDB_QUERY = {"Content-type": "application/sparql-query", 'Accept': '*/*'}
PATH_QUERY_CLASS_INFO = '/../../SPARQL/retrieve-class-info.rq'
PATH_QUERY_PROP_INFO = '/../../SPARQL/retrieve-properties-info.rq'
URL_BSDD_QUDT_MAP = 'https://api.bsdd.buildingsmart.org/api/Unit/v1'
BSDD_IMPORT = {
  "ModelVersion": "2.0",
  "OrganizationCode": "ucaiug",
  "DictionaryCode": "cim",
  "DictionaryName": "CIM Asset Catalogue",
  "DictionaryVersion": "0.1",
  "LanguageIsoCode": "EN",
  "LanguageOnly": "false",
  "UseOwnUri": "true",
  "DictionaryUri": "https://cim.ucaiug.io/ns",
  "License": None,
  "LicenseUrl": None,
  "ChangeRequestEmailAddress": None,
  "MoreInfoUrl": None,
  "QualityAssuranceProcedure": None,
  "QualityAssuranceProcedureUrl": None,
  "ReleaseDate": datetime.utcnow().strftime('%Y-%m-%d'),
  "Status": "draft",
}
PATH_CIM_BSDD_JSON = '/../../cim-bsdd.json'
BSDD = "https://bsdd.buildingsmart.org/"


class CimToBsddTransformer(object):
  def __init__(self, params):
    self.gdb_uri = params.gdb_uri
    self.gdb_user = params.gdb_user
    self.gdb_password = params.gdb_pass
    self.gdb_repo = params.gdb_repo
    self.sparql_uri = "repositories/" + params.gdb_repo
    self.bsdd_to_qdt = None

  @staticmethod
  def call_api(attempt, uri, req_method, req_headers=None, req_body=None,
      files=None, timeout=10):
    response = None
    while attempt > 0:
      try:
        if req_method == HTTPMethod.POST:
          response = requests.post(url=uri, data=req_body, headers=req_headers,
                                   files=files, timeout=timeout)
        elif req_method == HTTPMethod.GET:
          response = requests.get(url=uri, params=req_body, headers=req_headers,
                                  timeout=timeout)
        else:
          raise requests.exceptions.RequestException(
            req_method + " not supported.")
        if response.status_code == 200:
          break
        else:
          sleep(2)
          attempt -= 1
          continue
      except Exception as e:
        print(e.args)
        sleep(2)
        attempt -= 1
        continue
    return response

  def get_gdb_auth_token(self):
    login_uri = "rest/login"
    login_body = json.dumps(
        {"username": self.gdb_user, "password": self.gdb_password})
    login_headers = {"Content-type": "application/json"}
    login = self.call_api(5, self.gdb_uri + login_uri, HTTPMethod.POST,
                          login_headers, login_body)
    token = login.headers['Authorization']

    return token

  @staticmethod
  def get_sparql_from_file(location):
    file = open(os.getcwd() + location)
    sparql = file.read()
    file.close()

    return sparql

  def get_query_results_graph(self, query_fspath):
    headers = HEADER_GDB_QUERY
    headers['Authorization'] = self.get_gdb_auth_token()
    sparql = self.get_sparql_from_file(query_fspath)
    info = self.call_api(5, self.gdb_uri + self.sparql_uri,
                         HTTPMethod.POST, headers, sparql, timeout=300)
    g = Graph(base=BSDD)
    g.parse(StringIO(info.text))

    return g

  def get_bsdd_unit_from_qudt_url(self, url):
    if self.bsdd_to_qdt is None:
      self.bsdd_to_qdt = json.loads(
        self.call_api(5, URL_BSDD_QUDT_MAP, HTTPMethod.GET).text)
    unit = next((unit for unit in self.bsdd_to_qdt if
                 unit.get('qudtUri') is not None and unit['qudtUri'] == str(
                   url)), str(url))

    return unit

  def get_class_info(self):
    classes_dict = {K_CLASS: []}
    g = self.get_query_results_graph(PATH_QUERY_CLASS_INFO)

    for cl in g.subjects(URIRef('ClassType', base=BSDD), Literal('Class')):
      class_dict = {K_CPROP: []}

      for p, o in g.predicate_objects(cl):
        pk = str(p).replace(BSDD, '')
        if p not in [URIRef(K_CPROP, base=BSDD)]:
          class_dict[pk] = str(o)
        else:
          prop = {K_AVAL: []}
          for propp, propo in g.predicate_objects(o):
            if propp != URIRef(K_AVAL, base=BSDD):
              if propp == URIRef('Unit', base=BSDD):
                prop[str(propp).replace(BSDD,
                                        '')] = self.get_bsdd_unit_from_qudt_url(
                  propo)
              else:
                prop[str(propp).replace(BSDD, '')] = str(propo)
            else:
              alv = {}
              for alvp, alvo in g.predicate_objects(propo):
                alv[str(alvp).replace(BSDD, '')] = str(alvo)
              if len(alv.items()) > 0:
                prop = next((prp for prp in class_dict[K_CPROP] if
                             prp.get(K_PROPURI) == prop.get(K_PROPURI)), prop)
                prop_alvs = prop[K_AVAL]
                if alv not in prop_alvs:
                  prop[K_AVAL].append(alv)
          if not len(prop[K_AVAL]) > 0:
            prop.pop(K_AVAL)
          prp = next((prp for prp in class_dict[pk] if
                      prp.get(K_PROPURI) == prop.get(K_PROPURI)), None)
          if prp is None:
            class_dict[pk].append(prop)
      if not len(class_dict[K_CPROP]) > 0:
        class_dict.pop(K_CPROP)
      classes_dict[K_CLASS].append(class_dict)

    return classes_dict

  def get_property_info(self):
    props_dict = {K_PROPS: []}
    uk = 'Units'
    g = self.get_query_results_graph(PATH_QUERY_PROP_INFO)

    for pr in g.subjects(URIRef('Name', base=BSDD)):
      prop_dict = {uk: [], K_AVAL: []}

      for p, o in g.predicate_objects(pr):
        pk = str(p).replace(BSDD, '')
        if p not in [URIRef(uk, base=BSDD), URIRef(K_AVAL, base=BSDD)]:
          prop_dict[pk] = str(o)
        else:
          node = {}
          for nodep, nodeo in g.predicate_objects(o):
            node[str(nodep).replace(BSDD, '')] = str(nodeo)
          if len(node.items()) > 0:
            if p == URIRef(uk, base=BSDD):
              unit = self.get_bsdd_unit_from_qudt_url(nodeo)
              if unit not in prop_dict[pk]:
                prop_dict[pk].append(unit)
            else:
              prop_dict[pk].append(node)
      if not len(prop_dict[uk]) > 0:
        prop_dict.pop(uk)
      if not len(prop_dict[K_AVAL]) > 0:
        prop_dict.pop(K_AVAL)
      props_dict[K_PROPS].append(prop_dict)

    return props_dict

  def create_bsdd_dict(self):
    path = os.getcwd() + PATH_CIM_BSDD_JSON
    bsdd = BSDD_IMPORT.copy()
    classes = self.get_class_info()
    properties = self.get_property_info()
    bsdd[K_CLASS] = classes[K_CLASS]
    bsdd[K_PROPS] = properties[K_PROPS]
    with open(path, 'w') as fout:
      json.dump(bsdd, fout, indent=4)

    return path


tr = CimToBsddTransformer(args)

print('bSDD written to: ' + tr.create_bsdd_dict())
