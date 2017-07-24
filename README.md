[![Build Status](https://travis-ci.org/ridibooks/lightweight-rest-tester.svg?branch=master)](https://travis-ci.org/ridibooks/lightweight-rest-tester)
[![Coverage Status](https://coveralls.io/repos/github/ridibooks/lightweight-rest-tester/badge.svg?branch=HEAD)](https://coveralls.io/github/ridibooks/lightweight-rest-tester?branch=HEAD)

# lightweight-rest-tester
A lightweight REST API testing framework. It reads test cases from JSON files, and then dynamically generates and executes unittest of Python. It supports five HTTP methods, *GET*, *POST*, *PUT*, *UPDATE* and *DELETE*.

## 1. Getting Started
Write your test cases into JSON files and pass their locations as the argument.

### JSON File Format
Put HTTP method as a top-level entry, and then specify what you *request* and how you verify its *response*. In the `request` part, you can set the target REST API by URL (`url`) with parameters (`params`) and timeout (`timeout`) in seconds. In the `response` part, you can add two types of test cases, HTTP status code (`statusCode`) and [JSON Schema](http://json-schema.org) (`jsonSchema`).

The following example sends GET request to `http://json-server:3000/comments` with the `postId=1` parameter and `10` seconds timeout. When receiving the response, it checks if the status code is `200` and the returned JSON satifies JSON Schema:

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

## 2. Request

The `request` part consists of `url`, `params` and `timeout`. Except for `url`, they are optional.

#### params
This framework generates multiple test cases with all possible sets of parameters when you put arrays of parameter values. It will let you know which parameter set fails a test if any. For example, the following parameters generate 27 test cases:
```json
"params": {
  "param_1": [1, 2, 3],
  "param_2": ["a", "b", "c"],
  "param_3": ["def", "efg", "hij"]
}
```

#### timeout
Request's timeout in seconds. Its default value is 10 (seconds).

## 3. Response

The `response` part validates the received status code (`statusCode`) and JSON by JSON Schema (`jsonSchema`). They are all optional. However, you should put at least one of them.

#### statusCode
The expected status code. If you put an array of status codes, a test will be passed when one of these codes is received. For example, the following `statusCode` will pass a test if the received status code is either `200` or `201`:
```json
"response": {
  "statusCode": [200, 201]
}
```

#### jsonSchema
This framework uses [jsonschema](https://github.com/Julian/jsonschema) to validate the received JSON. `jsonschema` fully supports the [Draft 3](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft3Validator) and [Draft 4](https://python-jsonschema.readthedocs.io/en/latest/validate/#jsonschema.Draft4Validator) of JSON Schema.

## 4. Write-and-Read Test

This framework support *Write-and-Read* test scenarios that have particular test-execution-order like *PUT-and-GET*. To use this feature, just put two HTTP methods in one JSON file and fill the necessary information for each method. You can find an example of *PUT-and-GET* in [here](https://github.com/ridibooks/lightweight-rest-tester/blob/dev/readme/init/test/function/resources/test_function_write_put.json).

You can build four types of *Write-and-Read* tests:
*POST-and-GET*, *PUT-and-GET*, *UPDATE-and-GET* and *DELETE-and-GET*.

Unlike single method test, *Write-and-Read* test builds always one test case to preserve test-execution order.

(TBD)
