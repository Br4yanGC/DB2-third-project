import React from 'react';
import banner from '../assets/img0.gif';

const Home = () => {
  const members = [
    'Chancan Chanca, Sanders',
    'Gomero Castillo, Brayan Eduardo',
    'Yupanqui López, Milagros Valeria',
    'Zapata Gallegos, Neo Marcelo',
  ];

  return (
    <div className="d-flex justify-content-center align-items-start vh-100 px-5">
      <div className="text-center mt-5">
        <img src={banner} alt="banner" style={{ marginTop: '50px' }} />
        <p className="fs-4 mt-3">
          "Yesterday is history, tomorrow is a mystery, but today is a gift. That's why it's called the present."
        </p>
        <div className="fs-5 mt-3 text-start">
          <p>Members:</p>
          <ul className="list-unstyled">
            {members.map((member, index) => (
              <li key={index} style={{ listStylePosition: 'inside' }}>
                - {member}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Home;
