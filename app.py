from flask import Flask
from flask import render_template
from flask import abort
import requests

# Ég hefði getað unnið þetta mikið betur en átti mjög lítinn tíma svo þetta er svolítið lélégur kóði vona að það afsakist.

class Entry:
    def __init__(self, company, bensin95, diesel):
        self.company = company
        self.bensin95 = bensin95
        self.diesel = diesel


app = Flask(__name__)
petrolJson = requests.get("https://apis.is/petrol").json()
petrolEntries = []

for i in petrolJson["results"]:
    petrolEntries.append(Entry(
        i["company"],
        i["bensin95"],
        i["diesel"]
    ))

petrolLogo = {
    "N1": "https://www.n1.is/media/13053/n1-logorautt.png",
    "Dælan": "https://www.landsbankinn.is/library/Images/Frettir/2018/Daelan-515.png",
    "Orkan": "https://lh3.googleusercontent.com/proxy/RmcIhYMDY3_kTvgI_Pb_klCAtAPfIl3NA24R7zDFr5YGzfQj-DYPivCgjD8PUhpQ2pi2ghJcmJZXVEXhUtvQxp6p7_1fnfSHInI9S1yYNlDlwA",
    "ÓB": "https://www.olis.is/images/undirsidur/logo/ob_logo_2012_web.jpg",
    "Atlantsolía": "https://www.trottur.is/wp-content/uploads/2013/08/atlantsolia.jpg",
    "Olís": "https://starf.olis.is/storf/storf/images/logo.png",
    "Costco Iceland": "https://dividendvaluebuilder.com/wp-content/uploads/2016/04/COST2.jpg",
}

def getStations():
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
    

uniqueStations = getStations()
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
        station_logos=petrolLogo)
    else:
        abort(404)

@app.errorhandler(404)
def route_404(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
