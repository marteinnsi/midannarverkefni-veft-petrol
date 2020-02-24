from flask import Flask
from flask import render_template
from flask import abort
import requests

# Ég hefði getað unnið þetta mikið betur en átti mjög lítinn tíma svo þetta er svolítið lélégur kóði vona að það afsakist.

class Entry:
    def __init__(self, company, name, bensin95, diesel):
        self.company = company
        self.name = name
        self.bensin95 = bensin95
        self.diesel = diesel


app = Flask(__name__)
petrolJson = requests.get("https://apis.is/petrol").json()
petrolEntries = []

for i in petrolJson["results"]:
    petrolEntries.append(Entry(
        i["company"],
        i["name"],
        i["bensin95"],
        i["diesel"]
    ))

petrolLogo = {
    "N1": "https://www.n1.is/media/13053/n1-logorautt.png",
    "Dælan": "https://www.landsbankinn.is/library/Images/Frettir/2018/Daelan-515.png",
    "Orkan": "data:image/png;base64,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",
    "ÓB": "https://www.olis.is/images/undirsidur/logo/ob_logo_2012_web.jpg",
    "Atlantsolía": "https://www.trottur.is/wp-content/uploads/2013/08/atlantsolia.jpg",
    "Olís": "https://starf.olis.is/storf/storf/images/logo.png",
    "Costco Iceland": "https://dividendvaluebuilder.com/wp-content/uploads/2016/04/COST2.jpg",
}

def getStationsUnique():
    stations = set()
    for entry in petrolEntries:
        stations.add(entry.company)
    return stations


def getCheapestStation():
    cheapestPetrolStation = ""
    cheapestPetrolPrice = 7500
    cheapestDieselStation = ""
    cheapestDieselPrice = 7500

    for entry in petrolEntries:
        if entry.bensin95 <= cheapestPetrolPrice:
            cheapestPetrolStation = entry.company
            cheapestPetrolPrice = entry.bensin95
        if entry.diesel <= cheapestDieselPrice:
            cheapestDieselStation = entry.company
            cheapestDieselPrice = entry.diesel

    return {
        "petrol": (cheapestPetrolStation, cheapestPetrolPrice),
        "diesel": (cheapestDieselStation, cheapestDieselPrice)
    }

def getPricePetrol(station):
    for b in petrolEntries:
        if b.company == station:
            return b.bensin95
    return -1

def getPriceDiesel(station):
    for b in petrolEntries:
        if b.company == station:
            return b.diesel
    return -1

def getAllLocations(station):
    locs = []
    for b in petrolEntries:
        if b.company == station:
            locs.append((b.name, b.bensin95, b.diesel))
    return sorted(locs, key=lambda b: b[2]) 
    
global uniqueStations
global cheapestStation

uniqueStations = getStationsUnique()
cheapestStation = getCheapestStation()

@app.route("/")
def route_index():
    return render_template("index.html", 
    cheapest_petrol_station=cheapestStation["petrol"][0],
    cheapest_petrol_price=cheapestStation["petrol"][1],
    cheapest_diesel_station=cheapestStation["diesel"][0],
    cheapest_diesel_price=cheapestStation["diesel"][1],
    stations=uniqueStations,
    station_logos=petrolLogo
    )


@app.route("/stodvar/<bensinstod>")
def route_bensinstod(bensinstod):
    if bensinstod in uniqueStations:
        return render_template("stod.html",
        station=bensinstod,
        station_petrol=getPricePetrol(bensinstod),
        station_diesel=getPriceDiesel(bensinstod),
        stations=uniqueStations,
        station_logos=petrolLogo,
        locations=getAllLocations(bensinstod))
    else:
        abort(404)

@app.errorhandler(404)
def route_404(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
