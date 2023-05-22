# Warehouse Inventory API 🏪
> A python-based solution for a Warehouse Inventory system using [FastAPI](https://fastapi.tiangolo.com/lo/).

## Overview:

A shop in London has 2 million IoT tracking devices in the Warehouse Inventory for sale,
of which half need configuration to meet UK industry standards.
A configured device will have a status ACTIVE and an ideal temperature between (0’C to
10’C).

When a device is not configured, the default status is READY and temperature value is -
1’C.

Every device has a unique secret seven-digit pin code used for unlocking the device.
A given device needs to be sent to a Device Configuration Service (DCS) to set the device
status ACTIVE and random temperature value between (0 to 10).
The Device Configuration Service does not need a device pin code for the configuration
operation.

The shop can sell a device only if it meets the UK government's industry standard.

<br>

## The project include the following:
A solution for the London shop as described above:
1. Develop a REST API for the Warehouse Inventory to
    - Add, update, or remove a device
    - Return all devices available for sale in numerical order of their seven-digit
pin code.
2. Develop the Device Configuration Service and provide an endpoint responsible for configuring a device.
3. Provide comprehensive Unit and Integration tests for
    - All database repositories where applicable,
    - All communicating API and endpoints.


## How to use:
### Setup and Run: 
- Clone the repository:
    ```sh
    git clone https://github.com/kfrawee/warehouse-inventory-api.git
    ```
- Local run:
    - Install degeneracies:
        ```sh
        pip install -r requirements.txt
        ```
    - Run the server (debug mode):
        ```sh
        python main.py
        ```
        - Debug: 

            - If you're using vscode, configure debugger: `.vscode/launch.json`:

                ```json
                {
                    "version": "0.2.0",
                    "configurations": [
                        {
                            "name": "Python: Debug Server",
                            "type": "python",
                            "request": "launch",
                            "program": "./debug_server.py",
                            "console": "integratedTerminal",
                            "justMyCode": true
                        }
                    ]
                }
                ```

        - Or:
                
            ```sh
            python debug_server.py
            ```

- Using docker:
    ```sh 
    docker-compose up -d
    ```
## Test and Documentation:
To make sure the API is running, run the health curl:
```sh
curl --location 'http://localhost:8000/ping' 
```
<br>

Now, navigate to `http://localhost:8000/docs` to view the available endpoints and test the API and view the API documentation . <br>

Also, you can navigate to `http://localhost:8000/redoc` to check the API documentation.

## Run Tests:
To run tests with coverage ratio, using Pytest:
```sh
pytest --cov --cov-config=.coveragerc tests/integration
```
---
