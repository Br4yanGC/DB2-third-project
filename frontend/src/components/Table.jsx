const Table = ({ data }) => {
  if (!data.pictures) {
    // Render a loading state or a message indicating that the data is being fetched
    return <p>Loading...</p>;
  }

  return (
    <div className="table-responsive w-75 mx-auto">
      <table className="table align-middle table-striped">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Filename</th>
            <th scope="col">Score</th>
          </tr>
        </thead>
        <tbody>
          {data.pictures.map((picture, index) => (
            <tr key={index}>
              <th scope="row">{index + 1}</th>
              <td>
                <a href={`src/assets/lfw/${picture.filename}`} target="_blank" rel="noopener noreferrer">
                  {picture.filename}
                </a>
              </td>
              <td>{picture.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p>Execution Time: {data.execution_time} ms</p>
    </div>
  );
};

export default Table;