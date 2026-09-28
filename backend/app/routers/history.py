from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.schemas.analysis import HistorySummaryItem, DeleteResponse
from backend.app.database import (
    get_all_history,
    get_analysis_by_id,
    delete_analysis_by_id,
    clear_all_history
)

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=List[HistorySummaryItem], summary="Get Analysis History")
async def list_history(limit: int = 50):
    """Returns list of past resume matching analyses with scores and timestamps."""
    records = await get_all_history(limit=limit)
    return records

@router.get("/{analysis_id}", summary="Get Single Analysis by ID")
async def get_single_analysis(analysis_id: str):
    """Retrieves full analysis report for the given ID."""
    record = await get_analysis_by_id(analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found.")
    return record

@router.delete("/{analysis_id}", response_model=DeleteResponse, summary="Delete Analysis from History")
async def delete_single_analysis(analysis_id: str):
    """Deletes a specific analysis record from SQLite."""
    deleted = await delete_analysis_by_id(analysis_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return DeleteResponse(success=True, message=f"Analysis '{analysis_id}' deleted successfully.")

@router.delete("", response_model=DeleteResponse, summary="Clear All Analysis History")
async def clear_history():
    """Deletes all analysis history from SQLite."""
    count = await clear_all_history()
    return DeleteResponse(success=True, message=f"Cleared {count} analysis history records.")
