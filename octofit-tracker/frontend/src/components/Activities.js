import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/activities/`
    : '/api/activities/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Activities endpoint:', endpoint);
        console.log('Fetched activities:', results);
      });
  }, [endpoint]);

  return (
    <div className="container mt-4">
      <div className="card">
        <div className="card-body">
          <h2 className="card-title mb-4">Activities</h2>
          <div className="table-responsive">
            <table className="table table-striped table-hover">
              <thead className="table-dark">
                <tr>
                  <th>#</th>
                  <th>Type</th>
                  <th>Duration (min)</th>
                  <th>Date</th>
                  <th>User</th>
                </tr>
              </thead>
              <tbody>
                {activities.map((a, i) => (
                  <tr key={a.id || i}>
                    <td>{i + 1}</td>
                    <td>{a.type}</td>
                    <td>{a.duration}</td>
                    <td>{a.date}</td>
                    <td>{a.user && a.user.username ? a.user.username : ''}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Activities;
