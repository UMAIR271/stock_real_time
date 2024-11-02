import asyncio
import aiohttp
import ssl
import json
import time
from zeep import AsyncClient, Settings
from zeep.cache import SqliteCache
from zeep.transports import AsyncTransport


async def create_async_client():
    """
    Initializes and returns an asynchronous Zeep client for the web service.
    """
    # Define the WSDL URL for the SOAP web service
    wsdl_url = 'http://csp.cell-data.it/wsCellData.asmx?WSDL'
    # Create an SSL context with disabled hostname checking and verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    # Create an aiohttp TCP connector with the custom SSL context
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    # Set a timeout limit for HTTP requests
    timeout = aiohttp.ClientTimeout(total=30)
    # Initialize a client session with the defined timeout and connector
    session = aiohttp.ClientSession(timeout=timeout, connector=connector)
    # Initialize an asynchronous transport layer with SQLite caching for WSDL
    transport = AsyncTransport(cache=SqliteCache(path='./wsdl_cache.db'))
    # Assign the client session to the transport layer manually
    transport.client_session = session
    # Prevent the transport layer from closing the session automatically
    transport._close_session = False
    # Disable strict mode in Zeep settings for more lenient XML handling
    settings = Settings(strict=False, xml_huge_tree=True)
    # Create an asynchronous client for the SOAP service with custom settings and transport
    client = AsyncClient(wsdl=wsdl_url, transport=transport, settings=settings)
    return client, session

async def get_metals_data_async(client, metal_price_type):
    """
    Asynchronously retrieves metals data using the SOAP service.
    """
    try:
        # Measure start time for the request
        start_time = time.time()
        # Perform an asynchronous SOAP request with the specified metal price type
        response = await client.service.getTestMetals(metal_price_type)
        # Calculate the response time
        response_time = time.time() - start_time
        # Log the response time and data for debugging
        print(f"Response from getTestMetals('{metal_price_type}'):")
        print(response)
        print(f"Response time for '{metal_price_type}': {response_time:.2f} seconds")
        # Parse the JSON response into a Python dictionary
        data = json.loads(response)
        return metal_price_type, data
    except Exception as e:
        # Handle exceptions and log errors
        print(f"An error occurred in get_metals_data_async('{metal_price_type}'): {e}")
        return metal_price_type, None


async def main():
    # Initialize the SOAP client and session asynchronously
    # client, session = await create_async_client()

    try:
        while True:
            # Define metal price types to be fetched
            # metal_price_types = ['rtmet', 'rtmet3M', 'offdoll', 'offeurolme']
            metal_price_types = ['rtmet','offdoll']
            # Prepare asynchronous tasks for fetching each metal price type
            # tasks = [get_metals_data_async(client, metal_price_type) for metal_price_type in metal_price_types]
            # Execute all tasks concurrently and wait for all to complete
            # results = await asyncio.gather(*tasks)

            # Sample data, structured as tuples inside a list
            results = [
                ('rtmet', {
                    'items': [
                        {'ask': 2244.0, 'aske': 2067.33, 'bid': 2234.0, 'bide': 2058.11,
                         'datequote': '31/10/2024 08:30:00', 'metalcode': 'AA-C'},
                         {'ask': 2211221214.0, 'aske': 2067.33, 'bid': 2234.0, 'bide': 2058.11,
                         'datequote': '31/10/2024 08:30:00', 'metalcode': 'AA-C'},
                        {'ask': 2589.0, 'aske': 2385.16, 'bid': 2588.5, 'bide': 2384.7,
                         'datequote': '31/10/2024 16:45:52', 'metalcode': 'AL-C'},
                        {'ask': 9383.0, 'aske': 8644.26, 'bid': 9381.5, 'bide': 8642.88,
                         'datequote': '31/10/2024 16:45:55', 'metalcode': 'CU-C'},
                        {'ask': 15484.49, 'aske': 14265.37, 'bid': 15474.49, 'bide': 14256.16,
                         'datequote': '31/10/2024 16:42:58', 'metalcode': 'NI-C'},
                        {'ask': 1965.5, 'aske': 1810.75, 'bid': 1964.5, 'bide': 1809.83,
                         'datequote': '31/10/2024 16:45:45', 'metalcode': 'PB-C'},
                        {'ask': 30837.0, 'aske': 28409.15, 'bid': 30747.0, 'bide': 28326.24,
                         'datequote': '31/10/2024 16:45:28', 'metalcode': 'SN-C'},
                        {'ask': 3033.75, 'aske': 2794.9, 'bid': 3032.25, 'bide': 2793.52,
                         'datequote': '31/10/2024 16:45:50', 'metalcode': 'ZN-C'}
                    ],
                    'title': 'List of metals quotations',
                    'type': 'real time'
                }),
                ('offdoll', {
                    'items': [
                        {'ask': 23445.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 2243.0, 'aske': 0, 'bid': 2234.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 2644.0, 'aske': 0, 'bid': 2642.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AL-C'},
                        {'ask': 2617.5, 'aske': 0, 'bid': 2617.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AL-C'},
                        {'ask': 9557.0, 'aske': 0, 'bid': 9556.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'CU-3M'},
                        {'ask': 3255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 4255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 5255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 6255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 7255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        {'ask': 8255.0, 'aske': 0, 'bid': 2245.0, 'bide': 0, 'datequote': '2024-10-31',
                         'metalcode': 'AA-C'},
                        #  {'ask': 1111.0, 'aske': 0, 'bid': 223.0, 'bide': 0, 'datequote': '2024-10-31',
                        #  'metalcode': 'AA-C'}
                    ],
                    'title': 'List of metals quotations',
                    'type': 'official'
                })
            ]

            if results:
                return results

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print(f"success:")
        # Clean up: close the SOAP transport and HTTP session
        # await client.transport.aclose()
        # await session.close()

if __name__ == "__main__":
    # Execute the main function asynchronously
    asyncio.run(main())
