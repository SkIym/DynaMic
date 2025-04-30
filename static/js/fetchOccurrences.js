async function fetchOccurrences() {
    try {
        const response = await fetch("/occurrences")
        const data = await response.json()
        
        console.log(data)
        return data
    }
    catch (error) {
        console.error("Error fetching occurrences:", error)
    }
}