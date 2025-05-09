let map = null

const form = document.getElementById('form')
form.addEventListener('submit', async function(event) {
    event.preventDefault()
    const formData = new FormData(form)
    console.log(Object.fromEntries(formData))

    const time = formData.get("time")
    let group = parseInt(formData.get("group")) 
    const dateNow = new Date()
    let startDate = ""

    switch (time) {
        case "past-hour":
            startDate = new Date(dateNow.setHours(dateNow.getHours() - 1))
            break;
        case "past-day":
            startDate = new Date(dateNow.setHours(dateNow.getHours() - 24))
            break;
        case "past-week":
            startDate = new Date(dateNow.setHours(dateNow.getHours() - 168))
            break;
        case "past-month":
            startDate = new Date(dateNow.setMonth(dateNow.getMonth() - 1))
            break;
        default:
            startDate = new Date(Date.UTC(0, 0, 0, 0, 0, 0))
            break;
    }
    let startDateISO = startDate.toISOString()
    console.log(startDateISO, group)
    const data = await fetchOccurrences(startDateISO, group)

    // remove layers
    if (map) {
        map = map.remove()
    }
    loadMap(data)
})

async function loadMap(data = null) {

    // initial data
    if (data == null) {
        let startDate = new Date(Date.UTC(0, 0, 0, 0, 0, 0))
        let startDateISO = startDate.toISOString()
        data = await fetchOccurrences(startDateISO, 0)
    }
    
    // initial map
    if (map==null) {
        map = L.map('map').setView([14.650983264532163, 121.06718461639298], 12); // default center
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(map);
    }
    

    const blobSize = 20;
    const highlightColor = "#FF2400"
                
    // heat layer, can adjust base intensity
    const baseIntensity = 0.9;
    let heat = L
        .heatLayer(
            data.map((i) => [i.latitude, i.longitude, baseIntensity]), 
            {   
                radius: blobSize,
                minOpacity: 0.7,
                // adjust style of the heat blobs here, see leaflet docs for options
            }
        )
        .addTo(map);

    let markers = L
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
                let childCount = cluster.getChildCount()
                let c = ' marker-cluster-';
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
    let circleMarkers = data.map((i) => {
        let circle = L
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
}
