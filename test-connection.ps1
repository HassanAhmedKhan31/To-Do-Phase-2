# Function to test the backend connection
function Test-BackendConnection {
    param (
        [string]$url,
        [int]$retries = 5,
        [int]$delay = 2
    )

    for ($i = 1; $i -le $retries; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $url -UseBasicParsing -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-Host "Backend is running and accessible at $url"
                return $true
            }
        }
        catch {
            Write-Host "Attempt $i of ${retries}: Backend not accessible at $url. Retrying in $delay seconds..."
            Start-Sleep -Seconds $delay
        }
    }

    Write-Error "Failed to connect to backend at $url after $retries attempts."
    return $false
}

# URL to test
$backendUrl = "http://127.0.0.1:8000/docs"

# Test the connection
if (Test-BackendConnection -url $backendUrl) {
    Write-Host "Connection to backend successful."
}
else {
    Write-Host "Could not connect to backend."
}
