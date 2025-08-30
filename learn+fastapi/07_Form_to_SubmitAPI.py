from fastapi import FastAPI, Form

# Create FastAPI app
app = FastAPI()

# ---------------------------------------
# Login API
# ---------------------------------------
# - Here we are using Form(...) to take input
# - username and password will come from a form (not JSON)
# - "..." means these fields are required
# ---------------------------------------
@app.post("/login")
def login(
    username: str = Form(...),   # take username from form-data
    password: str = Form(...)    # take password from form-data
):
    # For learning: just return what we received
    # ⚠️ Never return password in real projects
    return {"username": username, "password": password}
