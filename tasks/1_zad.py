import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    primorsky_place = "Приморский район, Санкт-Петербург"

    # Получение границ района
    gdf_primorsky = ox.geocode_to_gdf(primorsky_place)
    primorsky_boundary = gdf_primorsky.geometry.iloc[0]

    # Получение зданий в районе
    tags = {'building': 'yes'}
    primorsky_buildings = ox.geometries.geometries_from_polygon(primorsky_boundary, tags)

    # Получение детских садов
    kindergarten_tags = {'amenity': 'kindergarten'}
    kindergartens = ox.geometries.geometries_from_polygon(primorsky_boundary, kindergarten_tags)

    # Проверка, найдены ли детские сады
    if kindergartens.empty:
        print("Нет детских садов в указанном районе.")
        return

    # Визуализация
    fig, ax = plt.subplots(figsize=(10, 10))

    # Границы района
    gdf_primorsky.plot(ax=ax, color='none', edgecolor='blue', linewidth=2, label='Приморский район')

    # Отображение жилых зданий
    primorsky_buildings.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.6, label='Жилые здания')

    # Отображение детских садов и окружностей
    for idx, row in kindergartens.iterrows():
        # Получаем координаты центра детского сада
        center = row.geometry.centroid

        # Рисуем окружность радиусом 300 метров
        circle = plt.Circle((center.x, center.y), 300, color='blue', fill=False, linestyle='dotted', linewidth=2)
        ax.add_artist(circle)
        ax.scatter(center.x, center.y, color='yellow', s=100, label='Детский сад' if idx == 0 else "")

    plt.legend()
    plt.xlabel('Долгота')
    plt.ylabel('Широта')
    plt.title('Детские сады с окружностями радиусом 300 м в Приморском районе')
    plt.grid()

    plt.axis('equal')  # Соотношение осей для правильного отображения коругностей

    plt.show()

if __name__ == '__main__':
    main()