import aiohttp

API_URL = "https://dragon-soul-values.vercel.app/api/items"

async def buscar_itens():
    async with aiohttp.ClientSession() as session:
        async with session.get (API_URL) as response:
            if response.status != 200:
                print(f"Erro na API: {response.status}")
                return []
            data = await response.json()
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return data.get("items", [])
            return []
        
async def buscar_item_por_nome(nome: str):
    itens = await buscar_itens()
    nome = nome.lower()

    for item in itens:
        item_nome = str(item.get("name", "")).lower()

        if nome in item_nome:
            return item
        
    return None