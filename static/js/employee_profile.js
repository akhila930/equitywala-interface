// ... existing code ...

function deleteDocument(documentId) {
    if (confirm('Are you sure you want to delete this document?')) {
        fetch(`/delete-document/${documentId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to delete document');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Remove the document card from the UI
                const docCard = document.querySelector(`[data-document-id="${documentId}"]`);
                if (docCard) {
                    docCard.remove();
                }
                showAlert('Document deleted successfully', 'success');
            } else {
                showAlert('Failed to delete document', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Failed to delete document', 'error');
        });
    }
}

// Helper function to show alerts
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// ... existing code ...