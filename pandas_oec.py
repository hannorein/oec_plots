import glob
import xml.etree.ElementTree as ET
import copy

import pandas as pd

def oec_planets_dataframe(oec_filepath):
    """
    Build a dataframe out of all available planets.
    
    Parameters
    ----------
    oec_filepath: string
      The path to the open exoplanet catalogue checkout.
    
    Return:
      All planets as pandas.DataFrame object.
    """

    data = []
    for fname in glob.glob(oec_filepath + "/systems/*.xml"):
        system = ET.parse(open(fname, "r"))

        base_row = {}

        stars = system.findall('.//star')
        if stars:
            star = stars[0]
            star_name = star.findtext('./name')
            star_temperature = float(star.findtext('./temperature')) if star.findtext('./temperature') else None
            star_mass = float(star.findtext('./mass')) if star.findtext('./mass') else None
            base_row['star_name'] = star_name
            base_row['star_temperature'] = star_temperature
            base_row['star_mass'] = star_mass

        planets = system.findall('.//planet')

        for planet in planets:
            try:
                row = copy.copy(base_row)

                row['mass'] = float(planet.findtext("./mass")) if planet.findtext("./mass") else None
                row['semimajoraxis'] = float(planet.findtext("./semimajoraxis")) if planet.findtext("./semimajoraxis") else None
                row['discoverymethod'] = planet.findtext("./discoverymethod")
                row['name'] = planet.findtext("./name")    
                row['discoveryyear'] = int(planet.findtext("./discoveryyear")) if planet.findtext("./discoveryyear") else 1900
                # TODO Add more of the possible planet properties.
               
                data.append(row)
            except TypeError:
                pass

    df = pd.DataFrame.from_dict(data)

    # Convert the year to dates to have better date support later.
    df['discoveryyear'] = pd.to_datetime(df['discoveryyear'].astype('int'), format='%Y')
    return df

