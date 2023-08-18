OpenAI Proxy Server with Flask
==============================

This project is a proxy server for the OpenAI API, built using Flask and Redis for rate limiting.

Requirements
------------

-   Docker
-   Docker Compose
-   OpenAI Python Client

Installation
------------

1.  If not already installed, install Docker and Docker Compose on your machine. Check the [official instructions](https://docs.docker.com/get-docker/) for installation.

2.  Clone the repository to your machine.

    `git clone <repository link>`

3.  Create a `.env` file at the root of the project. In this file, you need to specify two API keys: the API key for access to the proxy server (`API_KEY`) and your API key for access to OpenAI (`OPEN_AI_API_KEY`).

    Example `.env` file:

    `OPEN_AI_API_KEY=<your OpenAI API key>
    API_KEY=<API key for proxy server access>`

Launch
------

1.  Start Docker Compose.

    `docker-compose up -d`

    Docker Compose will automatically build and start the Flask and Redis containers. The server will start listening on port 8080.

Usage
-----

After the server starts, you can use the OpenAI Python Client to interact with the proxy server. Instead of the usual OpenAI API URL, use the base URL of your proxy server. Use the API key for access to the proxy server as your API key.

`openai.api_base = "http://192.168.0.1:8080/api"
openai.api_key = "wcwcmoeineo"`

License
-------

This project is distributed under the MIT license. Details can be found in the `LICENSE` file.

Support
-------

If you have any difficulties or questions about using the package, create a [discussion](https://github.com/%3Cyour_profile%3E/%3Crepository_name%3E/discussions) in this repository or send an email to <your_email>.

Contributing
------------

We welcome your feedback and suggestions! If you want to improve the code or documentation, create a new branch and submit a pull request.
