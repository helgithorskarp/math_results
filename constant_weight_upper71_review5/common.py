"""Small reviewer-owned exact validation and serialization helpers."""
import json

def require(value,message):
    if not value: raise ValueError(message)

def canonical(value):
    return (json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()

def unique_object(pairs):
    result={}
    for key,value in pairs:
        require(key not in result,'duplicate JSON key')
        result[key]=value
    return result
