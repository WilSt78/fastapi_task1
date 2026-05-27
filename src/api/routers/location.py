from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_location_use_case,
    delete_location_use_case,
    get_all_locations_use_case,
    get_location_by_id_use_case,
)
from src.core.exceptions.domain_exceptions import (
    LocationNameIsOccupiedException,
    LocationNotFoundByIdException,
)
from src.domain.use_cases.locations import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetAllLocationsUseCase,
    GetLocationByIdUseCase,
)
from src.schemas.locations import Location
from src.services.auth import AuthService

router = APIRouter()


@router.get(
    "/locations",
    response_model=list[Location],
    status_code=status.HTTP_200_OK,
)
async def get_all_locations(
    use_case: GetAllLocationsUseCase = Depends(
        get_all_locations_use_case
    ),
):
    return await use_case.execute()


@router.get(
    "/locations/{location_id}",
    response_model=Location,
    status_code=status.HTTP_200_OK,
)
async def get_location_by_id(
    location_id: int,
    use_case: GetLocationByIdUseCase = Depends(
        get_location_by_id_use_case
    ),
):
    try:
        return await use_case.execute(location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.post(
    "/locations",
    response_model=Location,
    status_code=status.HTTP_201_CREATED,
)
async def create_location(
    name: str,
    current_user=Depends(AuthService.get_current_user),
    use_case: CreateLocationUseCase = Depends(
        create_location_use_case
    ),
):
    try:
        return await use_case.execute(name)
    except LocationNameIsOccupiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        ) from exc


@router.delete(
    "/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_location(
    location_id: int,
    current_user=Depends(AuthService.get_current_user),
    use_case: DeleteLocationUseCase = Depends(
        delete_location_use_case
    ),
):
    try:
        await use_case.execute(location_id)
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    return None
