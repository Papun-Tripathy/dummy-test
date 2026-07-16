import React, { useState, useEffect } from 'react';

export default function ItemList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // FIX: Add empty dependency array to run effect only once on mount
    fetch('/items')
      .then(res => {
        // FIX: Check for HTTP errors
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        // FIX: Validate data structure before setting state
        if (Array.isArray(data)) {
          setItems(data);
        } else {
          console.error('Fetched data is not an array:', data);
          setError(new Error('Received invalid data from server.'));
          setItems([]); // Default to empty array if data is invalid
        }
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching items:", err); // Log the actual error
        setError(err); // Store the error object
        setLoading(false);
      });
  }, []); // FIX: Added empty dependency array to prevent infinite loop

  const deleteItem = (id) => {
    // The fetch URL and method are generally correct for REST DELETE operations.
    // Add robust error handling for the delete operation.
    fetch(`/items/${id}`, { method: 'DELETE' })
      .then(res => {
        if (!res.ok) {
          throw new Error(`Failed to delete item. Status: ${res.status}`);
        }
        // For a successful DELETE, the backend might return 200 OK with no body, or 204 No Content.
        // We don't necessarily need to parse JSON. Just check success.
        // If the backend returns JSON on delete, you'd parse it here.
        return res.text(); // Consume the body if any, to avoid "body stream already read" warnings
      })
      .then(() => {
        // FIX: Update state immutably by filtering out the deleted item
        setItems(prevItems => prevItems.filter(item => item.id !== id));
      })
      .catch(err => {
        console.error("Error deleting item:", err);
        // Optionally, display a user-friendly error message, e.g., using a toast notification
        // For this example, we'll just log and update the general error state.
        setError(new Error(`Failed to delete item: ${err.message}`));
      });
  };

  if (loading) return <div>Loading items...</div>;
  // FIX: Display a more informative error message
  if (error) return <div style={{ color: 'red' }}>Error loading items: {error.message}</div>;

  return (
    <div>
      <h1>Store Items</h1>
      <ul>
        {items.map(item => (
          // FIX: Add unique key prop for each list item
          <li key={item.id}>
            {item.name} - ${item.price ? item.price.toFixed(2) : 'N/A'} {/* FIX: Add check for item.price */}
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {items.length === 0 && !loading && !error && (
        <p>No items found.</p>
      )}
    </div>
  );
}