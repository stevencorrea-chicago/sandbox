import './App.css';
import { useState, useEffect } from 'react';

function App() {
  const [formData, setFormData] = useState({
    title: "",
    author: "",
    year: "",
    country: "",
    language: ""
  });
  
  const [results, setResults] = useState([]);

  useEffect(() => {
  fetch("http://localhost:8000/books")
    .then(res => res.json())
    .then(data => {
      setResults(data);   // your table state
    })
    .catch(err => console.error("Error loading books:", err));
}, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

const handleSubmit = (e) => {
  e.preventDefault();
  searchBooks();   // <-- trigger search instead of POST
};

  const searchBooks = () => {
    const params = new URLSearchParams();

    if (formData.title) params.append("title", formData.title);
    if (formData.author) params.append("author", formData.author);
    if (formData.year) params.append("year", formData.year);
    if (formData.country) params.append("country", formData.country);
    if (formData.language) params.append("language", formData.language);

    fetch(`http://localhost:8000/books/search?${params.toString()}`)
      .then(res => res.json())
      .then(data => {
        setResults(data);
      })
      .catch(err => console.error("Search error:", err));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Book Information</h2>

        <form className="form-container" onSubmit={handleSubmit}>
          <label>
            Title:
            <input type="text" name="title" value={formData.title} onChange={handleChange} />
          </label>

          <label>
            Author:
            <input type="text" name="author" value={formData.author} onChange={handleChange} />
          </label>

          <label>
            Year:
            <input type="number" name="year" value={formData.year} onChange={handleChange} />
          </label>

          <label>
            Country:
            <input type="text" name="country" value={formData.country} onChange={handleChange} />
          </label>

          <label>
            Language:
            <input type="text" name="language" value={formData.language} onChange={handleChange} />
          </label>

          <button type="submit" className="submit-button">Submit</button>
        </form>

        <h2>Results</h2>

        <table className="results-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Author</th>
              <th>Year</th>
              <th>Country</th>
              <th>Language</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row) => (
              <tr key={row.id}>
                <td>{row.title}</td>
                <td>{row.author}</td>
                <td>{row.year}</td>
                <td>{row.country}</td>
                <td>{row.language}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <p className="note">
          Submit button added — ready for backend integration.
        </p>
      </header>
    </div>
  );
}

export default App;