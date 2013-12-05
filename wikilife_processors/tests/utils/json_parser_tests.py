# coding=utf-8
from wikilife_processors.tests.base_test import BaseTest
from wikilife_processors.utils.json_parser import JSONParser

class JSONParserTests(BaseTest):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_to_json(self):
        collection = {"a": "qwerty", "b": 100}
        json_str = JSONParser.to_json(collection)
        assert json_str == '{"a": "qwerty", "b": 100}' 

    def test_to_collection(self):
        json_str = '{"a": "qwerty", "b": 100}'
        
        collection = JSONParser.to_collection(json_str)
        assert collection == {"a": "qwerty", "b": 100}
        assert collection != {"a": "asdfg", "b": 200}
    
