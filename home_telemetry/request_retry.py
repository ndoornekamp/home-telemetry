import httpx


async def requests_retry_get_async(url) -> httpx.Response:
    transport = httpx.AsyncHTTPTransport(retries=2)
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(url)

    return response
