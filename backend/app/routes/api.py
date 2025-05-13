from fastapi import APIRouter
from pydantic import BaseModel
from app.services.ai import generate_root_explanation, NGSS_STANDARDS

router = APIRouter()

class FruitRootRequest(BaseModel):
    fruit: str
    standard_id: str

@router.post("/api/fruit")
async def get_root_explanation(request: FruitRootRequest):
    try:
        root = NGSS_STANDARDS.get(request.standard_id)
        if not root:
            return {"error": f"Standard {request.standard_id} not found."}

        explanation = await generate_root_explanation(request.fruit, root)
        return {"message": explanation}
    except Exception as e:
        return {"error": str(e)}

import os

@router.get("/debug/env")
async def debug_env():
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL")
    }