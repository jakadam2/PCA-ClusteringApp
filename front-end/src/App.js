import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileExplorer from './components/file_explorer/FileExplorer';
import DataTypeEditPage from './pages/DataTypeEditPage';

function App() {
  return (
    <div className="px-10 py-10 justify-start min-h-screen">
      <Router>
        <Routes>
          <Route path="/" element={<FileExplorer/>} />
          <Route path="/data-type-edit" element={<DataTypeEditPage/>} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
