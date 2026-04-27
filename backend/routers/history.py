from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.user import User
from models.history import History
from schemas.history import HistoryItem, HistoryResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=HistoryResponse)
async def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0
):
    """
    Retourne l'historique de l'utilisateur connecté
    
    PARAMÈTRES :
    ├── limit : nombre d'éléments à retourner (défaut: 20)
    └── skip  : nombre d'éléments à sauter (pagination)
    
    EXEMPLE :
    GET /history?limit=10&skip=0  → 10 premiers éléments
    GET /history?limit=10&skip=10 → éléments 11 à 20
    """
    
    # Compte le total
    total = db.query(History).filter(
        History.user_id == current_user.id
    ).count()
    
    # Récupère les éléments avec pagination
    # order_by(desc) → du plus récent au plus ancien
    items = db.query(History).filter(
        History.user_id == current_user.id
    ).order_by(
        History.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return HistoryResponse(items=items, total=total)


@router.delete("/{history_id}")
async def delete_history_item(
    history_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Supprime une entrée d'historique
    
    SÉCURITÉ :
    └── On vérifie que l'entrée appartient à l'utilisateur connecté
        Un utilisateur ne peut pas supprimer l'historique d'un autre !
    """
    
    item = db.query(History).filter(
        History.id == history_id,
        History.user_id == current_user.id  # ← IMPORTANT !
    ).first()
    
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Entrée non trouvée")
    
    db.delete(item)
    db.commit()
    
    return {"message": "Entrée supprimée"}