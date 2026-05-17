## Test Execution

1. Create virtualenv and install requirements:
    ```bash
    $ virtualenv venv 
    $ source venv/bin/activate 
    $ cd test
    $ pip install -r requirements.txt
    ```
2. Execute test cases to see the full functionality
    ```bash
    $ cd test
    $ behave
    ```

3. Run ZAProxy using daemon mode
    ```
    docker run -u zap -p 8080:8080 -d zaproxy/zap-stable zap.sh -daemon -host 0.0.0.0 -port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=change-me-9203935709
    ```

4. Run DAST test cases
    ```
    $ cd test
    $ behave -t @dast
    ```