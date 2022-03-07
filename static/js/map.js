ymaps.ready(init);

function init() {
    var map = new ymaps.Map("map", {
        center: [51.656677, 39.206890],
        zoom: 16
    });
    map.geoObjects.add(new ymaps.Placemark([51.656677, 39.206890]));
}