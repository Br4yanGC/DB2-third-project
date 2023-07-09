import React from 'react'
import Live from '../assets/img1.gif';

const KnnKDTreeKnnSearchLive = () => {
  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/knn-kdtree-knn-search-live');
      if (response.ok) {
        console.log('Backend function executed successfully');
      } else {
        console.error('Failed to execute backend function');
      }
    } catch (error) {
      console.error('An error occurred while executing backend function:', error);
    }
  };
  
  return (
    <div className="d-flex flex-column justify-content-center align-items-center vh-50 px-5">
      <p className='fs-1 text-center'>KnnKDTreeKnnSearchLive</p>
      <div className="text-center">
        <img src={Live} alt="banner" className="img-fluid" style={{ width: '600px', height: 'auto' }} />
        <p className="fs-4 mt-3" style={{ width: '800px' }}>
          We have a database with pictures from different people, most of them famous. 
          Take a look and discover who of all those people is the most similar to you.
        </p>
      </div>
      <button className="btn btn-primary mt-3" onClick={handleButtonClick}>Knn search on live</button>
    </div>
  );
}

export default KnnKDTreeKnnSearchLive