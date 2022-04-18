import pandas as pd
import requests
import os




def make_df(endpoint):
    '''
    This function will make a dataframe out of any of the defined endpoints. It takes 
    the endpoint with the host+api and generates the data until the next_page is a NoneType.
    It then converts all the data into a dataframe and returns it.
    '''
    if endpoint in ['sales', 'items', 'stores']:
        # Set up the domain as the host and the api
        host = 'https://api.data.codeup.com'
        api = '/api/v1/'
        # Set up the url to be the host, api, and endpoint
        url = host + api + endpoint
        # Set the response using the requests import
        response = requests.get(url)
        # Create an if statement that that sorts through the pages
        if response:
            # Define payload
            payload = response.json()['payload']
            # Set all_the_things of whatever is up above
            all_the_things = payload[endpoint]
            # Make whatever endpoint into a datafame
            df = pd.DataFrame(all_the_things)
            # Define next page to grab
            next_page = payload['next_page']
            # Use a 'next page' = True 
            while next_page:
                # Define the url for that page as the next page
                url = host + next_page
                # Print the url of the next page
                # Set the response
                response = requests.get(url)
                # Define the payload again
                payload = response.json()['payload']
                # Define next page to grab
                next_page = payload['next_page'] 
                # Set all_the_things of whatever is up above
                all_the_things = payload[endpoint]
#                 # Print out what page is being currently fetched
#                 print(f'\rFetching Page {data["payload"]["page"]} of {data["payload"]["max_page"]}: {url}', end='')
                # Make it into a dataframe
                df = pd.concat([df, pd.DataFrame(all_the_things)])
    
    return df


def get_items(usecache=True):
    """IF usecache is True, then the function will return the cached data. 
    Otherwise, it will make a request to the API and return the data."""
    filename = "items.csv"
    if usecache and os.path.exists(filename):
        print("Using cached data")
        return pd.read_csv(filename)
    print("Making request to API")
    domain = "https://api.data.codeup.com/"
    endpoint = "/api/v1/items"
    items = []
    url = domain + endpoint
    response = requests.get(url)
    data = response.json()
    items.extend(data["payload"]["items"])
    while data["payload"]["next_page"]:
        url = domain + data["payload"]["next_page"]
        response = requests.get(url)
        data = response.json()
        items.extend(data["payload"]["items"])
    df = pd.DataFrame(items)
    print("Writing data to csv")
    df.to_csv(filename, index=False)
    return pd.DataFrame(df)


def get_stores(usecache=True):
    '''IF usecache is True, then the function will return the cached data. 
    Otherwise, it will make a request to the API and return the data.'''
    filename = 'stores.csv'
    if usecache and os.path.exists(filename):
        print('Using cached data')
        return pd.read_csv(filename)
    print('Making request to API')
    domain = 'https://api.data.codeup.com/'
    endpoint = '/api/v1/stores'
    stores = []
    url = domain + endpoint
    response = requests.get(url)
    data = response.json()
    stores.extend(data['payload']['stores'])
    while data['payload']['next_page']:
        url = domain + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        stores.extend(data['payload']['stores'])
    df = pd.DataFrame(stores)
    print('Writing data to csv')
    df.to_csv(filename, index=False)
    return pd.DataFrame(df)


def get_sales(usecache=True):
    '''IF usecache is True, then the function will return the cached data. 
    Otherwise, it will make a request to the API and return the data.'''
    filename = 'sales.csv'
    if usecache and os.path.exists(filename):
        print('Using cached data')
        return pd.read_csv(filename)
    print('Making request to API')
    domain = 'https://api.data.codeup.com/'
    endpoint = '/api/v1/sales'
    sales = []
    url = domain + endpoint
    response = requests.get(url)
    data = response.json()
    sales.extend(data['payload']['sales'])
    while data['payload']['next_page']:
        url = domain + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        sales.extend(data['payload']['sales'])
    df = pd.DataFrame(sales)
    print('Writing data to csv')
    df.to_csv(filename, index=False)
    return pd.DataFrame(df)


def get_all_data():
    '''This function will get all the data from the API.'''
    items = get_items()
    stores = get_stores()
    sales = get_sales()
    df = pd.merge(sales, stores, how = 'inner', left_on = 'store', right_on='store_id')
    df = pd.merge(df, items, how = 'inner', left_on = 'item', right_on='item_id')
    return df


def get_opsd():
    filename = 'opsd.csv'
    if os.path.exists(filename):
        print('Reading from .csv')
        return pd.read_csv(filename)
    print('Getting a fresh copy of the data')
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    df.to_csv(filename, index=False)
    return df