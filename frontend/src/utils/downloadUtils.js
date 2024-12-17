// downloadUtils.js
export const downloadFile = async (url, filename) => {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'text/calendar',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        // Clean up the URL object
        setTimeout(() => {
            window.URL.revokeObjectURL(downloadUrl);
        }, 100);
        
        return true;
    } catch (error) {
        console.error('Download failed:', error);
        throw error;
    }
};