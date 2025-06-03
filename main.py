from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SprayNest backend is running."}

@app.post("/create-token")
def create_token(data: dict):
    # Placeholder: lógica real de criação de token com solana-cli/metaplex vai aqui
    return {"status": "ok", "details": "Token creation will be implemented soon."}

@app.post("/send-tip")
def send_tip(data: dict):
    return {"status": "ok", "wallet": "2eGAjfJuqwjG2TsAqHTfCbxqYBbanzt2EcsuhG31hU1E"}
