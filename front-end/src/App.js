import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileExplorer from './components/file_utils/FileExplorer';
import DataTypeEditPage from './pages/DataTypeEditPage';
import MainMenu from './pages/MainMenu';
import FileSaver from './components/file_utils/FileSaver';
import MainPCAComponentsVisualization from './pages/MainPCAComponentsVisualization';
import ClusterizationOptions from './pages/ClusterizationOptions';
import ClusterizationVisualization from './pages/ClusterizationVisualization';

function App() {
    const path = require("path")
    const { execFile } = window.require("child_process")
    var exePath = path.resolve('./backend.exe')
    var python = execFile(exePath, (error, stdout, stderr) => {
        if (error) {
            console.error(`execFile error: ${error}`);
            return;
        }
    console.log(`>>>>>>>>>>>>>>>> ${stdout}`);
    });
    console.log("done");
    return (
        <div className="px-10 py-10 justify-start min-h-screen">
        <Router>
            <Routes>
            <Route path="/" element={<FileExplorer/>} />
            <Route path="/menu" element={<MainMenu/>} />
            <Route path="/data-type-edit" element={<DataTypeEditPage/>} />
            <Route path="/save-file" element={<FileSaver/>} />
            <Route path="/pca-main-components" element={<MainPCAComponentsVisualization/>} />
            <Route path="/clusterization-options" element={<ClusterizationOptions/>} />
            <Route path="/clusterization-visualization" element={<ClusterizationVisualization/>} />
            </Routes>
        </Router>
        </div>
    );
}

export default App;
