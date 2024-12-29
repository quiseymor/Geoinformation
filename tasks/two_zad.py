import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    kalininskiy_place = "Калининский район, Санкт-Петербург"
    krasnogvardeyskoe_place = "Красногвардейский район, Санкт-Петербург"

    gdf_kalininskiy = ox.geocode_to_gdf(kalininskiy_place)
    gdf_krasnogvardeyskiy = ox.geocode_to_gdf(krasnogvardeyskoe_place)

    #  границы
    kalininskiy_boundary = gdf_kalininskiy.geometry.iloc[0]
    krasnogvardeyskiy_boundary = gdf_krasnogvardeyskiy.geometry.iloc[0]

    # Получение зданий в районах
    tags = {'building': True}
    kalininskiy_buildings = ox.geometries.geometries_from_polygon(kalininskiy_boundary, tags)
    krasnogvardeyskiy_buildings = ox.geometries.geometries_from_polygon(krasnogvardeyskiy_boundary, tags)

    # фильтр промышленных 
    industrial_buildings_kalininskiy = kalininskiy_buildings[kalininskiy_buildings['building'].isin(['industrial', 'factory'])]
    residential_buildings_kalininskiy = kalininskiy_buildings[kalininskiy_buildings['building'] == 'yes']
    # фильтр жилых
    industrial_buildings_krasnogvardeyskiy = krasnogvardeyskiy_buildings[krasnogvardeyskiy_buildings['building'].isin(['industrial', 'factory'])]
    residential_buildings_krasnogvardeyskiy = krasnogvardeyskiy_buildings[krasnogvardeyskiy_buildings['building'] == 'yes']

    # вокруг промышленных зданий (1000 м)
    buffer_kalininskiy = industrial_buildings_kalininskiy.buffer(1000)
    buffer_krasnogvardeyskiy = industrial_buildings_krasnogvardeyskiy.buffer(1000)

    residential_within_kalininskiy = residential_buildings_kalininskiy[
        residential_buildings_kalininskiy.geometry.intersects(buffer_kalininskiy.unary_union)
    ]

    residential_within_krasnogvardeyskiy = residential_buildings_krasnogvardeyskiy[
        residential_buildings_krasnogvardeyskiy.geometry.intersects(buffer_krasnogvardeyskiy.unary_union)
    ]

    fig, ax = plt.subplots(figsize=(10, 10))

    #  границы
    gdf_kalininskiy.plot(ax=ax, color='none', edgecolor='blue', linewidth=2, label='Калининский район')
    gdf_krasnogvardeyskiy.plot(ax=ax, color='none', edgecolor='green', linewidth=2, label='Красногвардейский район')

    if not residential_within_kalininskiy.empty:
        residential_within_kalininskiy.plot(ax=ax, color='red', label='Жилые здания (Калининский район) в санитарно-защитной зоне')
    if not residential_within_krasnogvardeyskiy.empty:
        residential_within_krasnogvardeyskiy.plot(ax=ax, color='orange', label='Жилые здания (Красногвардейский район) в санитарно-защитной зоне')

    plt.legend()
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.title('Жилые здания в санитарно-защитных зонах промышленных предприятий')
    plt.grid()

    plt.show()

if __name__ == '__main__':
    main()