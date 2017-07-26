[![Build Status](https://travis-ci.org/ridibooks/lightweight-rest-tester.svg?branch=master)](https://travis-ci.org/ridibooks/lightweight-rest-tester)
[![Coverage Status](https://coveralls.io/repos/github/ridibooks/lightweight-rest-tester/badge.svg?branch=HEAD)](https://coveralls.io/github/ridibooks/lightweight-rest-tester?branch=HEAD)

# lightweight-rest-tester
A lightweight REST API testing framework written in Python (working with 2.7 ~ 3.6). It reads [JSON Schema](http://json-schema.org) test-cases from JSON files and then generates and executes unittest of Python. 

## 1. Getting Started
Write your test cases into JSON files and pass their locations (directory) as the argument:
```
python rest_tester/main.py "JSON file directory"
```

If your python cannot identify the `rest_tester` module, then set the python path:
```
export PYTHONPATH=.
```

### JSON File Format
Put HTTP method as a top-level entry, and then specify what you *request* and how you verify its *response*. It supports five HTTP methods, *GET*, *POST*, *PUT*, *PATCH* and *DELETE*. In the `request` part, you can set the target REST API by URL (`url`) with parameters (`params`) and timeout (`timeout`) in seconds. In the `response` part, you can add two types of test cases, HTTP status code (`statusCode`) and [JSON Schema](http://json-schema.org) (`jsonSchema`).

The following example sends GET request to `http://json-server:3000/comments` with the `postId=1` parameter and `10` seconds timeout. When receiving the response, it checks if the status code is `200` and the returned JSON satisfies JSON Schema:

```json
{
  "get": {
    "request": {
      "url": "http://json-server:3000/comments",
      "params": {
        "postId": 1
      },
      "timeout" : 10
    },
    
    "response": {
      "statusCode": 200,
      "jsonSchema": {
        "JSON Schema"
      }
    }
  }
}
```

You can find some JSON samples in [here](/samples) and [there](/test/function/resources). For the details, please read the below.

## 2. Request

The `request` part consists of `url`, `params` and `timeout`. Except for `url`, they are optional.

#### params
When parameter values are given as an array, multiple test cases with all possible parameter-sets are generated. They will show which parameter-set fails a test if exists (please see [5. Test Case Name](#5-test-case-name)). For example, the following parameters generate 9 test cases (e.g., `{"p1": 1, "p2": "abc", "p3": "def"}`):
```json
"params": {
  "p1": [1, 2, 3],
  "p2": "abc",
  "p3": ["def", "efg", "hij"]
}
```

#### timeout
Request's timeout in seconds. Its default value is 10 (seconds).

## 3. Response

The `response` part validates the received status code (`statusCode`) and JSON by JSON Schema (`jsonSchema`). They are all optional, but at least one of them should be provided.

#### statusCode
The expected status code. When an array of status codes is given, the test checks if one of these codes is received. For example, the following `statusCode` checks if the received status code is either `200` or `201`:
```json
"statusCode": [200, 201]
```

#### jsonSchema
This framework uses [jsonschema](https://github.com/Julian/jsonschema) to validate the received JSON. `jsonschema` fully supports the [Draft 3](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft3Validator) and [Draft 4](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft4Validator) of JSON Schema.

## 4. Write-and-Read Test

Sometimes, it is necessary to check if some modifications on a database work correctly. We call such test scenario as *Write-and-Read* test that has a particular test-execution-order like *PUT-and-GET*. This framework supports this feature. To use it, just put two HTTP methods in one JSON file and fill the information for each method. You can find an example of *PUT-and-GET* in [here](https://github.com/ridibooks/lightweight-rest-tester/blob/dev/readme/init/test/function/resources/test_function_write_put.json).

You can build the four types of *Write-and-Read* test:

- *POST-and-GET*
- *PUT-and-GET*
- *PATCH-and-GET*
- *DELETE-and-GET*

Unlike the single-method test, *Write-and-Read* test builds always one test case to preserve test-execution order. Even when arrays of parameter values are given, all the test cases belonging to *Write* method (e.g., *PUT*) are executed first and then the test cases of *Read* method (e.g., *GET*) are executed.

## 5. Test Case Name

This framework uses [URL query string format](https://en.wikipedia.org/wiki/Query_string) to make test case name. However, it starts with JSON file name instead of `url`. It helps you understand which parameter-set fails a test if exists. For example, `json_file.json?postId=1&id=2` is the name of the following test case:

```json
"request": {
  "url": "http://json-server:3000/comments",
  "params": {
    "postId": 1,
    "id": 2
  },
  "timeout" : 10
}
```

Unlike the single-method test, *Write-and-Read* test uses only JSON file name without parameters when making its name.

## 6. Contributions to This Project

Please feel free to leave your suggestions or make PRs.
