import httpx


async def requests_retry_get_async(url: str) -> httpx.Response:
    transport = httpx.AsyncHTTPTransport(retries=2)
    async with httpx.AsyncClient(transport=transport) as client:
        return await client.get(url)
