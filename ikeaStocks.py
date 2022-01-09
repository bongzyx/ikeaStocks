import requests
import json
import datetime
from datetime import datetime, timezone

#This is a forked request, followed by a pull request - Ronald

def getIkeaInfo(item):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json;version=2',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Client-ID': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631',
        'Origin': 'https://www.ikea.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    params = (
        ('itemNos', item['itemCode']),
        ('expand', 'StoresList,Restocks,SalesLocations'),
    )

    response = requests.get(
        'https://api.ingka.ikea.com/cia/availabilities/ru/sg', headers=headers, params=params)

    jsonInfo = json.loads(response.text)

    itemInfo = requests.get(
        "https://www.ikea.com/sg/en/products/803/s59417803.json")

    for loc in jsonInfo['availabilities']:
        if loc['classUnitKey']['classUnitCode'] == '022':
            tampInfo = loc
            loc['storeName'] = "Tampines"
        elif loc['classUnitKey']['classUnitCode'] == '045':
            alexInfo = loc
            loc['storeName'] = "Alexandra"
        elif loc['classUnitKey']['classUnitCode'] == '650':
            jemInfo = loc
            loc['storeName'] = "JEM"

    allStores = [tampInfo, alexInfo, jemInfo]
    outputString = f"-----     {item['itemName']}     -----"
    for store in allStores:
        try:
            outputString += (
                f"\n[{store['storeName']}] {'✅' if store['availableForCashCarry'] else '❌'}")
            if store['availableForCashCarry']:
                stocks = store['buyingOption']['cashCarry']['availability']['quantity']
                updateTime = store['buyingOption']['cashCarry']['availability']['updateDateTime']
                updateTime = datetime.strptime(updateTime, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                    tzinfo=timezone.utc).astimezone(tz=None).strftime("%d-%m-%Y %H:%M:%S")
                outputString += (
                    f"\n   - Stocks: {stocks}\n   - Updated: {updateTime}")
            else:
                if store['buyingOption']['cashCarry']['range']['inRange']:
                    earliestDate = store['buyingOption']['cashCarry']['availability']['restocks'][0]['earliestDate']
                    latestDate = store['buyingOption']['cashCarry']['availability']['restocks'][0]['latestDate']
                    count = store['buyingOption']['cashCarry']['availability']['restocks'][0]['quantity']
                    updateTime = store['buyingOption']['cashCarry']['availability']['restocks'][0]['updateDateTime']
                    updateTime = datetime.strptime(updateTime, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                        tzinfo=timezone.utc).astimezone(tz=None).strftime("%d-%m-%Y %H:%M:%S")
                    reliability = store['buyingOption']['cashCarry']['availability']['restocks'][0]['reliability']
                    type = store['buyingOption']['cashCarry']['availability']['restocks'][0]['type']

                    outputString += (
                        f"\n   - Restock: {earliestDate} to {latestDate}\n   - Units: {count}\n   - Updated {updateTime}\n   - {reliability}; {type}")
        except:
            outputString += "Error"
    outputString += ('\n\n')

    return outputString


def loopAll():
    items = [
        {'itemCode': '90461105', 'itemName': 'MÅLSKYTT Table top'},
        {'itemCode': '80465142', 'itemName': 'ANFALLARE Table top'},
        {'itemCode': '00473551', 'itemName': 'ALEX Drawer unit'},
        {'itemCode': '00217976', 'itemName': 'ADILS Leg'},
        {'itemCode': '10200254', 'itemName': 'SIGNUM Cable trunking'},
    ]
    outputString = ""
    for i in items:
        outputString += getIkeaInfo(i)
    return outputString


if __name__ == "__main__":
    print(loopAll())
