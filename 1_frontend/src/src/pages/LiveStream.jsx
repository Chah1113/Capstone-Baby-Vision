import React from 'react';
import { useNavigate } from 'react-router-dom';

function LiveStream() {
  const navigate = useNavigate();

  return (
    <div className="text-on-surface min-h-screen bg-slate-900 font-body transition-colors duration-300">
      
      {/* 🌙 상단 헤더 (뒤로 가기 버튼 포함) */}
      <header className="bg-slate-900/80 backdrop-blur-xl fixed top-0 w-full z-50 flex items-center px-4 py-4 border-b border-slate-800">
        <button onClick={() => navigate(-1)} className="p-2 text-slate-300 hover:text-white transition-colors">
          <span className="material-symbols-outlined">arrow_back</span>
        </button>
        <span className="text-lg font-bold text-white ml-2 font-headline">실시간 CCTV 모니터링</span>
        
        {/* 우측 LIVE 깜빡임 효과 */}
        <div className="ml-auto flex items-center gap-2 bg-red-500/20 px-3 py-1 rounded-full">
          <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
          <span className="text-[10px] font-bold text-red-400 tracking-wider">LIVE</span>
        </div>
      </header>

      {/* 📹 비디오 송출 영역 */}
      <main className="pt-20 px-4 max-w-5xl mx-auto h-screen flex flex-col pb-10">
        <div className="relative w-full grow bg-black rounded-2xl overflow-hidden shadow-2xl border border-slate-800 flex items-center justify-center mt-4">
          
          {/* 👇 백엔드의 스트리밍 서버 주소로 👇 */}
          <img 
          className="w-full h-full object-contain" 
          // baby-vision 백엔드나 MediaMTX 브릿지 서버를 가리키는 ngrok 주소
          src={import.meta.env.VITE_API_BASE_URL}
          alt="실시간 CCTV 화면" 
          />
          
        </div>
        
        {/* 하단 컨트롤러 안내 */}
        <div className="mt-6 bg-slate-800/50 p-4 rounded-xl flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="material-symbols-outlined text-blue-400">videocam</span>
            <div>
              <p className="text-sm font-bold text-white">메인 게이트 카메라 01</p>
              <p className="text-xs text-slate-400">네트워크 상태: 양호 (ngrok)</p>
            </div>
          </div>
          <button onClick={() => navigate(-1)} className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg text-sm font-bold transition-colors">
            종료
          </button>
        </div>
      </main>
    </div>
  );
}

export default LiveStream;