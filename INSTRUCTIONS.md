# t3py

We're building a command line application with UV and Python. Use httpx. It is designed to act as a wrapper for the T3 API.

The T3 API is included in this repo as an OpenAPI spec at openapi.json

## Important features

- The user should be able to run `t3py` and the command line interface application boots up
  - This interface should first authenticate the user to obtain a JWT, and then display a menu interface that allows them to select what they want to do.
  - The interface doesn't need to wrap the entire API, but all the reports endpoints should be implemented as routines
  - Each "routine" should be a series of steps where the user enters or selects information that will be sent to the request.
    - Preload options whenever possible. When a license number needs to be selected, offer a list to choose from.
    - Display defaults taken from the API docs.
  - The user should be able to run one-off commands like `t3py authcheck`, which will run the "authcheck" routine and then exit
- The user should be able to use `t3py` as an import to their python scripts, including various elements as needed
- Wrapping authentication is important
  - The credentials endpoint is the most commonly used.
- The t3py python library should wrap the entire T3 API. 