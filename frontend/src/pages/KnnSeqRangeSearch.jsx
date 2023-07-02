import React, { useState } from 'react';
import Table from '../components/Table';
import Input from '../components/Input';

const KnnSeqRangeSearch = () => {
  const [data, setData] = useState({ pictures: [], execution_time: 0 });
  const [isLoading, setIsLoading] = useState(false);

  const handleFormSubmit = async () => {
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/knn-seq-range-search');
      if (response.ok) {
        const data = await response.json();
        setData(data);
      } else {
        console.error('Request failed with status:', response.status);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <p className='fs-1 text-center'>KnnSeqRangeSearch</p>
      <Input type={'range'} onSubmit={handleFormSubmit} />
      {isLoading ? (
        <p className="text-center">Loading...</p>
      ) : data.pictures.length > 0 || data.execution_time ? (
        <div>
          <p className="fs-2 text-center">Results</p>
          <Table data={data} />
        </div>
      ) : null}
    </div>
  );
};

export default KnnSeqRangeSearch;