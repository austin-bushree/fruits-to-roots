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
        print("🔍 Received request:", request)

        root = NGSS_STANDARDS.get(request.standard_id)
        if not root:
            print(f"❌ Standard {request.standard_id} not found in NGSS_STANDARDS")
            return {"error": f"Standard {request.standard_id} not found."}

        print(f"🌱 Using standard:\n{root}")
        explanation = await generate_root_explanation(request.fruit, root)
        print("✅ Explanation generated successfully.")
        return {"message": explanation}
    except Exception as e:
        print("🔥 Exception occurred:", str(e))
        return {"error": str(e)}
