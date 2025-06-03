
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-token")
async def create_token(request: Request):
    try:
        data = await request.json()
        name = data.get("name")
        symbol = data.get("symbol")
        supply = str(data.get("supply"))
        creator = data.get("creator")

        if not name or not symbol or not supply or not creator:
            return {"error": "Missing required fields"}

        # 1. Criar token
        token_output = subprocess.check_output(["spl-token", "create-token"], text=True)
        mint_address = token_output.split()[-1]

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
