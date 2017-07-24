[![Build Status](https://travis-ci.org/ridibooks/lightweight-rest-tester.svg?branch=master)](https://travis-ci.org/ridibooks/lightweight-rest-tester)
[![Coverage Status](https://coveralls.io/repos/github/ridibooks/lightweight-rest-tester/badge.svg?branch=HEAD)](https://coveralls.io/github/ridibooks/lightweight-rest-tester?branch=HEAD)

# lightweight-rest-tester
A lightweight REST API testing framework. It reads test cases from JSON files, and then dynamically generates and executes unittest of Python. It supports five HTTP methods, *GET*, *POST*, *PUT*, *UPDATE* and *DELETE*.

## 1. Getting Started
Write your test cases into JSON files and pass their locations as the argument.

### 1.1. JSON File Format
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

### 1.2. Request

#### url
There is nothing special on url.

#### params (optional)
This framework generates multiple test cases with all possible sets of parameters when you put arrays of values into parameters. It will let you know which parameter set fails a test if any. For example, the following parameters generate 27 test cases:
```json
"params": {
  "param_1": [1, 2, 3],
  "param_2": ["a", "b", "c"],
  "param_3": ["def", "efg", "hij"]
}
```

(TBD)
