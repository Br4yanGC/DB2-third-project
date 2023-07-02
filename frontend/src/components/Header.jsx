import React from 'react'

const Header = () => {
  return (
    <nav className="navbar navbar-expand-lg bg-body-tertiary px-5">
      <div className="container-fluid">

        <a className="navbar-brand" href="#">Navbar</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
          <ul className="navbar-nav ml-auto mr-3">
            <li className="nav-item">
              <a className="nav-link active" aria-current="page" href="/">Home</a>
            </li>
            
            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Knn-Sequential
              </a>
              <ul className="dropdown-menu">
                <li><a className="dropdown-item" href="/knn-seq-range-search">Range search</a></li>
                <li><a className="dropdown-item" href="/knn-seq-knn-search">Knn search</a></li>
              </ul>
            </li>

            <li className="nav-item dropdown">
              <a className="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Knn-RTree
              </a>
              <ul className="dropdown-menu">
                <li><a className="dropdown-item" href="/knn-rtree-range-search">Range search</a></li>
                <li><a className="dropdown-item" href="/knn-rtree-knn-search">Knn search</a></li>
              </ul>
            </li>

            <li className="nav-item">
              <a className="nav-link" aria-current="page" href="/knn-kdtree-knn-search">Knn-KdTree</a>
            </li>
          </ul>
        </div>

      </div>
    </nav>
  )
}

export default Header