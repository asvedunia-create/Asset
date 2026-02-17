from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.ad import ADResolver
from app.collectors import collect_inventory
from app.database import Base, engine, get_db
from app.models import Asset, Service
from app.schemas import AssetOut, RefreshRequest

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Asset Inventory MVP")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
ad_resolver = ADResolver()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/assets", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    result = db.execute(select(Asset).options(selectinload(Asset.services)).order_by(Asset.hostname))
    return result.scalars().all()


@app.post("/api/assets/refresh", response_model=list[AssetOut])
def refresh_assets(payload: RefreshRequest, db: Session = Depends(get_db)):
    refreshed: list[Asset] = []

    for target in payload.targets:
        snapshot = collect_inventory(protocol=target.protocol, hostname=target.hostname, address=target.address)
        owner = ad_resolver.resolve_owner(target.hostname)

        asset = db.execute(select(Asset).where(Asset.hostname == target.hostname)).scalar_one_or_none()
        if asset is None:
            asset = Asset(
                hostname=target.hostname,
                address=target.address,
                protocol=target.protocol,
                os_name=snapshot.os_name,
                owner=owner,
            )
            db.add(asset)
            db.flush()
        else:
            asset.address = target.address
            asset.protocol = target.protocol
            asset.os_name = snapshot.os_name
            asset.owner = owner
            asset.services.clear()

        for svc in snapshot.services:
            asset.services.append(Service(name=svc["name"], version=svc["version"]))

        refreshed.append(asset)

    db.commit()

    for asset in refreshed:
        db.refresh(asset)

    return refreshed
