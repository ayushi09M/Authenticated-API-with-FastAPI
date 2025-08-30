from fastapi import FastAPI

# 1.create instance of FsatAPI class
app = FastAPI()

# ========Ordering of routes matters!===============================
# If you have two routes that could match the same path, the order in which they are defined matters.
# FastAPI will match the first route that fits the request path.  
#  
# For example, if you have a static route and a dynamic route that could match the same path,
# the static route should be defined first to ensure it is matched correctly.

# "/users/me" : static route
# "/users/{username}" : dynamic route

# ✅ This ensures static paths are not accidentally captured by dynamic paths.
# ===============================================


#static route, should be defined first
# eg: "/users/me",.... not "/users/{username}"", because me can be a username too
@app.get("/users/me")
def read_user_me():
    return {"This is the current user"}

# Dynamic route , should be defined after static routes
@app.get("users/{username}")
def profile(username:str):
    return {f"This is the username: {username}"}