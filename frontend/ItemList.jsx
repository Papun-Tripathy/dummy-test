import React, { useState, useEffect } from 'react';

export default function ItemList() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // BUG: Missing dependency array / infinite loop fetching
    fetch('/items')
      .then(res => res.json())
      .then(data => {
        // BUG: Directly assigning list without validation (might crash if not an array)
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }); // BUG: No [] array here!

  const deleteItem = (id) => {
    // BUG: Typos in api url path or incorrect fetch parameter structure
    fetch(`/items/${id}`, { method: 'DELETE' })
      .then(res => res.json())
      .then(result => {
        // BUG: Directly modifying local state incorrectly
        items.splice(items.findIndex(item => item.id === id), 1);
        setItems(items); // React won't re-render because reference is the same!
      });
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error loading items</div>;

  return (
    <div>
      <h1>Store Items</h1>
      <ul>
        {items.map(item => (
          // BUG: Missing key prop in map loop
          <li>
            {item.name} - ${item.price.toFixed(2)}
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
