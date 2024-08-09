import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchHistoryModal.css';

const SearchHistoryModal = ({ userId, onClose }) => {
  const [searchHistory, setSearchHistory] = useState([]);
  const [expandedIndex, setExpandedIndex] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSearchHistory = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/search-history', { user_id: userId });
        if (response.data.success) {
          setSearchHistory(response.data.history);
        } else {
          setError('An error occurred while fetching search history.');
        }
      } catch (error) {
        console.error('Error fetching search history', error);
        setError('An error occurred while fetching search history.');
      }
    };

    fetchSearchHistory();
  }, [userId]);

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Search History</h2>
        {error ? (
          <p className="error-message">{error}</p>
        ) : searchHistory.length === 0 ? (
          <p>No search history available.</p>
        ) : (
          <div className="search-history-list">
            {searchHistory.map((search, index) => (
              <div key={index} className="search-item">
                <div className="search-header" onClick={() => toggleExpand(index)}>
                  <span>{search.search_query}</span>
                  <span>{search.search_date}</span>
                </div>
                {expandedIndex === index && (
                  <div className="recommended-courses">
                    {search.recommended_courses.length === 0 ? (
                      <p>No recommended courses for this search.</p>
                    ) : (
                      <ul>
                        {search.recommended_courses.map((course, courseIndex) => (
                          <li key={courseIndex}>
                            {course.course_title} ({course.course_id}) - {course.campus}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
        <div className="modal-actions">
          <button className="clear-history-button" onClick={() => axios.post('http://127.0.0.1:5000/api/clear-search-history', { user_id: userId }).then(() => setSearchHistory([]))}>
            Clear Search History
          </button>
          <button className="close-button" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default SearchHistoryModal;