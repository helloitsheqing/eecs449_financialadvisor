docker build -t auth0-python-web-01-login .
docker run --env-file backend_env.env -p 5001:5001 -it auth0-python-web-01-login
