import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Home from './pages/Home'
import KnnKDTreeKnnSearch from './pages/KnnKDTreeKnnSearch'
import KnnKDTreeKnnSearchLive from './pages/KnnKDTreeKnnSearchLive'
import KnnRTreeKnnSearch from './pages/KnnRTreeKnnSearch'
import KnnRTreeRangeSearch from './pages/KnnRTreeRangeSearch'
import KnnSeqKnnSearch from './pages/KnnSeqKnnSearch'
import KnnSeqRangeSearch from './pages/KnnSeqRangeSearch'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

function App() {

  return (
    <>
      <Header />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/knn-kdtree-knn-search' element={<KnnKDTreeKnnSearch />} />
        <Route path='/knn-kdtree-knn-search-live' element={<KnnKDTreeKnnSearchLive />} />
        <Route path='/knn-rtree-knn-search' element={<KnnRTreeKnnSearch />} />
        <Route path='/knn-rtree-range-search' element={<KnnRTreeRangeSearch />} />
        <Route path='/knn-seq-knn-search' element={<KnnSeqKnnSearch />} />
        <Route path='/knn-seq-range-search' element={<KnnSeqRangeSearch />} />
      </Routes>
    </>
  )
}

export default App
