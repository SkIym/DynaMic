async function fetchOccurrences(iso_start_date = "", group = 0) {
    try {

        const response = await fetch("/occurrences?" + new URLSearchParams({
                iso_start_date: iso_start_date,
                group: group
            })
        )

        const data = await response.json()
        
        console.log(new URLSearchParams({
            iso_start_date: iso_start_date,
            group: group
        }))
        return data
    }
    catch (error) {
        console.error("Error fetching occurrences:", error)
    }
}