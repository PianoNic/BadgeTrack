from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from mediatorx import Mediator

from src.api.controller import controller
from src.api.dependencies import get_mediator
from src.application.commands.record_visit.record_visit_command import RecordVisitCommand
from src.application.commands.record_visit.recorded_visit import RecordedVisit
from src.domain.exceptions import InvalidBadgeError

router = APIRouter(tags=["Badge"])

VISITOR_COOKIE = "visitor_id"
_ONE_YEAR_SECONDS = 31536000
# Badges sit behind image proxies like GitHub's camo, which cache for as long as the response allows.
# shields.io answers with max-age=432000 (5 days), so the SVG is served from here with caching off.
_NO_CACHE_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Cache-Control": "max-age=0, no-cache, no-store, must-revalidate",
    "Pragma": "no-cache",
    "Expires": "0",
}
# the SVG is shown from this origin, so it gets no scripts, fonts or remote loads
_SVG_HEADERS = {
    **_NO_CACHE_HEADERS,
    "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'",
}


@controller(router)
class BadgeController:
    mediator: Mediator = Depends(get_mediator)

    @router.get("/badge")
    async def badge(
        self,
        request: Request,
        tag: str,
        label: str = "visits",
        color: str = "4ade80",
        style: str = "flat",
        logo: str = "",
    ) -> RedirectResponse:
        command = RecordVisitCommand(
            tag=tag,
            label=label,
            color=color,
            style=style,
            logo=logo,
            visitor_id=request.cookies.get(VISITOR_COOKIE),
        )
        try:
            visit: RecordedVisit = await self.mediator.send(command)
        except InvalidBadgeError as error:
            raise HTTPException(status_code=400, detail="Invalid parameters.") from error

        if visit.badge_svg is None:
            response = RedirectResponse(visit.badge_url, status_code=302, headers=_NO_CACHE_HEADERS)
        else:
            response = Response(visit.badge_svg, media_type="image/svg+xml", headers=_SVG_HEADERS)
        if visit.new_visitor_id:
            response.set_cookie(
                key=VISITOR_COOKIE,
                value=visit.new_visitor_id,
                max_age=_ONE_YEAR_SECONDS,
                httponly=True,
                samesite="lax",
            )
        return response
