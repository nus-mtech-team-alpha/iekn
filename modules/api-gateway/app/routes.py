from fastapi import APIRouter, Request

router = APIRouter()

@router.get('/callback')
async def hello_world():
    return {"message": "hello world!"}

@router.api_route('/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE'])
async def proxy(path: str, request: Request):
    import requests
    url = f'http://example-service/{path}'
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers.items() if key != 'host'},
        data=await request.body(),
        cookies=request.cookies,
        allow_redirects=False)

    return response.content, response.status_code, response.headers.items()