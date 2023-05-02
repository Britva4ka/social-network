# social-network
hillel_python_pro
1. git clone
2. create+activate venv (```python3 -m venv venv``` + ```source venv/bin/activate```)
3. ```pip install -r requirements.txt```
4. create directory for user's avatar saving (or it will be created automatically)
5. create .env ```cp env.example .env``` and set your data
6. READY TO RUN (network.py)

* To create fake users
```flask fake users <amount:int>```
* Extract users_data 
```flask user extract_users```
* Extract post_data 
```flask post extract_posts <user_id:int>```

* If FATAL:  password authentication failed for user - create postgres superuser named system user with system password

* API endpoints:
```
/generate-token

/users GET POST
/users/<int:user_id> GET PUT DELETE
/profiles GET
/profiles/<int:profile_id> GET PUT
/posts GET POST
/posts/<int:post_id> GET PUT DELETE
/users/<int:user_id>/posts GET POST
/users/<int:user_id>/posts/<int:post_id> GET POST PUT DELETE
/likes GET POST
/dislikes GET POST
/likes/<int:like_id> GET DELETE
/dislikes/<int:dislike_id> GET DELETE
/messages GET POST 
/messages/<int:message_id> GET PUT DELETE
```