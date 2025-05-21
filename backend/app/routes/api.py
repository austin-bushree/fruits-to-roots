from fastapi import APIRouter, Request
from pydantic import BaseModel
# from app.services.ai import generate_root_explanation, NGSS_STANDARDS
from app.services.ai import generate_dci_explanation
from starlette.concurrency import run_in_threadpool
import sqlite3


router = APIRouter()

#Using Pydantic models to declare request bodies.
class FruitRootRequest(BaseModel):
    fruit: str
    standard_id: str

class DCIRequest(BaseModel):
    group_name: str
    interest: str

# @router.post("/api/fruit")
# async def get_root_explanation(request: FruitRootRequest):
#     try:
#         print("🔍 Received request:", request)
#
#         root = NGSS_STANDARDS.get(request.standard_id)
#         if not root:
#             print(f"❌ Standard {request.standard_id} not found in NGSS_STANDARDS")
#             return {"error": f"Standard {request.standard_id} not found."}
#
#         print(f"🌱 Using standard:\n{root}")
#         explanation = generate_root_explanation(request.fruit, root)
#         print("✅ Explanation generated successfully.")
#         return {"message": explanation}
#     except Exception as e:
#         print("🔥 Exception occurred:", str(e))
#         return {"error": str(e)}

@router.post("/api/explain-dci", tags=["DCI Explanation"])
async def explain_dci(payload: DCIRequest):
    print("REQUESTED: ", payload.group_name, " ", payload.interest)

    try:
        print("TRYING")
        explanation = await run_in_threadpool(generate_dci_explanation, payload.group_name, payload.interest)
        print("RESPONSE: ", explanation)
        return {"message": explanation}
    except Exception as e:
        return {"error": str(e)}

@router.get("/api/dci-group-names", tags=["DCI Explanation"])
async def get_dci_group_names():
    try:
        conn = sqlite3.connect("app/db/ngss.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT group_name FROM dcis ORDER BY group_name")
        results = cursor.fetchall()
        conn.close()

        # Extract the first element from each row (which is a tuple)
        group_names = [row[0] for row in results]
        return group_names
    except Exception as e:
        return {"error": str(e)}
