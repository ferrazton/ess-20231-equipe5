from fastapi import APIRouter, Query, status, File, UploadFile
from db.server import server_;
from schemas.response import HttpResponseModel
from service.impl.item_service import ItemService
from schemas.post_schema import NewPost

router = APIRouter()

@router.get('/')
async def search():
    return {'None': 'Bem Vindo aos Posts!'}
    
@router.get("/{post_id}", 
    response_model=HttpResponseModel,
    status_code=status.HTTP_200_OK,
    description="Retrieve an post by its ID",
    tags=["user post"],
    responses={
        status.HTTP_200_OK: {
            "model": HttpResponseModel,
            "description": "Successfully got post by id",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Post not found",
        }
    })
async def get_post(post_id: str) -> HttpResponseModel:
    '''
    Get post by ID
    Parameters:
    - post_id: The ID of the post to retrieve.

    Returns:
    - The post with the specified ID.

    Raises:
    - HTTPException 404: If the post is not found.
    '''
    post_get_response = ItemService.get_post(post_id)
    return post_get_response

@router.post("/new_post", 
            response_model=HttpResponseModel,
            status_code=status.HTTP_201_CREATED,
            description="Upload a new post to the forum",
            tags = ['user post'],
            responses={
                status.HTTP_201_CREATED:{
                    "model": HttpResponseModel,
                    "description": "Successfully created a new post"
                },
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE:{
                    "model": HttpResponseModel,
                    "description": "Image file type unsupported"
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR:{
                    "model": HttpResponseModel,
                    "description": "Error in creating post"
                }
            })
async def create_post(post: NewPost) -> HttpResponseModel:
    '''
    Create/Upload a post on the forum
    Parameters:
    - post: The post and its contents.
    - image (Optional): The image file attached to the post.

    Returns:
    - The newly created post.

    Raises:
    - HTTPException 415: If the type of the sent file isn't a JPEG or a PNG
    - HTTPException 500: If the server can't generate a unique id for the post.
    '''
    post_create_response = ItemService.create_post(post.assemble())
    return post_create_response