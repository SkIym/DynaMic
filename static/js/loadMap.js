document.addEventListener('DOMContentLoaded', async function() {
    
    const map = L.map('map').setView([14.650983264532163, 121.06718461639298], 16); // default center
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);

    const data = await fetchOccurrences();
    const blobSize = 20;
    const highlightColor = "#FF2400"
                
    // heat layer, can adjust base intensity
    const baseIntensity = 0.6;
    var heat = L
        .heatLayer(
            data.map((i) => [i.latitude, i.longitude, baseIntensity]), 
            {   
                radius: blobSize,
                minOpacity: 0.4,
                // adjust style of the heat blobs here, see leaflet docs for options
            }
        )
        .addTo(map);

    var markers = L
        .markerClusterGroup
        .withList({
            labelFn: function(el, ei, cluster) {
                return "<p>[" + ei + "] " + el.options.listText + "</p>";
            },
            headerFn: function(els, cluster) {
                return "<p>Explosions within selected cluster: </p>";
            },
            sortFn: function(m1, m2) {
                return m1.options.id > m2.options.id ? 1 : -1;
            },
            showHeader: true,
            sidePanel: true,
            list: true,
            sidePanelWidth: 40,
            showCoverageOnHover: false,
            spiderLegPolylineOptions: {
                weight: 5,
                color: highlightColor,
                opacity: 0.2,
                dashOffset: 10
            },
            maxClusterRadius: blobSize,
            iconCreateFunction: function(cluster) {
                var childCount = cluster.getChildCount()
                var c = ' marker-cluster-';
                if (childCount < 3) {
                    c += 'small';
                } else if (childCount < 5) {
                    c += 'medium';
                } else {
                    c += 'large';
                }
                return new L
                .DivIcon({ 
                    html: '<div><span>' + childCount + '</span></div>', 
                    iconSize: new L.Point(40, 40),
                    className: 'marker-cluster' + c
                });
            }
        })

    // circle markers over heat blobs, shows time and date of the occurrences when clicked
    const allMarkers = [];
    var circleMarkers = data.map((i) => {
        var circle = L
            .circleMarker(
                [i.latitude, i.longitude],
                {
                    opacity: 0,
                    radius: blobSize,
                    weight: 0,
                    fillOpacity: 0,
                    listText: `Date: ${i.date} ------ Time: ${i.time} ----- Lat: ${i.latitude} ----- Lng: ${i.longitude}`
                }
            )
            .bindPopup(
                `<p>Date: ${i.date} <br/> Time: ${i.time} </p>`
                // can add className option here for styling, see leaflet docs
            ) 
            .addTo(map)
        allMarkers.push(circle)
        markers.addLayer(circle)   
    })

    // Add marker groups to map after adding the circle markers
    map.addLayer(markers)

    // Make circle markers opaque upon clicking on parent cluster
    markers.on('clusterclick', (cluster) => {
        resetAllMarkers()
        const childMarkers = cluster.layer.getAllChildMarkers()
        childMarkers.forEach(m => {
            m.setStyle({
                opacity: 0.2,
                weight: 1,
                fillOpacity: 0.2,
                color: highlightColor 
            })

            if (m._renderer) {
                m._renderer._updateCircle(m);
            }
        })
        cluster.layer.spiderfy()
    })

    map.on("click", resetAllMarkers)

    // To reset markers
    function resetAllMarkers() {
        allMarkers.forEach(m => {
            m.setStyle({
                opacity: 0,
                weight: 0,
                fillOpacity: 0
            });
            
            if (m._renderer) {
                m._renderer._updateCircle(m);
            }
        });
        
    }
});
