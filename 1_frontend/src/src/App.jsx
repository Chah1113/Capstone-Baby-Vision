import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Main from './pages/Main';
import History from './pages/History';
import IncidentDetails from './pages/IncidentDetails';
import Settings from './pages/Settings';
import Zone from './pages/Zone';
import LiveStream from './pages/LiveStream';

function App() {
  
  // 💡 앱이 처음 켜질 때(모든 화면 공통) 다크 모드 상태를 확인하고 적용합니다.
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        {/* 기본 경로 접속 시 로그인 창으로 */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/main" element={<Main />} />
        <Route path="/history" element={<History />} />
        <Route path="/incident-details" element={<IncidentDetails />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/zone" element={<Zone />} />
        <Route path="/live-stream" element={<LiveStream />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;