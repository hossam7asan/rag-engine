from fastapi import APIRouter, Depends, UploadFile, status
from controllers import DataController
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
import anyio
import logging
from models.enums.ResponseEnums import ResponseSignal


logger = logging.getLogger(__name__)
data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings),
    data_controller: DataController = Depends(DataController),
):

    # validation the file properties
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal},
        )

    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=(file.filename or "unnamed"), project_id=project_id
    )

    try:
        async with await anyio.open_file(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception:
        logger.exception("Error while uploading file")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value},
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
        }
    )
