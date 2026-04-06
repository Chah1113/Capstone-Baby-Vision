import React from 'react';
import { Link } from 'react-router-dom';

function Zone() {
  return (
    <div className="bg-background font-body text-on-surface antialiased min-h-screen">
      <header className="bg-slate-50/70 dark:bg-slate-900/70 backdrop-blur-xl docked full-width top-0 sticky z-50 shadow-sm dark:shadow-none flex justify-between items-center px-6 py-4 w-full">
        <div className="flex items-center gap-2">
          <span className="material-symbols-outlined text-blue-700 dark:text-blue-400">visibility</span>
          <h1 className="text-xl font-black text-blue-900 dark:text-blue-50 tracking-tighter font-headline">Eye Catch</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="hover:bg-slate-200/50 dark:hover:bg-slate-800/50 scale-95 active:scale-90 transition-transform duration-200 p-2 rounded-full">
            <span className="material-symbols-outlined text-slate-500 dark:text-slate-400">notifications_active</span>
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-extrabold font-headline tracking-tight text-on-surface">위험 구역 설정</h2>
          <p className="text-on-surface-variant mt-1">아이가 접근하면 즉시 알림을 받을 위험 구역(주방, 베란다 등)을 설정하세요.</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 flex flex-col gap-4">
            <div className="relative aspect-video rounded-3xl overflow-hidden bg-surface-dim group cursor-crosshair">
              <img alt="아이방 구조" className="w-full h-full object-cover" src="https://images.unsplash.com/photo-1519340333755-56e9c1d04579?auto=format&fit=crop&q=80" />
              
              <svg className="absolute inset-0 w-full h-full pointer-events-none">
                <polygon className="fill-tertiary/20 stroke-tertiary stroke-2" points="150,100 400,120 380,300 120,280" />
                <circle className="fill-on-primary stroke-tertiary stroke-2 pointer-events-auto cursor-move" cx="150" cy="100" r="4" />
                <circle className="fill-on-primary stroke-tertiary stroke-2 pointer-events-auto cursor-move" cx="400" cy="120" r="4" />
                <circle className="fill-on-primary stroke-tertiary stroke-2 pointer-events-auto cursor-move" cx="380" cy="300" r="4" />
                <circle className="fill-on-primary stroke-tertiary stroke-2 pointer-events-auto cursor-move" cx="120" cy="280" r="4" />
                <polygon className="fill-primary/10 stroke-primary/40 stroke-2" points="600,200 800,250 750,450 550,400" strokeDasharray="4" />
              </svg>
              
              <div className="absolute top-4 left-4 bg-white/70 backdrop-blur-md px-3 py-2 rounded-xl text-xs font-medium text-primary shadow-sm flex items-center gap-2">
                <span className="material-symbols-outlined text-sm">info</span>
                클릭하여 꼭짓점 추가. 더블 클릭하여 다각형 닫기.
              </div>
              
              <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-2 p-2 bg-white/70 backdrop-blur-md rounded-full shadow-lg border border-white/20">
                <button className="p-3 bg-primary text-white rounded-full shadow-md scale-95 active:scale-90 transition-all flex items-center gap-2 px-5">
                  <span className="material-symbols-outlined">add_circle</span>
                  <span className="text-sm font-semibold">구역 그리기</span>
                </button>
                <button className="p-3 bg-surface-container-highest text-on-surface rounded-full scale-95 active:scale-90 transition-all">
                  <span className="material-symbols-outlined">backspace</span>
                </button>
                <div className="w-px h-8 bg-outline-variant/30 self-center"></div>
                <button className="p-3 bg-surface-container-highest text-on-surface rounded-full scale-95 active:scale-90 transition-all">
                  <span className="material-symbols-outlined">zoom_in</span>
                </button>
              </div>
            </div>
          </div>

          <div className="lg:col-span-4 flex flex-col gap-6">
            <div className="bg-surface-container-lowest rounded-3xl p-6 shadow-sm flex flex-col gap-4">
              <h3 className="text-lg font-bold font-headline">활성 구역</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl group transition-all hover:bg-surface-container">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-8 bg-tertiary rounded-full"></div>
                    <div>
                      <p className="font-bold text-sm">주방 인덕션 주변</p>
                      <p className="text-xs text-on-surface-variant">높은 민감도</p>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between p-4 bg-surface-container-low rounded-xl group transition-all hover:bg-surface-container">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-8 bg-primary rounded-full"></div>
                    <div>
                      <p className="font-bold text-sm">베란다 출입문</p>
                      <p className="text-xs text-on-surface-variant">표준 알림</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-surface-container-lowest rounded-3xl p-6 shadow-sm">
              <h3 className="text-lg font-bold font-headline mb-4">전역 매개변수</h3>
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="text-xs font-semibold text-on-surface-variant tracking-wider uppercase">탐지 정밀도</label>
                  <div className="h-1.5 w-full bg-surface-container-high rounded-full overflow-hidden">
                    <div className="h-full bg-primary w-3/4"></div>
                  </div>
                  <div className="flex justify-between text-[10px] text-on-surface-variant font-bold">
                    <span>유연함</span>
                    <span>정밀함</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-auto flex gap-3 pt-4">
              <button className="flex-1 bg-surface-container-high text-on-surface font-bold py-3 rounded-full hover:bg-surface-variant transition-colors">취소</button>
              <button className="flex-2 bg-linear-to-br from-primary to-blue-600 text-on-primary font-bold py-3 rounded-full shadow-lg scale-95 active:scale-90 transition-all flex justify-center items-center gap-2">
                <span className="material-symbols-outlined text-lg">save</span>
                설정 저장
              </button>
            </div>
          </div>
        </div>
      </main>

      <nav className="fixed bottom-0 left-0 w-full flex justify-around items-center px-4 pb-4 pt-2 bg-slate-50 dark:bg-slate-800/50 shadow-[0_-4px_20px_rgba(0,24,72,0.04)] z-50 rounded-t-xl">
        <Link to="/main" className="flex flex-col items-center justify-center text-slate-500 px-5 py-2 hover:text-blue-600 transition-all">
          <span className="material-symbols-outlined">videocam</span>
          <span className="text-xs font-medium">모니터링</span>
        </Link>
        <Link to="/zone" className="flex flex-col items-center justify-center bg-blue-50 text-blue-800 rounded-2xl px-5 py-2 transition-all">
          <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>grid_view</span>
          <span className="text-xs font-medium">구역</span>
        </Link>
        <Link to="/history" className="flex flex-col items-center justify-center text-slate-500 px-5 py-2 hover:text-blue-600 transition-all">
          <span className="material-symbols-outlined">warning</span>
          <span className="text-xs font-medium">사건 내역</span>
        </Link>
        <Link to="/settings" className="flex flex-col items-center justify-center text-slate-500 px-5 py-2 hover:text-blue-600 transition-all">
          <span className="material-symbols-outlined">settings</span>
          <span className="text-xs font-medium">설정</span>
        </Link>
      </nav>
      <div className="h-24 md:hidden"></div>
    </div>
  );
}

export default Zone;