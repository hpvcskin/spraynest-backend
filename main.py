from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess

app = FastAPI()

# CORS middleware para permitir chamadas do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Considera limitar isto no futuro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de dados recebidos do frontend
class TokenData(BaseModel):
    name: str
    symbol: str
    supply: int
    decimals: int
    creator: str

@app.get("/")
def root():
    return {"status": "SprayNest backend is live."}

@app.post("/create-token")
async def create_token(data: TokenData):
    try:
        name = data.name
        symbol = data.symbol
        supply = str(data.supply)
        decimals = str(data.decimals)
        creator = data.creator

        # 1. Criar o token
        token_output = subprocess.check_output(
            ["spl-token", "create-token", "--decimals", decimals],
            text=True
        )
        mint_address = token_output.strip().split()[-1]

        # 2. Criar conta associada
        subprocess.run(["spl-token", "create-account", mint_address], check=True)

        # 3. Mintar tokens para a wallet do utilizador (creator)
        subprocess.run(["spl-token", "mint", mint_address, supply, creator], check=True)

        # 4. Revogar autoridade de mint
        subprocess.run(["spl-token", "authorize", mint_address, "mint", "--disable"], check=True)

        # 5. Revogar autoridade de freeze
        subprocess.run(["spl-token", "authorize", mint_address, "freeze", "--disable"], check=True)

        return {"token_address": mint_address}

    except subprocess.CalledProcessError as e:
        return {"error": f"Erro ao executar comando: {e.cmd}\nSaída: {e.output}"}
    except Exception as e:
        return {"error": str(e)}
