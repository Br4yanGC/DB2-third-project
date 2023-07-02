import React, { useState } from 'react'

const Input = ({ type, onSubmit }) => {
  const [numberValue, setNumberValue] = useState('');
  const [imageFile, setImageFile] = useState(null);

  const handleNumberChange = (e) => {
    setNumberValue(e.target.value);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImageFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('typeValue', type);
    formData.append('numberValue', numberValue);
    formData.append('imageFile', imageFile);

    try {
      const response = await fetch('http://127.0.0.1:5000/send-input', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        // Handle the response from the backend
        console.log(data);
        // Call the onSubmit function passed from the parent component
        onSubmit();
      } else {
        // Handle the case where the request was not successful
        console.error('Request failed with status:', response.status);
      }
    } catch (error) {
      // Handle any error that occurs during the request
      console.error(error);
    }
  };
  
  return (
    <form className="container text-center" onSubmit={handleSubmit}>
      <div className="row justify-content-md-center">
        <div className="col col-lg-8">
          <label htmlFor="typeNumber" className="form-label">Insert {type == 'knn' ? 'the top-k' : 'a radius'} value</label>
          <input 
            className="form-control" 
            type="number" 
            id="inputNumber" 
            value={numberValue}
            onChange={handleNumberChange}
          />
        </div>
      </div>

      <div className="row justify-content-md-center">
        <div className="col col-lg-8">
          <label htmlFor="formFile" className="form-label">Load an image</label>
          <input 
            className="form-control"
            type="file"
            id="formFile"
            onChange={handleImageChange}
          />
        </div>
      </div>
      <button type="submit" className="btn btn-primary px-4 m-3">Submit</button>
    </form>
  )
}

export default Input
