async function fetchOccurrences(time = 'all-time', group = 1) {
    try {
        const response = await fetch(`/occurrences?time=${time}&group=${group}`)
        const data = await response.json()
        
        console.log(data)
        return data
    }
    catch (error) {
        console.error("Error fetching occurrences:", error)
    }
}