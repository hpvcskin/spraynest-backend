
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenData(BaseModel):
    name: str
    symbol: str
    supply: int
    creator: str

@app.post("/create-token")
async def create_token(data: TokenData):
    try:
        name = data.name
        symbol = data.symbol
        supply = str(data.supply)
        creator = data.creator

        # 1. Criar token
        token_output = subprocess.check_output(["spl-token", "create-token"], text=True)
        mint_address = token_output.strip().split()[-1]

        # 2. Criar conta associada
        subprocess.run(["spl-token", "create-account", mint_address], check=True)

        # 3. Mintar tokens para o endereço do utilizador
        subprocess.run(["spl-token", "mint", mint_address, supply, creator], check=True)

        # 4. Revogar mint authority
        subprocess.run(["spl-token", "authorize", mint_address, "mint", "--disable"], check=True)

        # 5. Revogar freeze authority
        subprocess.run(["spl-token", "authorize", mint_address, "freeze", "--disable"], check=True)

        return {"token_address": mint_address}

    except subprocess.CalledProcessError as e:
        return {"error": f"Command failed: {e.cmd}\n{e.output}"}
    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def root():
    return {"message": "SprayNest backend is running."}
